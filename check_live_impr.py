import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
cmd = 'docker logs --since 1m v-ads-ad-server-1 | grep "type=impression" | wc -l'
stdin, stdout, stderr = client.exec_command(cmd)
print('Live impressions past 1min:', stdout.read().decode('utf-8').strip())
client.close()