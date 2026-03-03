"""Quick SSH helper — run commands on the remote server."""
import sys
import paramiko

HOST = "173.208.137.202"
USER = "root"
PASS = "Dewa@123"

def run_cmds(commands: list[str]) -> None:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS, timeout=15)
    transport = ssh.get_transport()
    if transport:
        transport.set_keepalive(30)
    for cmd in commands:
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=300)
        # Read with buffering to handle large outputs
        out = stdout.read().decode("utf-8", errors="replace").strip()
        err = stderr.read().decode("utf-8", errors="replace").strip()
        label = cmd.split("&&")[-1].strip()[:60]
        print(f"--- {label} ---")
        if out:
            # Truncate long output
            lines = out.split("\n")
            if len(lines) > 100:
                print("\n".join(lines[:30]))
                print(f"  ... ({len(lines) - 60} lines omitted) ...")
                print("\n".join(lines[-30:]))
            else:
                print(out)
        if err:
            err_lines = err.split("\n")
            if len(err_lines) > 50:
                print("[stderr]", "\n".join(err_lines[-30:]))
            else:
                print(f"[stderr] {err}")
        print()
    ssh.close()

if __name__ == "__main__":
    cmds = sys.argv[1:] if len(sys.argv) > 1 else [
        "cd /root/v-ads && docker compose up -d ad-server 2>&1",
        "sleep 5 && docker ps --filter name=v-ads-ad-server 2>&1",
        "cd /root/v-ads && docker compose logs ad-server --tail=30 2>&1",
    ]
    run_cmds(cmds)
