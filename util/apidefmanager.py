import os, sys, timeit
import urllib.request
import asyncio
try:
    from konlpy.tag import Mecab
    mecab = Mecab()
except Exception as e:
    import mecab
    mecab = mecab.MeCab()

from util.utilmanager import build_analyzer, to_jaso, tokenize_by_morpheme_char, \
    tokenize_by_morpheme_jaso, get_one_edit_apart_words, get_jamo_levenshtein_words
from ir.base import Tfidf
from ir.word2vec import WordCentroidDistance, FastTextCentroidDistance, WordMoversDistance, FastWordCentroidRetrieval, WordCentroidRetrieval
from ir.base import Matching, Tfidf
from ir.core import Retrieval
import logging
from gensim.models import FastText
from util.utilmanager import jamo_sentence, jamo_to_word, get_configset, dfconcat
from ir.irmanager import IrManager
from gensim.models import Word2Vec, FastText

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


async def a_query_func(retrieval, vvoca_docs_d, q_noun, target):
    s0 = timeit.default_timer()
    try:
        jamo_v = vvoca_docs_d.get(q_noun, None)
        print('===================================================')
        print('========= start q_noun:%s ==========' % jamo_to_word(q_noun))
        print('#### start q_noun:%s #####' % q_noun)
        if not jamo_v:
            vocas, score = retrieval.query(q_noun, return_scores=True, k=10)
            print('vocas, score')
            print(vocas, score)
            # voca_ls = []
            if vocas.any():
                voca_ls = list(map(lambda x: jamo_to_word(x), list(vocas)))
                print('voca_ls:%s' % voca_ls)
                one_edit_apart_similar_l = get_one_edit_apart_words(voca_ls, jamo_to_word(q_noun))
                print('1.similar_l:%s' % one_edit_apart_similar_l)

                leven_min_voca, leven_min_score = get_jamo_levenshtein_words(voca_ls, jamo_to_word(q_noun))
                print('2.leven_min_voca:%s' % leven_min_voca)

                jamo_leven_morphs_l = mecab.morphs(leven_min_voca)
                print('3. jamo_leven_morphs_l:%s' % jamo_leven_morphs_l)
                q_word_morphs_l = mecab.morphs(jamo_to_word(q_noun))
                print('4. q_word_morphs_l:%s' % q_word_morphs_l)

                vocas_intersec = list(set(jamo_leven_morphs_l) & set(q_word_morphs_l))
                voca_intersec = ' '.join(vocas_intersec)
                print('5. voca_intersec:%s' % voca_intersec)
                rtvoca = None
                if one_edit_apart_similar_l and leven_min_voca:
                    if one_edit_apart_similar_l[0] == leven_min_voca:
                        if len(leven_min_voca) >= len(jamo_to_word(q_noun)):
                            print('-------- q_noun:%s --> %s' % (q_noun, leven_min_voca))
                            rtvoca = leven_min_voca
                            target.append((jamo_to_word(q_noun), rtvoca))
                            print('#### end q_noun:%s || %s #####' % (q_noun, rtvoca))
                            print('========= end q_noun:%s || %s ==== end ======' % (q_noun, rtvoca))
                            print('===================================================')
                            return
            print('========= end q_noun:%s || %s ==== end ======' % (q_noun, rtvoca))
            print('===================================================')
    except Exception as e:
        print('a_query_func q_noun(%s) exception:%s' % (q_noun, e))
    ttime = timeit.default_timer() - s0
    print('%s time:%s' % (q_noun, ttime))


async def process_async_exec_list(retrieval, vvoca_docs_d, q_jamo_nouns_l, target):
    s = timeit.default_timer()
    async_exec_func_list = []
    for q_noun in q_jamo_nouns_l:
            async_exec_func_list.append(a_query_func(retrieval, vvoca_docs_d, q_noun, target))
    await asyncio.wait(async_exec_func_list)


def get_q2propose_multi_by_query(q, retrieval, vvoca_docs_d):
    target = list()
    s = timeit.default_timer()
    # # q = '5g 후대폰 플래에 대해서 알려줘'
    # q = '예배시 후대폰 끄자 교화에서'
    # q = '5g 후대폰 하누님 예베를 설명해주시요'
    # morphs_l = mecab.morphs(q)
    # print('morphs_l:%s' % morphs_l)
    # nouns_l = mecab.nouns(q)
    # print('nouns_l:%s' % nouns_l)

    q_jamo = jamo_sentence(q)
    q_new = q
    q_jamo_nouns_l = q_jamo.split()
    asyncio.run(process_async_exec_list(retrieval, vvoca_docs_d, q_jamo_nouns_l, target))

    for t in target:
        q_new = q_new.replace(list(t)[0], list(t)[1])
    ttime = timeit.default_timer() - s
    print('get_q2propose_by_query ttime:%s' % ttime)
    print('q_new')
    print(q_new)
    return q_new


def get_glossary_db(conn):
    irm_ = IrManager()
    configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
    # tb_df_ = irm_.get_tb_df_by_collection(collection, configset_)


def get_q2propose_replace_db(q, conn):
    target = list()
    s = timeit.default_timer()
    # # q = '5g 후대폰 플래에 대해서 알려줘'
    # q = '예배시 후대폰 끄자 교화에서'
    # q = '5g 후대폰 하누님 예베를 설명해주시요'
    # morphs_l = mecab.morphs(q)
    # print('morphs_l:%s' % morphs_l)
    # nouns_l = mecab.nouns(q)
    # print('nouns_l:%s' % nouns_l)

    q_new = q

    for t in target:
        q_new = q_new.replace(list(t)[0], list(t)[1])
    ttime = timeit.default_timer() - s
    print('get_q2propose_by_query ttime:%s' % ttime)
    print('q_new')
    print(q_new)
    return q_new