import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
cmd = 'docker exec v-ads-redis-1 redis-cli KEYS "imp_dedup:*" | wc -l'
stdin, stdout, stderr = client.exec_command(cmd)
print('Dedup keys count:', stdout.read().decode('utf-8').strip())
client.close()