import os, sys
import gensim
import pandas as pd
from ir.utils import build_analyzer
from utils import dbmanager, logmanager

# https://stackoverflow.com/questions/27488446/how-do-i-get-word-frequency-in-a-corpus-using-scikit-learn-countvectorizer
from sklearn.feature_extraction.text import CountVectorizer

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

class ModelManager():

    def __init__(self):
        print('ModelManager init')
        self.logger = logmanager.logger('model', 'modelmanager')

    def make_model(self):
        self.logger.info('start make_model')
        gbook_df = pd.read_sql_table('api_googlebook', dbmanager.get_connect_engine())
        gbook_df_title = gbook_df['title']
        DEFAULT_ANALYZER = build_analyzer('sklearn', stop_words=False, lowercase=True)
        gbook_df_title = gbook_df_title.apply(lambda x: DEFAULT_ANALYZER(x))

        title_docs = gbook_df_title.values.tolist()
        model = gensim.models.Word2Vec(title_docs, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
        model.train(title_docs, total_examples=len(title_docs), epochs=config.MODEL_EPOCHS)
        model.save('w2v_title_model')
        model.wv.save_word2vec_format(fname='w2v_title_vector.bin', binary=False)
        w2v_title = gensim.models.Word2Vec.load(PROJECT_ROOT + config.MODEL_W2V_PATH + 'w2v_title_model')
        # w2v_title = gensim.models.Word2Vec.load(PROJECT_ROOT + config.MODEL_W2V_PATH + 'w2v_title_vector.bin')
        rs_similar = w2v_title.most_similar('song')
        self.logger.info(rs_similar)
        print(rs_similar)

        gbook_df_authors = gbook_df['authors']
        gbook_df_authors = gbook_df_authors.apply(lambda x: DEFAULT_ANALYZER(x))
        authors_docs = gbook_df_authors.values.tolist()
        model = gensim.models.Word2Vec(authors_docs, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
        model.train(authors_docs, total_examples=len(authors_docs), epochs=config.MODEL_EPOCHS)
        model.save('w2v_authors_model')
        model.wv.save_word2vec_format(fname='w2v_authors_vector.bin', binary=False)
        w2v_authors = gensim.models.Word2Vec.load(PROJECT_ROOT + config.MODEL_W2V_PATH + 'w2v_authors_model')

        rs_similar = w2v_authors.most_similar('john')
        self.logger.info(rs_similar)
        print(rs_similar)
        self.logger.info('end makemodel')
        return w2v_title, w2v_authors

    def qcountvector(self):
        corpus = [
            'This is the first document.',
            'This document is the second document.',
            'And this is the third one.',
            'Is this the first document?',
        ]

        gbook_df = pd.read_sql_table('api_googlebook', dbmanager.get_connect_engine())
        gbook_df_title = gbook_df['title']
        DEFAULT_ANALYZER = build_analyzer('sklearn', stop_words=False, lowercase=True)
        gbook_df_title = gbook_df_title.apply(lambda x: ' '.join(DEFAULT_ANALYZER(x)))
        corpus = gbook_df_title.values.tolist()

        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(corpus)
        print(vectorizer.get_feature_names())
        # ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
        print(X.toarray())
        X_all_countvector = X.toarray()
        # [[0 1 1 1 0 0 1 0 1]
        #  [0 2 0 1 0 1 1 0 1]
        #  [1 0 0 1 1 0 1 1 1]
        #  [0 1 1 1 0 0 1 0 1]]
        print(X.toarray().sum(axis=0))
        # [1 4 2 4 1 1 4 1 4]
        X_sum_countvector = X.toarray().sum(axis=0)


    def qtfidf(self):
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.feature_extraction.text import TfidfTransformer
        from nltk.corpus import stopwords

        corpus = [
            'This is the first document.',
            'This document is the second document.',
            'And this is the third one.',
            'Is this the first document?',
        ]

        gbook_df = pd.read_sql_table('api_googlebook', dbmanager.get_connect_engine())
        gbook_df_title = gbook_df['title']
        DEFAULT_ANALYZER = build_analyzer('sklearn', stop_words=False, lowercase=True)
        gbook_df_title = gbook_df_title.apply(lambda x: ' '.join(DEFAULT_ANALYZER(x)))
        corpus = gbook_df_title.values.tolist()
        # train_set = ["The sky is blue.", "The sun is bright."] #Documents
        train_set = corpus #Documents
        stopWords = stopwords.words('english')
        vectorizer = CountVectorizer(stop_words=stopWords, lowercase=True)
        transformer = TfidfTransformer()
        trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()


        test_set = ["The sun in the sky is bright."] #Query
        # testVectorizerArray = vectorizer.transform(test_set).toarray()
        # print('Fit Vectorizer to train set', trainVectorizerArray)
        # print('Transform Vectorizer to test set', testVectorizerArray)
        #
        # transformer.fit(trainVectorizerArray)
        # print(transformer.transform(trainVectorizerArray).toarray())
        #
        # transformer.fit(testVectorizerArray)
        #
        # tfidf = transformer.transform(testVectorizerArray)
        # print(tfidf.todense())

        self.get_tfidfdense(vectorizer, trainVectorizerArray, transformer, test_set)

    def get_tfidfdense(self, vectorizer, trainVectorizerArray, transformer, test_set):
        testVectorizerArray = vectorizer.transform(test_set).toarray()
        print('Fit Vectorizer to train set', trainVectorizerArray)
        print('Transform Vectorizer to test set', testVectorizerArray)

        transformer.fit(trainVectorizerArray)
        print(transformer.transform(trainVectorizerArray).toarray())

        transformer.fit(testVectorizerArray)

        tfidf = transformer.transform(testVectorizerArray)

        tfidfdense = tfidf.todense()
        print('tfidf dense:', tfidfdense)

        tfidfdense_pure = tfidfdense[0]
        print('tfidf tfidfdense_pure:', tfidfdense_pure)

        sum_tfidfdense_pure = sum(tfidfdense_pure)
        print('tfidf sum(tfidfdense_pure):', sum_tfidfdense_pure)

        print('tfidf_pure sum mean:', sum(tfidfdense_pure)/len(tfidfdense_pure))



if __name__ == "__main__":
        mm = ModelManager()
        # mm.make_model()
        #
        # mm.qcountvector()

        mm.qtfidf()


