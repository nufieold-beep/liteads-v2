import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
cmd1 = 'docker exec v-ads-postgres-1 psql -U liteads -d liteads -c "INSERT INTO advertisers (id, name, type, contact_name, contact_email) VALUES (0, \'DSP Wrappers\', 1, \'System\', \'sys@sys.com\') ON CONFLICT (id) DO NOTHING;"'
cmd2 = 'docker exec v-ads-postgres-1 psql -U liteads -d liteads -c "INSERT INTO campaigns (id, advertiser_id, name, budget_daily, budget_total, bid_type, bid_amount, bid_floor) VALUES (0, 0, \'DSP Wrappers\', 999999, 999999, 1, 0, 0) ON CONFLICT (id) DO NOTHING;"'

for cmd in [cmd1, cmd2]:
    stdin, stdout, stderr = client.exec_command(cmd)
    print(f'CMD: {cmd}')
    print('STDOUT:\n', stdout.read().decode('utf-8'))
    print('STDERR:\n', stderr.read().decode('utf-8'))
client.close()