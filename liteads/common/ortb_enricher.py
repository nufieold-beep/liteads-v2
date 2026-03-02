"""
OpenRTB 2.6 Bid-Request Auto-Enrichment.

When a publisher sends an incomplete ORTB bid request, this module fills
every missing field with IAB-compliant defaults so that downstream DSPs
always receive a fully-formed request.

Usage:
    from liteads.common.ortb_enricher import enrich_bid_request
    enriched = enrich_bid_request(bid_request)   # mutates & returns
"""

from __future__ import annotations

import uuid
from typing import Any, Optional

from liteads.common.logger import get_logger

logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Default values matching the canonical schema
# ─────────────────────────────────────────────────────────────────────────────

_DEFAULTS_VIDEO = {
    "mimes": ["video/mp4"],
    "protocols": [2, 3, 5, 6, 7, 8],
    "w": 1920,
    "h": 1080,
    "plcmt": 1,
    "placement": 1,
    "linearity": 1,
    "startdelay": 0,
    "minduration": 3,
    "maxduration": 30,
    "playbackmethod": [1, 3, 4, 5],
    "delivery": [2],
    "skip": 0,
}

_DEFAULTS_DEVICE = {
    "devicetype": 3,
    "lmt": 0,
    "dnt": 0,
    "language": "en",
}

_DEFAULTS_CONTENT = {
    "len": 1800,
    "livestream": 0,
    "language": "en",
    "cat": ["IAB1-6"],
}

_DEFAULTS_PUBLISHER = {
    "id": "PUB_ID",
    "name": "PUBLISHER",
}

_DEFAULTS_REGS = {
    "coppa": 0,
}

_DEFAULTS_REGS_EXT = {
    "gdpr": 0,
    "us_privacy": "1---",
}

_DEFAULTS_SCHAIN_NODE = {
    "asi": "viadsmedia.com",
    "sid": "778008",
    "hp": 1,
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _set_default(obj: Any, attr: str, default: Any) -> bool:
    """Set *attr* on a Pydantic model if it is ``None`` / empty.

    Returns ``True`` when a default was applied.
    """
    current = getattr(obj, attr, None)
    if current is None or (isinstance(current, (list, str)) and not current):
        setattr(obj, attr, default)
        return True
    return False


def _ensure_dict_defaults(obj: Any, attr: str, defaults: dict) -> None:
    """For an ``ext`` dict attribute, merge missing keys from *defaults*."""
    ext = getattr(obj, attr, None)
    if ext is None:
        setattr(obj, attr, dict(defaults))
        return
    if isinstance(ext, dict):
        for k, v in defaults.items():
            if k not in ext:
                ext[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def enrich_bid_request(
    br: Any,
    *,
    client_ip: Optional[str] = None,
    user_agent: Optional[str] = None,
    slot_id: Optional[str] = None,
) -> Any:
    """Enrich an OpenRTB ``BidRequest`` in-place and return it.

    Parameters
    ----------
    br:
        A ``liteads.schemas.openrtb.BidRequest`` instance (Pydantic model).
    client_ip:
        Real client IP from ``X-Forwarded-For`` header – used when ``device.ip``
        is missing.
    user_agent:
        ``User-Agent`` header value – used when ``device.ua`` is missing.
    slot_id:
        Supply-tag slot ID – used as fallback for ``imp.tagid`` and ``app.id``.
    """
    enriched_fields: list[str] = []

    # ── 1. Top-level BidRequest fields ────────────────────────────────
    if not br.id:
        br.id = f"REQ-{uuid.uuid4().hex[:12]}"
        enriched_fields.append("id")

    if _set_default(br, "at", 1):
        enriched_fields.append("at")

    if _set_default(br, "tmax", 500):
        enriched_fields.append("tmax")

    if not br.cur or br.cur == []:
        br.cur = ["USD"]
        enriched_fields.append("cur")

    # ── 2. Impression + Video ─────────────────────────────────────────
    for imp in br.imp:
        if not imp.id:
            imp.id = "1"
            enriched_fields.append("imp.id")

        tag = slot_id or "SELLER_PLACEMENT_ID"
        if _set_default(imp, "tagid", tag):
            enriched_fields.append("imp.tagid")

        if imp.bidfloor is None or imp.bidfloor == 0.0:
            imp.bidfloor = 5.0
            enriched_fields.append("imp.bidfloor")

        if _set_default(imp, "bidfloorcur", "USD"):
            enriched_fields.append("imp.bidfloorcur")

        # -- Video --
        if imp.video is None:
            # Create a minimal Video object from defaults
            from liteads.schemas.openrtb import Video as OrtbVideo
            imp.video = OrtbVideo(**_DEFAULTS_VIDEO)
            enriched_fields.append("imp.video (created)")
        else:
            v = imp.video
            for key, default in _DEFAULTS_VIDEO.items():
                current = getattr(v, key, None)
                if current is None or (isinstance(current, list) and not current):
                    setattr(v, key, default)
                    enriched_fields.append(f"imp.video.{key}")

    # ── 3. Device ─────────────────────────────────────────────────────
    if br.device is None:
        from liteads.schemas.openrtb import Device as OrtbDevice
        br.device = OrtbDevice(
            ip=client_ip or "",
            ua=user_agent or "",
            **_DEFAULTS_DEVICE,
        )
        enriched_fields.append("device (created)")
    else:
        dev = br.device
        for key, default in _DEFAULTS_DEVICE.items():
            if _set_default(dev, key, default):
                enriched_fields.append(f"device.{key}")

        # Fill IP from header if missing
        if not dev.ip and client_ip:
            dev.ip = client_ip
            enriched_fields.append("device.ip")

        # Fill UA from header if missing
        if not dev.ua and user_agent:
            dev.ua = user_agent
            enriched_fields.append("device.ua")

    # ── 4. Geo auto-enrichment from MaxMind ───────────────────────────
    _enrich_geo(br, enriched_fields)

    # ── 5. App / Publisher / Content ──────────────────────────────────
    if br.app is None:
        from liteads.schemas.openrtb import App as OrtbApp, Publisher as OrtbPublisher
        br.app = OrtbApp(
            id=slot_id or "APP_ID",
            name="APP_NAME",
            bundle="com.example.ctv",
            publisher=OrtbPublisher(**_DEFAULTS_PUBLISHER),
        )
        enriched_fields.append("app (created)")
    else:
        app = br.app
        _set_default(app, "id", slot_id or "APP_ID")
        _set_default(app, "name", "APP_NAME")
        _set_default(app, "bundle", "com.example.ctv")

        # Publisher
        if app.publisher is None:
            from liteads.schemas.openrtb import Publisher as OrtbPublisher
            app.publisher = OrtbPublisher(**_DEFAULTS_PUBLISHER)
            enriched_fields.append("app.publisher (created)")
        else:
            for key, default in _DEFAULTS_PUBLISHER.items():
                _set_default(app.publisher, key, default)

        # Content – only fill lightweight defaults when completely absent
        if app.content is None:
            from liteads.schemas.openrtb import Content as OrtbContent
            app.content = OrtbContent(**_DEFAULTS_CONTENT)
            enriched_fields.append("app.content (created)")
        else:
            for key, default in _DEFAULTS_CONTENT.items():
                if _set_default(app.content, key, default):
                    enriched_fields.append(f"app.content.{key}")

    # ── 6. User ───────────────────────────────────────────────────────
    if br.user is None:
        from liteads.schemas.openrtb import User as OrtbUser
        ifa = br.device.ifa if br.device else None
        br.user = OrtbUser(
            id=ifa or "",
            ext={"consent": "", "eids": []},
        )
        enriched_fields.append("user (created)")
    else:
        if br.user.ext is None:
            br.user.ext = {"consent": "", "eids": []}
            enriched_fields.append("user.ext")
        else:
            if "consent" not in br.user.ext:
                br.user.ext["consent"] = ""
            if "eids" not in br.user.ext:
                br.user.ext["eids"] = []

    # ── 7. Regs ───────────────────────────────────────────────────────
    if br.regs is None:
        from liteads.schemas.openrtb import Regs as OrtbRegs
        br.regs = OrtbRegs(
            coppa=0,
            ext=dict(_DEFAULTS_REGS_EXT),
        )
        enriched_fields.append("regs (created)")
    else:
        if _set_default(br.regs, "coppa", 0):
            enriched_fields.append("regs.coppa")
        _ensure_dict_defaults(br.regs, "ext", _DEFAULTS_REGS_EXT)

    # ── 8. Source / SChain ────────────────────────────────────────────
    _enrich_source(br, slot_id, enriched_fields)

    # Log summary
    if enriched_fields:
        logger.info(
            "ORTB request auto-enriched",
            request_id=br.id,
            enriched_count=len(enriched_fields),
            enriched_fields=enriched_fields,
        )

    return br


# ─────────────────────────────────────────────────────────────────────────────
# Private helpers
# ─────────────────────────────────────────────────────────────────────────────

def _enrich_geo(br: Any, enriched_fields: list[str]) -> None:
    """Auto-attach ``device.geo`` via MaxMind when the publisher omits it."""
    if br.device is None or not br.device.ip:
        return

    geo = br.device.geo
    # If geo already has a country, skip
    if geo is not None and geo.country:
        return

    try:
        from liteads.common.geoip import lookup as geoip_lookup
        from liteads.schemas.openrtb import Geo as OrtbGeo

        g = geoip_lookup(br.device.ip)
        if g and g.country:
            br.device.geo = OrtbGeo(
                country=g.country,
                region=g.region,
                city=g.city,
                metro=g.metro,
                lat=g.lat,
                lon=g.lon,
                zip=getattr(g, "zip", None),
                type=g.type,         # 2 = IP-based
                ipservice=g.ipservice,  # 3 = MaxMind
            )
            enriched_fields.append("device.geo (MaxMind)")
    except Exception as exc:
        logger.debug("GeoIP enrichment skipped", error=str(exc))


def _enrich_source(br: Any, slot_id: Optional[str], enriched_fields: list[str]) -> None:
    """Ensure ``source.ext.schain`` is present with our node."""
    if br.source is None:
        from liteads.schemas.openrtb import Source as OrtbSource, SupplyChain, SupplyChainNode

        br.source = OrtbSource(
            ext={
                "schain": {
                    "ver": "1.0",
                    "complete": 1,
                    "nodes": [
                        {
                            "asi": "viadsmedia.com",
                            "sid": slot_id or "778008",
                            "hp": 1,
                        }
                    ],
                }
            },
        )
        enriched_fields.append("source (created)")
        return

    # Source exists but schain may be missing
    src = br.source
    if src.schain is None:
        # Check ext.schain too (some SSPs put it there)
        if src.ext and "schain" in src.ext:
            return  # already has schain in ext

        from liteads.schemas.openrtb import SupplyChain, SupplyChainNode
        src.schain = SupplyChain(
            ver="1.0",
            complete=1,
            nodes=[
                SupplyChainNode(
                    asi="viadsmedia.com",
                    sid=slot_id or "778008",
                    hp=1,
                )
            ],
        )
        enriched_fields.append("source.schain (created)")
