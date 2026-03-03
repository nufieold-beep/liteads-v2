import paramiko
import time
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')

cmd_logs = 'docker logs --since 5m v-ads-ad-server-1 | grep "type=impression"'
stdin, stdout, stderr = client.exec_command(cmd_logs)
out = stdout.read().decode('utf-8').strip()

with open('res2.txt', 'w') as f:
    f.write('Impressions last 5m:\n' + out)

client.close()