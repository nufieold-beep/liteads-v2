import paramiko
import time
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')

cmd_db = 'docker exec v-ads-postgres-1 psql -U liteads -d liteads -c "select count(*) from ad_events where event_type=1;"'
stdin, stdout, stderr = client.exec_command(cmd_db)
out = stdout.read().decode('utf-8').strip()

with open('res.txt', 'w') as f:
    f.write('DB Impressions Total:\n' + out)

client.close()