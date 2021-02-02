import pandas as pd
import time
import numpy as np
#https://www.delftstack.com/ko/howto/python-pandas/how-to-pretty-print-an-entire-pandas-series-dataframe/#%25EC%259E%2590%25EB%25A5%25B4%25EC%25A7%2580-%25EC%2595%258A%25EA%25B3%25A0-%25ED%2591%259C%25EC%258B%259C-%25ED%2595%25A0set_option
def hgj (sentence, timesl=0.1):
    for i in range(len(sentence)):
        print(sentence[i], end="")
        time.sleep(timesl)
# print(hgj('창1'))

def isEnglishOrKorean(input_s):
    k_count = 0
    e_count = 0
    result_str = ''
    i = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
            result_str+=c
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            result_str+= ' ' + str(c)
            e_count+=1
        elif ord('0') <= ord(c.lower()) <= ord('9'):
            if i == 0:
                result_str+= ' ' + str(c)
                i+=1
            else:
                result_str+=str(c)
        # if k_count > 1:
        # return "k" if k_count>1 else "e"
    return result_str
# print(isEnglishOrKorean('계시11'))


df = pd.read_csv('./hkj-the-holy-bible.txt', header = None, names=['bible_bcn_content'])
# dropping null value columns to avoid errors
df.dropna(inplace=True)
# new df frame with split value columns
new = df["bible_bcn_content"].str.split(" ", n=1, expand=True)

# making separate first name column from new df frame
df["bible_bcn"] = new[0]

# making separate last name column from new df frame
df["content"] = new[1]

# Dropping old Name columns
df.drop(columns=["bible_bcn_content"], inplace=True)
# print(df)

new2 = df["bible_bcn"].str.split(":", n=1, expand=True)

df['bible_book_name_chapter_number'] = new2[0]
df['number'] = new2[1]
df['content'] = new[1]

df['bible_book_name'] = df['bible_book_name_chapter_number'].apply(lambda x: isEnglishOrKorean(x))
new3 = df['bible_book_name'].str.split(" ", n=1, expand=True)

df['book_name'] = new3[0]
df['chapter_name'] = new3[1]
df.drop(columns=["bible_book_name"], inplace=True)
df.drop(columns=["bible_book_name_chapter_number"], inplace=True)

# df display
# print(df)
# print(df.count(axis = 1))

df_e = pd.read_csv('./kjv-the-holy-bible.txt', header = None, names=['ebible_bcn_content'])
new_e = df_e["ebible_bcn_content"].str.split(" ", n=1, expand=True)

# print(df_e)
# print(df_e.count(axis = 1))

df['ebible_bcn'] = new_e[0]
df['econtent'] = new_e[1]


# df.insert(0, 'bible_id', range(880, 880 + len(df)))
df.insert(0, 'bbid', range(1, 1 + len(df)))
# df = df.assign(New_ID=[880 + i for i in xrange(len(df))])[['bible_id'] + df.columns.tolist()]
# df = df.reset_index()
# df.columns[0] = 'New_ID'
# df['New_ID'] = df.index + 880

# print(df.head())
# print(df)
print(df.count(axis=1))


# https://cmdlinetips.com/2018/03/how-to-change-column-names-and-row-indexes-in-pandas/
df = df[['bbid', 'bible_bcn', 'content', 'book_name', 'chapter_name', 'number',
       'ebible_bcn', 'econtent']]
print(df.columns)

##########
df.columns = ['bbid', 'bible_bcn', 'content', 'book', 'chapter', 'number',
       'ebible_bcn', 'econtent']

def set_pandas_display_options() -> None:
    display = pd.options.display
    display.max_columns = 100
    display.max_rows = 100
    display.max_colwidth = 30
    display.width = None
set_pandas_display_options()
# print(df.head())
print(df.head(10))

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)
# print(df.head())



