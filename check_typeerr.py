import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
stdin, stdout, stderr = client.exec_command('docker logs --tail 20000 v-ads-ad-server-1 | grep "keyword argument"')
out = stdout.read().decode('utf-8').strip()
print('Errors:\n' + out[:2000])
client.close()