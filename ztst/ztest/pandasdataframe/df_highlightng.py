import pandas as pd
import seaborn as sns
from functools import reduce

# a = ["12","23","324","42"]
# b = map(str, a)
# print(b)
# a = list(map(str, a))
# print(a)
def trim_text(intext, first=False):
    intext_l = intext.split()
    if first:
        del intext_l[0]
    del intext_l[-1]
    print(intext_l)
    r_text = ' '.join(intext_l)
    return r_text


def highlight_list(h_text, h_word_list, h_tag_pre, h_tag_post, h_snippets, h_maxlength):
    h_words = list()
    highlighted_text = h_text
    snippets = list()
    if h_word_list:
        for h_word in h_word_list:
            replace_word = h_tag_pre + h_word + h_tag_post

            highlighted_text = highlighted_text.replace(h_word, replace_word)
            h_words.append(replace_word)
            print(highlighted_text)
        remain_text = highlighted_text

        if len(highlighted_text) <= h_maxlength:
            snippets.append(highlighted_text)
            return snippets

        if h_words:
            while len(snippets) < h_snippets:
                for h_w in h_words:
                    max_idx = round(h_maxlength) + len(h_w)
                    p_idx = remain_text.find(h_w)
                    if p_idx <= max_idx:
                        cut_text = remain_text[:max_idx - 1]
                        cut_text = trim_text(cut_text)
                        remain_text = remain_text[len(cut_text):]
                        snippets.append(cut_text)
                    elif p_idx > max_idx:
                        e_idx = p_idx + (round(h_maxlength / 2)) + len(h_w)
                        if e_idx <= len(remain_text):
                            cut_text = remain_text[p_idx - (round(h_maxlength/2) + len(h_w)):e_idx]
                            remain_text = remain_text[len(cut_text):]
                        else:
                            cut_text = remain_text[p_idx - (round(h_maxlength/2) + len(h_w)):len(remain_text)]
                            cut_text = trim_text(cut_text)
                            cut_idx = remain_text.find(cut_text)
                            remain_text = remain_text[:cut_idx] \
                                          + remain_text[cut_idx + len(cut_text):]
                        snippets.append(cut_text)
    return snippets


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
# df = dfconcat(df, columns, name='combi')
h_text = '우리나라 대한민국'
h_tag_pre = '<span>'
h_tag_post = '</span>'
h_word_list = ['a']
h_snippets = 4
h_maxlength = 50

df['highlight'] = df.apply(lambda x: highlight_list(x['sex'], h_word_list, h_tag_pre, h_tag_post, h_snippets, h_maxlength), axis=1)



print("count :", len(df))
print(df.head())

#
# import pandas as pd
#
# df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie']
#                       , 'age': [24, 42, 35]
#                       , 'state': ['NY', 'CA', 'LA']
#                       , 'point': [64, 92, 75]})
# print(df['name'].str.cat(df['state'], sep=' in '))
# # 0      Alice in NY
# # 1        Bob in CA
# # 2    Charlie in LA
# # Name: name, dtype: object
#

# import pandas as pd
#
# df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie']
#                       , 'age': [24, 42, 35]
#                       , 'state': ['NY', 'CA', 'LA']
#                       , 'point': [64, 92, 75]})
#
# print(df['name'])

#
# print(df['name'].str.cat(df['age'].astype(str), sep='-'))
# # 0      Alice-24
# # 1        Bob-42
# # 2    Charlie-35
# # Name: name, dtype: object
#
# print(df['name'] + '-' + df['age'].astype(str))
# # 0      Alice-24
# # 1        Bob-42
# # 2    Charlie-35
# # dtype: object



