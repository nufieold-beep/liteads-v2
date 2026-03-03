import paramiko
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('173.208.137.202', username='root', password='Dewa@123')
stdin, stdout, stderr = c.exec_command('docker logs --tail 50 v-ads-ad-server-1')
print('OUT:', stdout.read().decode('utf-8'))
print('ERR:', stderr.read().decode('utf-8'))