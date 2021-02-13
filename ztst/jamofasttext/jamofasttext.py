import util
from gensim.models import FastText
from gensim.models.word2vec import LineSentence

from tqdm import tqdm
import logging

# https://joyhong.tistory.com/137 임베딩 - FastText (한글 자소 분리)


# def process_jamo(tokenized_corpus_fname, output_fname):
#     toatal_lines = sum(1 for line in open(tokenized_corpus_fname, 'r', encoding='utf-8'))
#     with open(tokenized_corpus_fname, 'r', encoding='utf-8') as f1, \
#         open(output_fname, 'w', encoding='utf-8') as f2:
#         for _, line in tqdm(enumerate(f1), total=toatal_lines):
#             sentence = line.replace('\n', '').strip()
#             processed_sentence = util.jamo_sentence(sentence)
#             f2.writelines(processed_sentence + '\n')

# def process_jamo(tokenized_corpus_fname, output_fname):
#     with open(tokenized_corpus_fname, 'r', encoding='utf-8') as f1, \
#             open(output_fname, 'w', encoding='utf-8') as f2:
#         for line in f1:
#             sentence = line.replace('\n', '').strip()
#             processed_sentence = jamo_sentence(sentence)
#             f2.writelines(processed_sentence + '\n')

# tokenized_corpus_fname = 'corpus_mecab.txt'
# output_fname = 'corpus_mecab_jamo.txt'
# process_jamo(tokenized_corpus_fname, output_fname)


"""
Process Hangul Jamo Sentence.
Inspired By:
https://lovit.github.io/nlp/representation/2018/10/22/fasttext_subword
"""
import re
from soynlp.hangle import compose, decompose, character_is_korean

doublespace_pattern = re.compile('\s+')

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
    sent_ = doublespace_pattern.sub(' ', ''.join(sent_))
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


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
document = [
            '5g 휴대폰 플랜에 대해서 설명해주세요',
            'KT',
            '하나님 예배를 하자',
            ]


processed_document = list(map(lambda x: jamo_sentence(x), document))

model_fname = 'model_fasttext'
print('corpus 생성')
# corpus = [sent.strip().split(" ") for sent in tqdm(processed_document)]
corpus = [s.split() for s in processed_document]



# print("학습 중")
# # model = FastText(corpus, size=100, workers=4, sg=1, iter=2, word_ngrams=5)
# model = FastText(corpus, size=100, workers=4, sg=1, iter=2, word_ngrams=5, min_count=1)
# model.save('model_fasttext')
#
# print(f"학습 소요 시간 : {model.total_train_time}")
# # https://projector.tensorflow.org/ 에서 시각화 하기 위해 따로 저장
# model.wv.save_word2vec_format(model_fname + "_vis")
# print('완료')



def transform(list):
    return [(jamo_to_word(w), r) for (w, r) in list]

# 모델을 로딩하여 가장 유사한 단어를 출력
loaded_model = FastText.load(model_fname)
print(loaded_model.wv.vectors.shape)

print(transform(loaded_model.wv.most_similar(jamo_sentence('후대폰'), topn=5)))
print(transform(loaded_model.wv.most_similar(jamo_sentence('예베를'), topn=5)))
print(transform(loaded_model.wv.most_similar(jamo_sentence('KT'), topn=5)))
