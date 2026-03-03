import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
cmd = 'docker exec v-ads-redis-1 redis-cli KEYS "stat:0:*"'
stdin, stdout, stderr = client.exec_command(cmd)
keys = stdout.read().decode('utf-8').strip().split('\n')

if keys and keys[0]:
    for key in keys[:5]:
        cmd_hget = f'docker exec v-ads-redis-1 redis-cli HGETALL "{key}"'
        stdin2, stdout2, stderr2 = client.exec_command(cmd_hget)
        print(f'{key}:\n{stdout2.read().decode("utf-8")}')
else:
    print('No keys found')

client.close()