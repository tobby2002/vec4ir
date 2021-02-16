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

from benedict import benedict

bd = benedict()

s = 'sss'
t = 'ttt'
u = 'uuu'
content = 'contents...'
bd[s+'.'+t+'.'+u] = content
print(bd)


