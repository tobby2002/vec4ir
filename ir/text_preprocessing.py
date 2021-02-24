#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk
# nltk.download()
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import string
from konlpy.tag import Mecab
mecab = Mecab()

class TextPreprocessing:

    def preprocess_raw_text(self, raw_text):
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
        remove_number = re.sub("^\d$", " ", remove_whitespaces)

        # remove stopwords
        stopword_set = set(stopwords.words("english"))
        tokens = word_tokenize(remove_number)
        tokens = ' '.join(remove_number)
        meaningful_words = [i for i in tokens if i not in stopword_set]

        cleaned_word_list = ' '.join(meaningful_words)
        return cleaned_word_list

    def lemmatize_raw_text(self, raw_text):
        """using lemmatisation"""
        lemmatizer = WordNetLemmatizer()
        input_str = word_tokenize(raw_text)
        input_str = ' '.join(raw_text)
        tokens = [lemmatizer.lemmatize(word) for word in input_str]
        cleaned_word_list = ' '.join(tokens)
        return cleaned_word_list

    def stem_raw_text(self, raw_text):
        """using stemming"""
        stemmer = PorterStemmer()
        input_str = word_tokenize(raw_text)
        input_str = ' '.join(raw_text)
        tokens = [stemmer.stem(item) for item in input_str]
        cleaned_word_list = ' '.join(tokens)
        return cleaned_word_list

    # =======================================================
    # 형태소(POS)가 명사,동사,알파벳,숫자에 해당되는 단어 추출
    # 정규화(normalization) 어간추출(stemming) 처리
    # =======================================================
    def tokenizer(raw_texts, pos=["Noun","Alpha","Verb","Number"], stopword=[]):
        p = mecab.pos(raw_texts,
                norm=True,   # 정규화(normalization)
                stem=True    # 어간추출(stemming)
                )
        o = [word for word, tag in p if len(word) > 1 and tag in pos and word not in stopword]
        return(o)