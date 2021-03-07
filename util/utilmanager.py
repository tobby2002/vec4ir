#!/usr/bin/env python3
# coding: utf-8
import os, sys
import re
import bios
import timeit
import numpy as np
import re
import string

try:
    from konlpy.tag import Mecab
    mecab = Mecab()
except Exception as e:
    import mecab
    mecab = mecab.MeCab()
from scipy.stats import rankdata
from collections import Counter
# from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from ir.text_preprocessing import TextPreprocessing
from soynlp.hangle import jamo_levenshtein
from soynlp.hangle import compose, decompose, character_is_korean
from util.logmanager import logz
import benedict
log = logz()


def flatten(l):
    """
    flattens a list of list structure... nothing else.
    """
    return [item for sublist in l for item in sublist]


def filter_vocab(model, words, oov=None):
    filtered = []
    for word in words:
        if word in model:
            filtered.append(word)
        elif oov:
            filtered.append(oov)
    return filtered


def argtopk(A, k=None, sort=True):
    """ Get the the top k elements (in sorted order)
    >>> A = np.asarray([5,4,3,6,7,8,9,0])
    >>> A[argtopk(A, 3)]
    array([9, 8, 7])
    >>> argtopk(A, 1)
    array([6])
    >>> argtopk(A, 6)
    array([6, 5, 4, 3, 0, 1])
    >>> argtopk(A, 10)
    array([6, 5, 4, 3, 0, 1, 2, 7])
    >>> argtopk(A, 28)
    array([6, 5, 4, 3, 0, 1, 2, 7])
    >>> argtopk(A, None)
    array([6, 5, 4, 3, 0, 1, 2, 7])
    >>> X = np.arange(20)
    >>> argtopk(X, 10)
    array([19, 18, 17, 16, 15, 14, 13, 12, 11, 10])
    """
    assert k != 0, "That does not make sense"
    if k is not None and k < 0:
        # Just invert A element-wise
        k = -k
        A = -A
    A = np.asarray(A)
    if len(A.shape) > 1:
        raise ValueError('argtopk only defined for 1-d slices')
    axis = -1
    if k is None or k >= A.size:
        # if list is too short or k is None, return all in sort order
        if sort:
            return np.argsort(A, axis=axis)[::-1]
        else:
            return np.arange(A.shape[0])

    # assert k > 0
    # now 0 < k < len(A)
    ind = np.argpartition(A, -k, axis=axis)[-k:]
    if sort:
        # sort according to values in A
        # argsort is always from lowest to highest, so reverse
        ind = ind[np.argsort(A[ind], axis=axis)][::-1]

    return ind


def collection_statistics(embedding, documents, analyzer=None, topn=None):
    # print(embedding, analyzer, documents, sep='\n')
    c = Counter(n_tokens=0, n_embedded=0, n_oov=0)
    f = Counter()
    for document in documents:
        words = analyzer(document) if analyzer is not None else document
        for word in words:
            c['n_tokens'] += 1
            if word in embedding:
                c['n_embedded'] += 1
            else:
                f[word] += 1
                c['n_oov'] += 1

    d = dict(c)
    d['oov_ratio'] = c['n_oov'] / c['n_tokens']
    if topn:
        return d, f.most_common(topn)
    return d


def build_analyzer(tokenizer=None, stop_words=None, lowercase=True):
    """
    A wrapper around sklearns CountVectorizers build_analyzer, providing an
    additional keyword for nltk tokenization.

    :tokenizer:
        None or 'sklearn' for default sklearn word tokenization,
        'sword' is similar to sklearn but also considers single character words
        'nltk' for nltk's word_tokenize function,
        or callable.
    :stop_words:
         False, None for no stopword removal, or list of words, 'english'/True
    :lowercase:
        Lowercase or case-sensitive analysis.
    """
    # some default options for tokenization
    if not callable(tokenizer):
        tokenizer, token_pattern = {
            'sklearn': (None, r"(?u)\b\w\w+\b"),  # mimics default
            'sword': (None, r"(?u)\b\w+\b"),   # specifically for GoogleNews
            # 'nltk': (word_tokenize, None)  # uses punctuation for GloVe models
        }[tokenizer]

    # allow binary decision for stopwords
    sw_rules = {True: 'english', False: None}
    if stop_words in sw_rules:
        stop_words = sw_rules[stop_words]

    # employ the cv to actually build the analyzer from the components
    analyzer = CountVectorizer(analyzer='word',
                               tokenizer=tokenizer,
                               token_pattern=token_pattern,
                               lowercase=lowercase,
                               stop_words=stop_words).build_analyzer()
    return analyzer


def result_rank(result):
    # result_order = rankdata(result, mehtod='max')
    # reverse_rank = rankdata([-1 * i for i in result_order]).astype(float)

    result_order = rankdata(result, mehtod='ordinal')
    reverse_rank = rankdata([-1 * i for i in result_order]).astype(int)
    return reverse_rank

def dfconcat(df, columns, sep = ' ', name = 'combined'):
    """
    # https://ponyozzang.tistory.com/610?category=800537
    columns = ['sex', 'class', 'embarked']
    df = dfconcat(df, columns, name='combi')
    # print(df['name'].str.cat(df['state'], sep=' in '))
    :param df:
    :param columns:
    :param name:
    :return:
    """
    i = 0
    for c in columns:
        if i == 0:
            df[name] = df[c].astype(str)
        else:
            df[name] = df[name].str.cat(df[c].astype(str), sep=sep)
        i += 1
    return df

NO_JONGSUNG = 'ᴕ'

CHOSUNGS = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JOONGSUNGS = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNGS = [NO_JONGSUNG, 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
             'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

N_CHOSUNGS = 19
N_JOONGSUNGS = 21
N_JONGSUNGS = 28

FIRST_HANGUL = 0xAC00  # '가'
LAST_HANGUL = 0xD7A3  # '힣'

def to_jaso(s):
    result = []
    for c in s:
        if ord(c) < FIRST_HANGUL or ord(c) > LAST_HANGUL:  # if a character is a hangul
            result.append(c)
        else:
            code = ord(c) - FIRST_HANGUL
            jongsung_index = code % N_JONGSUNGS
            code //= N_JONGSUNGS
            joongsung_index = code % N_JOONGSUNGS
            code //= N_JOONGSUNGS
            chosung_index = code

            result.append(CHOSUNGS[chosung_index])
            result.append(JOONGSUNGS[joongsung_index])
            result.append(JONGSUNGS[jongsung_index])

    return ''.join(result)


DEFAULT_ANALYZER = build_analyzer('sklearn', stop_words=True, lowercase=False)
txtclean = TextPreprocessing()


def preprocess_clean_text(raw_text):
    """Preprocessing source data"""
    # lower case
    words = raw_text.lower()

    # keep only words
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    letters_only_text = regex.sub(' ', words)

    # remove whitespaces
    remove_whitespaces = letters_only_text.strip()

    # remove korean
    # remove_korean = re.sub("[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+", " ", remove_whitespaces)
    # remove_number = re.sub("^\d$", " ", remove_korean)

    # remove number
    # remove_number = re.sub("^\d$", " ", remove_whitespaces)

    tokens = ' '.join(remove_whitespaces)
    meaningful_words = [i for i in tokens if i not in tokens]

    cleaned_word_list = ' '.join(meaningful_words)
    return cleaned_word_list

def tokenize_by_morpheme_char(s):
    r = ' '.join(DEFAULT_ANALYZER(str(s).strip()))
    r = ' '.join(DEFAULT_ANALYZER(preprocess_clean_text(r)))
    # r = ' '.join(DEFAULT_ANALYZER(txtclean.lemmatize_raw_text(txtclean.preprocess_raw_text(r))))
    r = mecab.morphs(r)
    return r
    # s = DEFAULT_ANALYZER(str(s).strip())
    # return s

def tokenize_by_morpheme_sentence(s):
    o = s
    r = ' '.join(DEFAULT_ANALYZER(str(s)))
    r = ' '.join(DEFAULT_ANALYZER(preprocess_clean_text(r)))
    # r = ' '.join(DEFAULT_ANALYZER(txtclean.lemmatize_raw_text(txtclean.preprocess_raw_text(r))))
    r = ' '.join(mecab.morphs(r))
    r = r + ' ' + o + ' ' + ' '.join(mecab.nouns(o))
    return r

def tokenize_by_morpheme_jaso(s):
    return [to_jaso(token) for token in tokenize_by_morpheme_char(str(s))]


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

def get_configset(directory, file, collection=None):
    try:
        configset = bios.read(directory + os.sep + file, file_type='yaml')
        if configset:
            if collection and collection != 'ALL':
                rt = configset.get(collection, None)
            else:
                rt = configset
        else:
            rt = {'error': 'There is no configset. Set collection.yml on /configset directory'}
    except Exception as e:
        rt = {'error': str(e)}
        log.error(rt)
        return rt
    return rt

def check_key_in_columns(fq, column):
    
    return
def dicfilter(key, solr_kwargs, collection, default):
    return solr_kwargs.get(key, collection.get(key, default))


def one_edit_apart(s1,s2):
    """
    print(one_edit_apart('cat', 'dog'))
    print(one_edit_apart('cat', 'cats'))
    print(one_edit_apart('cat', 'cut'))
    print(one_edit_apart('cat', 'cast'))
    print(one_edit_apart('cat', 'at'))
    print(one_edit_apart('cat', 'acts'))
    print(one_edit_apart('휴대픈', '휴대폰'))
    print(one_edit_apart('g대폰', '휴대폰'))
    print(one_edit_apart('흐대폰', '휴대폰을'))
    print(one_edit_apart('휴대', '휴디'))
    print(one_edit_apart('후대', '휴대'))
    print(one_edit_apart('휴대', '휴대폰'))
    print(one_edit_apart('휴대폰', '휴대폰을'))
    :param s1:
    :param s2:
    :return:
    """
    if len(s1) < len(s2):
        for x in range(len(s2)):
            if s2[:x]+s2[x+1:] == s1:
                return True
    elif len(s1) == len(s2):
        for x in range(len(s1)):
            if s1[x] != s2[x] and s1[:x]+s1[x+1:] == s2[:x]+s2[x+1:]:
                return True
    else:
        for x in range(len(s1)):
            if s1[:x] + s1[x+1:] == s2:
                return True
    return False


def get_one_edit_apart_words(wordlist, q):
    ls = list(map(lambda x: str(x) if one_edit_apart(x, q) else None, wordlist))
    rs = list(filter(None, ls))
    return rs


def get_jamo_levenshtein_words(voca_ls, q):
    min_voca = None
    min_score = None
    try:
        s = timeit.default_timer()
        voca_l = list(map(lambda x: (jamo_levenshtein(x, q), x), voca_ls))
        leven_score_l = list(map(lambda x: jamo_levenshtein(x, q), voca_ls))
        if leven_score_l:
            min_word_t = voca_l[leven_score_l.index(min(leven_score_l))]
            min_voca = min_word_t[1]
            min_score = min_word_t[0]
    except Exception as e:
        log.error({'error': str(e)})

    ttime = timeit.default_timer() - s
    log.debug('min_voca:%s, min_score:%s' % (min_voca, min_score))
    log.debug('get_jamo_levenshtein_words ttime:%s' % ttime)
    return min_voca, min_score


def jamo_sentence(sent):
    def transform(char):
        if char == ' ':
            return char
        cjj = decompose(char)
        if len(cjj) == 1:
            return cjj
        cjj_ = ''.join(c if c != ' ' else '-' for c in cjj)
        return cjj_

    sent_ = []
    for char in sent:
        if character_is_korean(char):
            sent_.append(transform(char))
        else:
            sent_.append(char)
    sent_ = re.compile('\s+').sub(' ', ''.join(sent_))
    return sent_


def jamo_to_word(jamo):
    jamo_list, idx = [], 0
    while idx < len(jamo):
        if not character_is_korean(jamo[idx]):
            jamo_list.append(jamo[idx])
            idx += 1
        else:
            jamo_list.append(jamo[idx:idx + 3])
            idx += 3
    word = ""
    for jamo_char in jamo_list:
        if len(jamo_char) == 1:
            word += jamo_char
        elif jamo_char[2] == "-":
            word += compose(jamo_char[0], jamo_char[1], " ")
        else: word += compose(jamo_char[0], jamo_char[1], jamo_char[2])
    return word


def transform(list):
    return [(jamo_to_word(w), r) for (w, r) in list]


def q2morph(q):
    pos = mecab.pos(q.strip())
    nouns = mecab.nouns(q.strip())
    morphs = mecab.morphs(q.strip())
    return pos, nouns, morphs


def q2propose(q):
    pos = mecab.pos(q.strip())
    nouns = mecab.nouns(q.strip())
    morphs = mecab.morphs(q.strip())
    return pos, nouns, morphs

def find_and_cut(intext, cut_size, highlight_list):
    add_flg = False
    next_flg = True
    add_text = None
    if len(intext) >= cut_size:
        target_text = intext[:cut_size]
        r_text_l = target_text.split()
        del r_text_l[-1]
        target_text = ' '.join(r_text_l)
        remain_text = intext[len(target_text):]
    else:
        target_text = intext
        remain_text = ''

    for i in highlight_list:
        idx = target_text.find(i)
        if idx > 0:
            add_flg = True
            add_text = target_text
            break
    if len(remain_text) < 10:
        next_flg = False

    return add_flg, add_text, next_flg, remain_text


def highlight_list(h_text, h_word_list, h_tag_pre, h_tag_post, h_snippets, h_maxlength):
    h_words = list()
    highlighted_text = h_text
    snippets = list()
    if h_word_list:
        for h_word in h_word_list:
            replace_word = h_tag_pre + h_word + h_tag_post

            highlighted_text = highlighted_text.replace(h_word, replace_word)
            h_words.append(replace_word)
        remain_text = highlighted_text

        if len(highlighted_text) <= h_maxlength:
            snippets.append(highlighted_text)
            return snippets

        if h_words:
            cut_size = h_maxlength
            while len(snippets) < h_snippets:
                add_flg, \
                add_text, \
                next_flg, \
                remain_text \
                    = find_and_cut(remain_text, cut_size, h_words)
                if add_flg:
                    snippets.append(add_text)
                if not next_flg:
                    break

    return snippets

import re


def add_komma_with_equal(s):
    fq_l = re.split('or|and ', s)
    for i in fq_l:
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


def fq_exp(fq_l):
    fq_expr_l = list()
    for fq in fq_l:
        fq = fq.replace('AND', ' and ')
        fq = fq.replace('OR', ' or ')

        # case fq = 'CL_HIERY_CH_CD:(I or T or P or W or QA)'
        if fq.count(':') == 1 and fq.count('(') == 1 \
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
        fq_expr_l.append(fq_expr)
    fq_expr = ' and '.join(fq_expr_l)
    return fq_expr

def highlight_q(q):
    nouns = mecab.nouns(q.strip())
    splitwords = q.strip().split()
    unionwords = list(set().union(nouns,splitwords))
    unionwords = list(set().union(unionwords,[q.strip()]))
    # unionwords.sort(key=len, reverse=True)
    unionwords.sort(key=len, reverse=False)
    return unionwords

h_text = """
7.2 문자열의 길이 구하기
문자열을 처리를 하다 보면 문자열의 길이가 필요한 경우가 많습니다. 이번에는 len 함수를 사용하여 문자열의 길이를 구해보겠습니다.

>>> hello = 'Hello, world!'
>>> len(hello)
13
len으로 'Hello, world!' 문자열이 들어있는 변수 hello의 길이를 구해보면 13이 나옵니다. 물론 len('Hello, world!')처럼 문자열을 바로 넣어도 됩니다.

여기서 문자열의 길이는 공백까지 포함합니다. 단, 문자열을 묶은 따옴표는 제외합니다. 이 따옴표는 문자열을 표현하는 문법일 뿐 문자열 길이에는 포함되지 않습니다(문자열 안에 포함된 작은 따옴표, 큰 따옴표는 포함됩니다).

한글 문자열의 길이도 len으로 구하면 됩니다.

>>> hello = '안녕하세요'
>>> len(hello)
5
'안녕하세요'가 5글자이므로 길이는 5가 나옵니다.

참고 | 문자열의 바이트 수 구하기
한글, 한자, 일본어 등은 UTF-8 인코딩으로 저장하는데 문자열이 차지하는 실제 바이트 수를 구하는 방법은 다음과 같습니다.

string_utf8_len.py
hello = '안녕하세요'
length = len(hello.encode('utf-8'))     # UTF-8로 인코딩 했을 때 바이트 수를 구함
print(length)
"""
h_tag_pre = '<span>'
h_tag_post = '</span>'
h_word_list = ['문', '경우', 'len', 'UTF-8']
h_snippets = 4
h_maxlength = 75

l = highlight_list(h_text, h_word_list, h_tag_pre, h_tag_post, h_snippets, h_maxlength)
print(l)
print(len(l))

if __name__ == "__main__":
    q = '인터넷폰 기가지니'
    h_q = highlight_q(q)
    # print(h_q)
    # import doctest
    # doctest.testmod()
