import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
stdin, stdout, stderr = client.exec_command('docker logs --tail 5000 v-ads-ad-server-1 | grep "error" | tail -n 20')
with open('errors.txt', 'w') as f:
    f.write('Errors:\n' + stdout.read().decode('utf-8'))
client.close()