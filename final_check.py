import paramiko
import time
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
print('Wait a few seconds for an impression...')
time.sleep(10)
cmd_logs = 'docker logs --since 15m v-ads-ad-server-1 | grep "type=impression" | wc -l'
stdin, stdout, stderr = client.exec_command(cmd_logs)
print('Recent Nginx impressions in 15m:', stdout.read().decode('utf-8').strip())

cmd_db = 'docker exec v-ads-postgres-1 psql -U liteads -d liteads -c "select count(*) from ad_events where event_type=1 and created_at > now() - interval \'15 minutes\';"'
stdin, stdout, stderr = client.exec_command(cmd_db)
print('Recent DB impressions in 15m:\n', stdout.read().decode('utf-8').strip())

client.close()