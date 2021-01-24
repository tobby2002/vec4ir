### 전처리 코드
# https://omicro03.medium.com/%EC%9E%90%EC%97%B0%EC%96%B4%EC%B2%98%EB%A6%AC-nlp-15%EC%9D%BC%EC%B0%A8-fasttext-2b1aca6b3b56
# https://github.com/nltk/nltk_data download nltk

import re
# from lxml import etree
# import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
# targetXML = open('./ted_en-20160408.xml', 'r', encoding='UTF8')
# target_text = etree.parse(targetXML)
# parse_text = '\n'.join(target_text.xpath('//content/text()'))
# xml 파일로부터 <content>와 </content> 사이의 내용만 가져온다.

parse_text = '# 정규 표현식의 5g sub 모듈을 통해 content 중간에 등장하는 (Audio), (Laughter) 등의 배경음 부분을 제거.'

content_text = re.sub(r'\([^)]*\)', '', parse_text)
# 정규 표현식의 sub 모듈을 통해 content 중간에 등장하는 (Audio), (Laughter) 등의 배경음 부분을 제거.
sent_text = sent_tokenize(content_text)
# 입력 코퍼스에 대해서 NLTK를 이용하여 문장 토큰화를 수행한다.
normalized_text = []
for string in sent_text:
    tokens = re.sub(r"[^a-z0-9]+", " ", string.lower())
    normalized_text.append(tokens)
result = []
result = [word_tokenize(sentence) for sentence in normalized_text]
### FastText 학습
from gensim.models import FastText
ft_model = FastText(result, size=100, window=5, min_count=5, workers=4, sg=1)

fx = ft_model.predict('정규')
print(fx)