import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
cmd = 'docker exec v-ads-postgres-1 psql -U liteads -d liteads -c "select id, request_id, event_type, cost, win_price from ad_events order by id desc limit 10;"'
stdin, stdout, stderr = client.exec_command(cmd)
print('STDOUT:\n', stdout.read().decode('utf-8'))
client.close()