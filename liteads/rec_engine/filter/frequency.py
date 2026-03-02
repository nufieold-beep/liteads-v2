"""
Frequency filter – DISABLED for CTV.

CTV devices do not have persistent user identifiers (no cookies/sessions),
so frequency capping is not applicable.  This module is retained as a stub
for potential future in-app use.
"""

from __future__ import annotations

from typing import Any

from liteads.common.logger import get_logger
from liteads.rec_engine.filter.base import BaseFilter
from liteads.schemas.internal import AdCandidate, UserContext

logger = get_logger(__name__)


class FrequencyFilter(BaseFilter):
    """Stub – frequency capping is disabled for CTV environments."""

    def __init__(self, **kwargs: Any) -> None:
        pass

    async def filter(
        self,
        candidates: list[AdCandidate],
        user_context: UserContext,
        **kwargs: Any,
    ) -> list[AdCandidate]:
        return candidates

    async def filter_single(
        self,
        candidate: AdCandidate,
        user_context: UserContext,
        **kwargs: Any,
    ) -> bool:
        return True
