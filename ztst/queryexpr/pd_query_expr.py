# https://blog.naver.com/wideeyed/221867273249

# https://kongdols-room.tistory.com/120

# sort=CORR_DATE+desc

# fq=KNWLG_TYPE_ID:KT0004
# qf=KNWLG_NAME ATACH_CONTENTS FILE_NAME TAGS




import seaborn as sns

titanic = sns.load_dataset('titanic')
df = titanic[['age', 'sex', 'class', 'fare', 'survived']]
print("승객 수 :", len(df))
print(df.head())

# fq = 'CL_HIERY_CH_CD:T'
# fq = 'CL_HIERY_CH_CD:(I or T or P or W or QA)'

# fq = 'sex:male and class:Third '
fq = 'sex: (male or female)'
fq = 'age:54 and survived:1'

import re

def add_komma_with_equal(s):
    fq_l = re.split('or|and ', s)
    for i in fq_l:
        # value = eval(i.split(':')[1])
        value = i.split(':')[1]
        if isinstance(value, str):
            value = '"' + value.strip() + '" '
        s = s.replace(i, ' ' + i.split(':')[0].strip() + ' == ' + str(value) + ' ')
    return s

def add_komma(s):
    fq_l = re.split('or|and ', s)
    for i in fq_l:
        if isinstance(i, str):
            s = s.replace(i, ' "' + i.strip() + '" ')
    return s

def fq_exp(fq):
    fq = fq.replace('AND', ' and ')
    fq = fq.replace('OR', ' or ')

    # case fq = 'CORR_DATE:[2021-03-04T00:00:00Z TO 2021-03-11T23:59:59Z]
    if fq.count('[') == 1 and fq.count(']') == 1 and fq.lower().count('to') == 1:
        fq_cd = fq.split(':')[0]
        fq_time = fq.split(':')[1]

        fq_time = fq_time.replace('[', '')
        fq_time = fq_time.replace(']', '')

        fq_time = fq_time.replace('T', '')
        fq_time = fq_time.replace('Z', '')

        fq_time1 = fq_time.split('TO').strip()[0]
        fq_time2 = fq_time.split('TO').strip()[1]

        fq_expr = '%s >= "%s" and %s <= "%s"' % (fq_cd, fq_time1, fq_cd, fq_time2)

    # case fq = 'CL_HIERY_CH_CD:(I or T or P or W or QA)'
    elif fq.count(':') == 1 and fq.count('(') == 1 \
            and fq.count(')') == 1 and fq.count('and') != 1:
        fq_expr = fq.replace(':', ' in ')

        items_1 = re.findall('\(([^)]+)', fq_expr)  # extracts string in bracket()
        for i in items_1:
            i_komma = add_komma(i)
            fq_expr = fq_expr.replace(i, i_komma)
        fq_expr = fq_expr.replace('(', '[')
        fq_expr = fq_expr.replace(')', ']')
        fq_expr = fq_expr.replace('or', ',')

    # case fq = 'CL_HIERY_CH_CD:T'
    else:
        fq_expr = add_komma_with_equal(fq)

    return fq_expr

df_fq = df.query(fq_exp(fq))
print(df_fq)
