import re
fq = 'chapter:1 and number:14 or aa:1'
columns = ['chapter', 'number']
def check_key_in_columns(fq, columns):
    fq_r = fq.replace('AND', 'and')
    fq_r = fq_r.replace('OR', 'or')

    fq_r_l = re.split('or|and ', fq_r)
    fq_r_l = list(map(lambda x: x.strip(), fq_r_l))
    fq_r_l = list(map(lambda x: x.split()[0].lower(), fq_r_l))
    print(fq_r_l)
    return fq_r
print(check_key_in_columns(fq, columns))