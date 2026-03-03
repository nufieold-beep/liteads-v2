import paramiko

def check_redis():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect('173.208.137.202', username='root', password='Dewa@123')
        
        print('--- Redis Keys matching stat:* ---')
        stdin, stdout, stderr = client.exec_command('docker exec v-ads-redis-1 redis-cli KEYS "stat:*"')
        keys = stdout.read().decode('utf-8').strip().split('\n')
        keys = [k for k in keys if k]
        print(f'Found {len(keys)} stat:* keys')
        
        for idx, key in enumerate(keys[:5]):
            print(f'\nKey: {key}')
            stdin, stdout, stderr = client.exec_command(f'docker exec v-ads-redis-1 redis-cli HGETALL "{key}"')
            data = stdout.read().decode('utf-8').strip()
            print(data)

        print('\n--- Recent Database Events ---')
        sql = 'docker exec -t v-ads-postgres-1 psql -U postgres -d liteads -c "SELECT id, event_type, campaign_id, EXTRACT(EPOCH FROM created_at) as ts FROM event_logs ORDER BY created_at DESC LIMIT 5;"'
        stdin, stdout, stderr = client.exec_command(sql)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))

    finally:
        client.close()

if __name__ == '__main__':
    check_redis()
