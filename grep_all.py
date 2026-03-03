import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
# Get ALL instances of "Failed to track video event" over the entire log!
stdin, stdout, stderr = client.exec_command('docker logs v-ads-ad-server-1 | grep "Failed to track video event" | tail -n 50')
out = stdout.read().decode('utf-8').strip()
with open('all_failures.txt', 'w') as f:
    f.write(out)
client.close()