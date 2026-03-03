import paramiko
import time

def review_server():
    host = "173.208.137.202"
    user = "root"
    password = "Dewa@123"

    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password, timeout=10)
        
        commands = {
            "System Uptime & Load": "uptime",
            "Memory Usage": "free -m",
            "Docker Containers Status": "cd /root/v-ads && docker compose ps",
            "Local VAST Tags Latency Test": "curl -s -o /dev/null -w '%{time_total}s' 'http://localhost:8000/api/vast?sid=1992&test=1'",
            "Recent Ad Server Logs (Live Traffic)": "docker logs --tail 15 v-ads-ad-server-1"
        }
        
        for title, cmd in commands.items():
            print(f"\n=== {title} ===")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode('utf-8').strip()
            err = stderr.read().decode('utf-8').strip()
            if out:
                print(out)
            if err:
                print(err)
                
    except Exception as e:
        print(f"Error connecting: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    review_server()