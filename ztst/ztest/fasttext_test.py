### 전처리 코드
# https://omicro03.medium.com/%EC%9E%90%EC%97%B0%EC%96%B4%EC%B2%98%EB%A6%AC-nlp-15%EC%9D%BC%EC%B0%A8-fasttext-2b1aca6b3b56
# https://github.com/nltk/nltk_data download nltk

import re
import timeit
# from lxml import etree
# import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from konlpy.tag import Mecab
from util.utilmanager import build_analyzer, to_jaso, tokenize_by_morpheme_char, tokenize_by_morpheme_jaso, get_one_edit_apart_words
from ir.base import Tfidf

# def g2tfidf(docs, q):
#     s = timeit.default_timer()
#     tfidf = Tfidf()
#     tfidf.fit(docs)
#     result, score = tfidf.query(str(q), return_scores=True)
#     ttime = timeit.default_timer() - s
#     print('g2tfidf ttime: %s' % ttime)
#     print(g2tfidf)
#     print(result[0])
#     print(result, score)
#     if not result:
#         return None
#     return result[0]


mecab = Mecab()
morphs_l = mecab.morphs('영등포구청역에 있는 맛집 좀 알려주세요.')
morphs_txt = ' '.join(morphs_l)
# print('morphs_txt')
# print(morphs_txt)
# targetXML = open('./ted_en-20160408.xml', 'r', encoding='UTF8')
# target_text = etree.parse(targetXML)
# parse_text = '\n'.join(target_text.xpath('//content/text()'))
# xml 파일로부터 <content>와 </content> 사이의 내용만 가져온다.

parse_text = '# 정규 표현식의 5g sub 모듈을 통해 content 중간에 등장하는 (Audio), (Laughter) 등의 배경음 부분을 제거. 휴대폰을 찾아줘'

content_text = re.sub(r'\([^)]*\)', '', parse_text)
# 정규 표현식의 sub 모듈을 통해 content 중간에 등장하는 (Audio), (Laughter) 등의 배경음 부분을 제거.
sent_text = sent_tokenize(content_text)
# 입력 코퍼스에 대해서 NLTK를 이용하여 문장 토큰화를 수행한다.
normalized_text = []

# 글자단위 + nouns
for string in sent_text:
    # tokens = re.sub(r"[^a-z0-9]+", " ", string.lower())
    tokens = re.sub(r"[^a-z0-9|ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+", " ", string.lower())
    print('tokens')
    print(tokens)

    nouns = mecab.nouns(tokens)
    nouns_txt = ' '.join(nouns)
    print('nouns_txt')
    print(nouns_txt)

    morphs_l = mecab.morphs(tokens)
    morphs_txt = ' '.join(morphs_l)
    print('morphs_txt')
    print(morphs_txt)

    # normalized_text.append(tokens)
    normalized_text.append(tokens + ' ' + nouns_txt)

# # 글자단위 + 형태소 + nouns
# for string in sent_text:
#     # tokens = re.sub(r"[^a-z0-9]+", " ", string.lower())
#     tokens = re.sub(r"[^a-z0-9|ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+", " ", string.lower())
#     print('tokens')
#     print(tokens)
#
#     nouns = mecab.nouns(tokens)
#     nouns_txt = ' '.join(nouns)
#     print('nouns_txt')
#     print(nouns_txt)
#
#     morphs_l = mecab.morphs(tokens)
#     morphs_txt = ' '.join(morphs_l)
#     print('morphs_txt')
#     print(morphs_txt)
#
#     # normalized_text.append(tokens)
#     normalized_text.append(tokens + ' ' + nouns_txt + ' ' + morphs_txt)



# 글자+형태소+노멀라이즈 단위
# for string in sent_text:
#     # tokens = re.sub(r"[^a-z0-9]+", " ", string.lower())
#     tokens = re.sub(r"[^a-z0-9|ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+", " ", string.lower())
#     print('tokens')
#     print(tokens)
#     tokenize_morphem_char_l = tokenize_by_morpheme_char(tokens)
#
#     print('tokenize_morphem_char_l')
#     print(tokenize_morphem_char_l)
#     morphs_txt = ' '.join(tokenize_morphem_char_l)
#     print('morphs_txt')
#     print(morphs_txt)
#     normalized_text.append(morphs_txt)

# 자소단위
# for string in sent_text:
#     tokenize_morphem_char_l = tokenize_by_morpheme_jaso(string)
#     print('tokenize_morphem_char_l')
#     print(tokenize_morphem_char_l)
#     tokens = ' '.join(tokenize_morphem_char_l)
#     morphs_txt = ' '.join(mecab.morphs(tokens))
#     print('morphs_txt')
#     print(morphs_txt)
#     normalized_text.append(morphs_txt)
#     print('normalized_text')
#     print(normalized_text)


docs = []
docs = [word_tokenize(sentence) for sentence in normalized_text]
print('docs')
print(docs)



### FastText 학습
# https://radimrehurek.com/gensim/models/fasttext.html
from gensim.models import FastText, Word2Vec
# ft_model = FastText(docs, size=100, window=5, min_count=1, workers=4, sg=1)
# ft_model.save('ft.model')
# fx = load_ft_model.wv
print('allllllllllllllll')
# print(fx)


load_ft_model = FastText.load('ft.model')
fx = load_ft_model.wv.most_similar('5gg')
print("5gg")
print(fx)


s = timeit.default_timer()
q = '후대폰'
q_jaso = to_jaso(q)
fx = load_ft_model.wv.most_similar(q)
ttime = timeit.default_timer() - s
print('q=%s' % q)
print('q_jaso=%s' % q_jaso)
print('ttime:%s' % ttime)
print(fx)

s = timeit.default_timer()
q = '배경'
q_jaso = to_jaso(q)
fx = load_ft_model.wv.most_similar(q)
ttime = timeit.default_timer() - s
print('q=%s' % q)
print('q_jaso=%s' % q_jaso)
print('ttime:%s' % ttime)
print(fx)


s = timeit.default_timer()
q = '5g 후대폰에 대해서 알려줘'
mecab = Mecab()
q_morph_l = mecab.morphs(q)

q_jaso = to_jaso(q)
fx = load_ft_model.wv.most_similar(positive=q_morph_l, topn=30)

if fx:
    ls = list(map(lambda x: x[0], fx))

ttime = timeit.default_timer() - s
print('q=%s' % q)
print('q_jaso=%s' % q_jaso)
print('ttime:%s' % ttime)
print(fx)

similar_l = get_one_edit_apart_words(ls, q)




# w2v_model = Word2Vec(docs, size=100, window=5, min_count=1, workers=4, sg=1)
# wx = w2v_model.wv.most_similar('5gg')
# print(wx)
