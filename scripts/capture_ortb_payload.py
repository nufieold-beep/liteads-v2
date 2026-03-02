"""Capture one full ORTB bid request payload from the live server."""
import paramiko
import json
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("173.208.137.202", username="root", password="Dewa@123")

capture_script = '''import sys, json
sys.path.insert(0, "/app")
from liteads.ad_server.services.demand_forwarder import DemandForwarder, _strip_empty, _slim_payload
from liteads.schemas.request import AdRequest, VideoPlacementInfo, DeviceInfo, GeoInfo, AppInfo

ad_req = AdRequest(slot_id="ctv_preroll", environment="ctv",
    video=VideoPlacementInfo(width=1920, height=1080, max_duration=30, min_duration=5),
    device=DeviceInfo(device_type="ctv", ua="Mozilla/5.0 (Linux; Android 9; AFTR)", ip="108.235.97.58",
        ifa="b9e0cf2b-6003-4079-ba75-09485ffe05d9", device_type_raw=3, os="Android",
        make="Amazon Fire TV Stick", model="AFTR", ifa_type="afai"),
    geo=GeoInfo(country="US", latitude=40.7128, longitude=-74.0060),
    app=AppInfo(app_bundle="B06XJMH3QG", app_name="Discovery Go - Fire Tv",
        store_url="https://www.amazon.com/dp/b06xjmh3qg/",
        content_genre="entertainment", content_language="en"),
    us_privacy="1YNN")

class FakeTag:
    id = 1
    name = "CTV Pre-Roll"
    slot_id = "ctv_preroll"
    publisher_id = 1
    bid_floor = 0.0
    width = 1920
    height = 1080
    min_duration = 5
    max_duration = 30

bid_req = DemandForwarder._build_bid_request(ad_request=ad_req, request_id="test-123",
    supply_tag=FakeTag(), bid_floor=0.0, tmax=500)
payload = bid_req.model_dump(exclude_none=True)
payload = _strip_empty(payload)
payload = _slim_payload(payload)
print(json.dumps(payload, indent=2))
'''

# Write script to host, then copy into container
sftp = ssh.open_sftp()
with sftp.file("/tmp/capture_ortb.py", "w") as f:
    f.write(capture_script)
sftp.close()

ssh.exec_command("docker cp /tmp/capture_ortb.py liteads-ad-server-1:/tmp/capture_ortb.py")
time.sleep(1)

_, stdout, stderr = ssh.exec_command(
    "docker exec liteads-ad-server-1 python3 /tmp/capture_ortb.py",
    timeout=15,
)
out = stdout.read().decode().strip()
err = stderr.read().decode().strip()

if out:
    print("=== ACTUAL ORTB PAYLOAD ===")
    print(out)
else:
    print("=== STDOUT EMPTY ===")

if err:
    print("\n=== STDERR ===")
    print(err[-3000:])

ssh.close()
