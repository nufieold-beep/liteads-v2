import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
cmd = 'docker exec v-ads-postgres-1 psql -U liteads -d liteads -c "INSERT INTO campaigns (id, name, type, status, user_id, start_date, created_at, updated_at) VALUES (0, \'DSP Wrappers\', 1, 1, 1, NOW(), NOW(), NOW()) ON CONFLICT (id) DO NOTHING;"'
stdin, stdout, stderr = client.exec_command(cmd)
print('STDOUT:\n', stdout.read().decode('utf-8'))
print('STDERR:\n', stderr.read().decode('utf-8'))
client.close()