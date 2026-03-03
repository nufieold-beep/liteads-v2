import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
cmd = 'docker logs --tail 50 v-ads-ad-server-1'
stdin, stdout, stderr = client.exec_command(cmd)
print('Logs:\n', stdout.read().decode('utf-8'))
client.close()