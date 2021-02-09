import pandas as pd
import seaborn as sns

titanic = sns.load_dataset('titanic')
df = titanic[['age','sex','class','fare','survived']]
print("승객 수 :", len(df))
print(df.head())


grouped = df.groupby('class')
print(grouped)
print(type(grouped))

for key, group in grouped:
    print("* key", key)
    print("* count", len(group))
    print(group.head())
    print('\n')

