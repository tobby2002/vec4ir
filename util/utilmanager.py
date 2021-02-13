#!/usr/bin/env python3
# coding: utf-8
import os, sys
import re
import bios
import timeit
import numpy as np
from konlpy.tag import Mecab
from scipy.stats import rankdata
from collections import Counter
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from ir.text_preprocessing import TextPreprocessing
from soynlp.hangle import levenshtein
from soynlp.hangle import jamo_levenshtein
from soynlp.hangle import compose, decompose, character_is_korean

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
            'nltk': (word_tokenize, None)  # uses punctuation for GloVe models
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
mecab = Mecab()
txtclean = TextPreprocessing()


def tokenize_by_morpheme_char(s):
    s = ' '.join(DEFAULT_ANALYZER(str(s).strip()))
    s = ' '.join(DEFAULT_ANALYZER(txtclean.lemmatize_raw_text(txtclean.preprocess_raw_text(s))))
    s = mecab.morphs(s)
    return s
    # s = DEFAULT_ANALYZER(str(s).strip())
    # return s

def tokenize_by_morpheme_sentence(s):
    o = s
    r = ' '.join(DEFAULT_ANALYZER(str(s)))
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
        # print(configset)
        collections_l = configset.keys()
        # print(collections_l)
        # oj_knkeys = configset["oj_kn"].keys()
        # print(oj_knkeys)
        if configset:
            if collection:
                collection_d = configset.get(collection, None)
                rt = {
                    'configset': configset,
                    'collection': collection_d,
                }
            else:
                rt = {
                    'configset': configset,
                    'collection': None,
                }
        else:
            rt = {'error': 'There is no configset. Set collection.yml on configset'}
    except Exception as e:
        print('error: %s' % str(e))
        rt = {'error': str(e)}
        return rt
    print(rt)
    return rt


def dicfilter(key, solr_kwargs, collection, default):
    return solr_kwargs.get(key, collection.get(key, default))


def one_edit_apart(s1,s2):
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

# print(one_edit_apart('cat', 'dog'))
# print(one_edit_apart('cat', 'cats'))
# print(one_edit_apart('cat', 'cut'))
# print(one_edit_apart('cat', 'cast'))
# print(one_edit_apart('cat', 'at'))
# print(one_edit_apart('cat', 'acts'))
# print(one_edit_apart('휴대픈', '휴대폰'))
# print(one_edit_apart('g대폰', '휴대폰'))
# print(one_edit_apart('흐대폰', '휴대폰을'))
# print(one_edit_apart('휴대', '휴디'))
# print(one_edit_apart('후대', '휴대'))
# print(one_edit_apart('휴대', '휴대폰'))
# print(one_edit_apart('휴대폰', '휴대폰을'))

def get_one_edit_apart_words(wordlist, q):
    # s = timeit.default_timer()
    ls = list(map(lambda x: str(x) if one_edit_apart(x, q) else None, wordlist))
    rs = list(filter(None, ls))
    # ttime = timeit.default_timer() - s
    # print('get_similar_words ttime:%s' % ttime)
    # print('get_similar_words rs:%s' % rs)
    return rs

def get_jamo_levenshtein_words(voca_ls, q):
    min_voca = None
    min_score = None
    try:
        s = timeit.default_timer()
        voca_l = list(map(lambda x: (jamo_levenshtein(x, q), x), voca_ls))
        print('voca_l :%s' % voca_l)
        print('get_jamo_levenshtein_words ㅁ :%s' % q)
        leven_score_l = list(map(lambda x: jamo_levenshtein(x, q), voca_ls))
        if leven_score_l:
            min_word_t = voca_l[leven_score_l.index(min(leven_score_l))]
            min_voca = min_word_t[1]
            min_score = min_word_t[0]
    except Exception as e:
        print('get_jamo_levenshtein_words exception:%s' % e)
        print('voca_ls :%s' % voca_ls)
        print('q :%s' % q)

    ttime = timeit.default_timer() - s
    print('min_voca:%s, min_score:%s' % (min_voca, min_score))
    print('get_jamo_levenshtein_words ttime:%s' % ttime)
    return min_voca, min_score

# import re
# from soynlp.hangle import compose, decompose, character_is_korean
#
# doublespace_pattern = re.compile('\s+')

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
