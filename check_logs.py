import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
stdin, stdout, stderr = client.exec_command('docker logs --tail 2000 v-ads-ad-server-1 | grep "Failed to track video event" | tail -n 10')
print('Errors:\n', stdout.read().decode('utf-8'))
client.close()
