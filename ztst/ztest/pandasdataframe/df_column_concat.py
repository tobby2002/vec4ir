import pandas as pd
import seaborn as sns
from functools import reduce

# a = ["12","23","324","42"]
# b = map(str, a)
# print(b)
# a = list(map(str, a))
# print(a)


titanic = sns.load_dataset('titanic')

# column concat
# https://ponyozzang.tistory.com/610  --> key point url

columns = ['sex', 'class', 'deck']
# columns = ['sex', 'class', 'embarked']
df = titanic[columns]
df.set_index('sex')
# df['combined'] = df['sex'] + df['class']

def dfconcat(df, columns, name = 'combined'):
    # print(df['name'].str.cat(df['state'], sep=' in '))
    i = 0
    for c in columns:
        if i == 0:
            df[name] = df[c].astype(str)
        else:
            df[name] = df[name].str.cat(df[c].astype(str), sep=' ')
        i += 1
    return df
df = dfconcat(df, columns, name='combi')

# df['combined'] = df.apply(lambda x: x['sex'] + ' ' + x['class'] + ' ' + x['deck'], axis=1)




print("count :", len(df))
print(df.head())


import pandas as pd

df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie']
                      , 'age': [24, 42, 35]
                      , 'state': ['NY', 'CA', 'LA']
                      , 'point': [64, 92, 75]})
print(df['name'].str.cat(df['state'], sep=' in '))
# 0      Alice in NY
# 1        Bob in CA
# 2    Charlie in LA
# Name: name, dtype: object


import pandas as pd

df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie']
                      , 'age': [24, 42, 35]
                      , 'state': ['NY', 'CA', 'LA']
                      , 'point': [64, 92, 75]})
print(df['name'].str.cat(df['age'].astype(str), sep='-'))
# 0      Alice-24
# 1        Bob-42
# 2    Charlie-35
# Name: name, dtype: object

print(df['name'] + '-' + df['age'].astype(str))
# 0      Alice-24
# 1        Bob-42
# 2    Charlie-35
# dtype: object
