# a = 0.9
# b = 2
#
# c = a * b
# print(c)
#
# d = a ** b
# print(d)
#
# from benedict import benedict
# d = benedict()
#
# # set values by keypath
# d['profile.firstname'] = 'Fabio'
# d['profile.lastname'] = 'Caccamo'
# print(d) # -> { 'profile':{ 'firstname':'Fabio', 'lastname':'Caccamo' } }
# print(d['profile']) # -> { 'firstname':'Fabio', 'lastname':'Caccamo' }
#
# # check if keypath exists in dict
# print('profile.lastname' in d) # -> True
#
# # delete value by keypath
# del d['profile.lastname']

# from benedict import benedict
# dic = {'aaa' : 1}
# bd = benedict(dic)
# # bd = benedict()
#
# s = 'sss'
# t = 'ttt'
# u = 'uuu'
# content = 'contents...'
# bd[s+'.'+t+'.'+u] = content
# print(bd)
# print(dic)

# import os
# os_info = os.uname()
# os.uname().sysname == 'Linux'

# import socket
# def get_ip():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         # doesn't even have to be reachable
#         s.connect(('10.255.255.255', 1))
#         IP = s.getsockname()[0]
#     except Exception:
#         IP = '127.0.0.1'
#     finally:
#         s.close()
#     return IP
# print(get_ip())

import socket
ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
print(ip)

import socket
print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])


import socket
addr = socket.gethostbyname(socket.gethostname())
print(addr)