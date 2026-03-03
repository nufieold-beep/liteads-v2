import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
stdin, stdout, stderr = client.exec_command('cat /root/v-ads/.env || cat /root/v-ads/docker-compose.yml')
print(stdout.read().decode('utf-8'))
client.close()