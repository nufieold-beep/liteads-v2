"""Check live traffic after fixes deployed."""
import paramiko
import re
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("173.208.137.202", username="root", password="Dewa@123")

# Wait for some traffic
time.sleep(5)

# Get recent logs
_, stdout, _ = ssh.exec_command("docker logs --tail=200 liteads-ad-server-1 2>&1")
all_lines = stdout.read().decode().strip().split("\n")

nobid = len([l for l in all_lines if "dsp_204" in l])
bid = len([l for l in all_lines if "Bid received" in l or "bid_price" in l])
sent = len([l for l in all_lines if "Sending ORTB bid request" in l])
fills = len([l for l in all_lines if "VAST tag no fill" in l])
errors = [l for l in all_lines if any(w in l.lower() for w in ["error", "exception", "traceback"]) and "x-robots" not in l]

print(f"Sent: {sent}, No-bid: {nobid}, Bids: {bid}, No-fill: {fills}")
print(f"Errors: {len(errors)}")

# Show country codes
countries = set()
for l in all_lines:
    m = re.search(r'"ortb_country":\s*"([^"]+)"', l)
    if m:
        countries.add(m.group(1))
print(f"Country codes being sent: {countries}")

# Show 3 sample ORTB send logs
ortb_sends = [l for l in all_lines if "Sending ORTB bid request" in l]
for l in ortb_sends[:3]:
    print(l[:300])

# Show 3 sample no-bid logs
nobid_logs = [l for l in all_lines if "dsp_204" in l]
for l in nobid_logs[:3]:
    print(l[:300])

# Show any errors
for l in errors[:5]:
    print("ERR:", l[:300])

ssh.close()
