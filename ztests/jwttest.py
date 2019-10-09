import jwt

encoded_jwt = jwt.encode({'ip': '127.0.0.1'}, 'secret', algorithm='HS256')
# encoded_jwt
# 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
# print(jwt.decode(encoded_jwt, 'secret', algorithms=['HS256']))

DB_INFO = jwt.decode(encoded_jwt, 'secret', algorithms=['HS256'])
# {'some': 'payload'}
print(DB_INFO['ip'])

