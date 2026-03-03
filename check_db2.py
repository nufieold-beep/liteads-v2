import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
# Insert a dummy campaign 0 to fix the foreign key constraint immediately 
stdin, stdout, stderr = client.exec_command('docker exec v-ads-postgres-1 psql -U postgres -d liteads -c "INSERT INTO campaigns (id, name, type, status, budget, user_id, start_date, created_at, updated_at) VALUES (0, \'DSP Wrappers\', 1, 1, 999999, 1, NOW(), NOW(), NOW()) ON CONFLICT (id) DO NOTHING;"')
print('Camapigns:\n', stdout.read().decode('utf-8'))
client.close()