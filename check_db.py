import paramiko

def check_db():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect('173.208.137.202', username='root', password='Dewa@123')
        
        print('\n--- Recent Database Events ---')
        sql = 'docker exec -t v-ads-postgres-1 psql -U liteads -d liteads -c "SELECT id, event_type, campaign_id, request_id FROM ad_events ORDER BY id DESC LIMIT 10;"'
        stdin, stdout, stderr = client.exec_command(sql)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))

    finally:
        client.close()

if __name__ == '__main__':
    check_db()
