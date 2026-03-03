import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
cmd = 'cat /root/v-ads/liteads/ad_server/services/event_service.py | grep "isinstance(video"'
stdin, stdout, stderr = client.exec_command(cmd)
print('Deployed patch:\n', stdout.read().decode('utf-8'))
client.close()