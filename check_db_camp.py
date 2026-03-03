import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('173.208.137.202', username='root', password='Dewa@123')
# Insert a dummy campaign 0 to fix the foreign key constraint immediately 
stdin, stdout, stderr = client.exec_command('docker exec v-ads-postgres-1 psql -U postgres -d liteads -c "select * from campaigns limit 10;"')
print('Camapigns:\n', stdout.read().decode('utf-8'))
client.close()