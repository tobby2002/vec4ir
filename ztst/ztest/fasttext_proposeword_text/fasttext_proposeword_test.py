### 전처리 코드
# https://omicro03.medium.com/%EC%9E%90%EC%97%B0%EC%96%B4%EC%B2%98%EB%A6%AC-nlp-15%EC%9D%BC%EC%B0%A8-fasttext-2b1aca6b3b56
# https://github.com/nltk/nltk_data download nltk

import re
import timeit
# from lxml import etree
# import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from konlpy.tag import Mecab
from util.utilmanager import build_analyzer, to_jaso, tokenize_by_morpheme_char, \
    tokenize_by_morpheme_jaso, get_one_edit_apart_words, get_jamo_levenshtein_words
from ir.base import Tfidf
from ir.word2vec import WordCentroidDistance, FastTextCentroidDistance, WordMoversDistance, FastWordCentroidRetrieval, WordCentroidRetrieval
from ir.base import Matching, Tfidf
from ir.core import Retrieval
import logging
from gensim.models import FastText
from util.utilmanager import jamo_sentence, jamo_to_word, transform, tokenize_by_morpheme_char, tokenize_by_morpheme_sentence
from ir.utils import build_analyzer
from ir.query_expansion import CentroidExpansion, EmbeddedQueryExpansion
mecab = Mecab()
# morphs_l = mecab.morphs('abc cde 가 나 다 를 ')


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
document = [
            '5g 휴대폰 플랜에 대해서 설명해주세요',
            'KT',
            '하나님 예배를 하자',
            ]

# processed_document = list(map(lambda x: tokenize_by_morpheme_char(x), document))
# processed_document = [' '.join(s) for s in processed_document]
# processed_document = list(map(lambda x: jamo_sentence(x), processed_document))

processed_document = list(map(lambda x: tokenize_by_morpheme_sentence(x), document))
processed_document = list(map(lambda x: jamo_sentence(x), processed_document))

model_fname = 'ft.model'
print('corpus 생성')
# corpus = [sent.strip().split(" ") for sent in tqdm(processed_document)]
corpus = [s.split() for s in processed_document]

# print('========= 학습 ==========')
# print("학습 중")
# # model = FastText(corpus, size=100, workers=4, sg=1, iter=2, word_ngrams=5)
# model = FastText(corpus, size=100, workers=4, sg=1, iter=1, word_ngrams=5, min_count=1)
# model.save(model_fname)
# #unload unnecessary memory after training
# model.init_sims(replace=True)
#
# print(f"학습 소요 시간 : {model.total_train_time}")
# # https://projector.tensorflow.org/ 에서 시각화 하기 위해 따로 저장
# model.wv.save_word2vec_format(model_fname + "_vis")
# print('완료')


# print('========= 제안 검색어 ==========')
load_ft_model = FastText.load(model_fname)
print(load_ft_model.wv.vectors.shape)

vvoca_docs_d = load_ft_model.wv.vocab
vvoc_l = list(vvoca_docs_d.keys())
print('===== start ==== copus vocas ==========')
print('vvoc_l:%s' % vvoc_l)
print('===== end ==== copus vocas ==========')
q = jamo_sentence('후대폰 하니님 kt')

match_op = Matching()
wcd = WordCentroidDistance(load_ft_model.wv)

vvoc_retrieval = Retrieval(wcd, matching=match_op, labels=vvoc_l)
vvoc_retrieval.fit(vvoc_l)

print('========= voca 검색어 ==========')
vocas, score = vvoc_retrieval.query(q, return_scores=True)
print('vocas, score')
print(vocas, score)

print('========= docu 검색어 ==========')
jamo_document = list(map(lambda x: jamo_sentence(x), document))
docu_retrieval = Retrieval(wcd, matching=match_op, labels=document)
docu_retrieval.fit(jamo_document)
docus, score = docu_retrieval.query(q, return_scores=True)
print('docus, score')
print(docus, score)



# q = jamo_sentence('후대폰')
# # docs, score = retrieval.query(q, return_scores=True)
# # print('docs, score')
# # print(docs, score)
# # # wvvoc = wvvoc_l[docs[0]]





# q_jaso = to_jaso(q)
mecab = Mecab()
import asyncio


async def replace_noun(load_ft_model, noun, target):
    s0 = timeit.default_timer()
    fx = load_ft_model.wv.most_similar(noun, topn=5)
    if fx:
        ls = list(map(lambda x: jamo_to_word(x[0]), fx))
    similar_l = get_one_edit_apart_words(ls, jamo_to_word(noun))
    if similar_l:
        # q_new = q_new.replace(jamo_to_word(noun), similar_l[0])
        target.append((jamo_to_word(noun), similar_l[0]))
        # print('%s - q_new_replaced:%s' % (jamo_to_word(noun), q_new))

    ttime = timeit.default_timer() - s0
    # print('%s time:%s' % (noun, ttime))


# async def process_async_replace_noun(q_jamo_nouns_l, target):
#     s = timeit.default_timer()
#     async_exec_func_list = []
#     for jamo_noun in q_jamo_nouns_l:
#         # print('noun:%s' % jamo_noun)
#         jamo_v = vvoca_docs_d.get(jamo_noun, None)
#         # docs = retrieval.query(noun)
#         if not jamo_v:
#         #     print('jamo_v:%s' % jamo_v)
#         # else:
#             # async_exec_func_list.append(replace_noun(load_ft_model, noun, q, q_new))
#             async_exec_func_list.append(replace_noun(load_ft_model, jamo_noun, target))
#     await asyncio.wait(async_exec_func_list)
#     ttime = timeit.default_timer() - s
#     # print('process_async time:%s' % ttime)
#
#
# def get_q2propose(retrieval):
#     target = list()
#     s = timeit.default_timer()
#     q = '5g 후대폰 플랜에 대해서 알려줘'
#     q_jamo = jamo_sentence('5g 후대폰 플랜에 대해서 알려줘')
#     q_new = q
#     q_jamo_nouns_l = q_jamo.split()
#     asyncio.run(process_async_replace_noun(q_jamo_nouns_l, target))
#     for t in target:
#         q_new = q_new.replace(list(t)[0], list(t)[1])
#     ttime = timeit.default_timer() - s
#     print('get_q2propose ttime:%s' % ttime)
#     print('q_new')
#     print(q_new)
#     return q_new


# get_q2propose(retrieval)


# def get_q2propose_by_query(retrieval):
#     target = list()
#     s = timeit.default_timer()
#     # q = '5g 후대폰 플래에 대해서 알려줘'
#     q = '예배시 후대폰 끄자 교화에서'
#     q = '에배를 설명해 주세요'
#     morphs_l = mecab.morphs(q)
#     print('morphs_l:%s' % morphs_l)
#     nouns_l = mecab.nouns(q)
#     print('nouns_l:%s' % nouns_l)
#
#     q_jamo = jamo_sentence(q)
#     q_new = q
#     q_jamo_nouns_l = q_jamo.split()
#     for q_noun in q_jamo_nouns_l:
#         jamo_v = vvoca_docs_d.get(q_noun, None)
#         if not jamo_v:
#             words, score = retrieval.query(q_noun, return_scores=True)
#             print('words, score')
#             print(words, score)
#
#             if len(words):
#                 ls = list(map(lambda x: jamo_to_word(x), list(words)))
#             similar_l = get_one_edit_apart_words(ls, jamo_to_word(q_noun))
#             if similar_l:
#                 target.append((jamo_to_word(q_noun), similar_l[0]))
#
#     for t in target:
#         q_new = q_new.replace(list(t)[0], list(t)[1])
#     ttime = timeit.default_timer() - s
#     print('get_q2propose_by_query ttime:%s' % ttime)
#     print('q_new')
#     print(q_new)

# print('========= get_q2propose_by_query ==========')
# get_q2propose_by_query(retrieval)


async def a_query_func(retrieval, q_noun, target):
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
            voca_ls = []
            if len(vocas):
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


async def process_async_exec_list(retrieval, q_jamo_nouns_l, target):
    s = timeit.default_timer()
    async_exec_func_list = []
    for q_noun in q_jamo_nouns_l:
            async_exec_func_list.append(a_query_func(retrieval, q_noun, target))
    await asyncio.wait(async_exec_func_list)


def get_q2propose_multi_by_query(retrieval):
    target = list()
    s = timeit.default_timer()
    # # q = '5g 후대폰 플래에 대해서 알려줘'
    # q = '예배시 후대폰 끄자 교화에서'
    q = '5g의 후대폰 플렌에대해서 kt에서 에배를 설명해 주세요'
    morphs_l = mecab.morphs(q)
    print('morphs_l:%s' % morphs_l)
    nouns_l = mecab.nouns(q)
    print('nouns_l:%s' % nouns_l)

    q_jamo = jamo_sentence(q)
    q_new = q
    q_jamo_nouns_l = q_jamo.split()
    asyncio.run(process_async_exec_list(retrieval, q_jamo_nouns_l, target))

    for t in target:
        q_new = q_new.replace(list(t)[0], list(t)[1])
    ttime = timeit.default_timer() - s
    print('get_q2propose_by_query ttime:%s' % ttime)
    print('q_new')
    print(q_new)

# print('========= get_q2propose_multi_by_query ==========')
# get_q2propose_multi_by_query(retrieval)