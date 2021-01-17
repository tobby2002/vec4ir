import os, sys
import gensim
import pandas as pd
from ir.base import Matching, Tfidf
from ir.core import Retrieval
from ir.utils import build_analyzer
from ir.word2vec import WordCentroidDistance, WordMoversDistance
from gensim.models import Word2Vec, Doc2Vec

import config
from util import dbmanager, logmanager, dirmanager, utilmanager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

class ModelManager():

    def __init__(self):
        print('ModelManager init')
        self.logger = logmanager.logger('model', 'modelmanager')
        self.logger.info('ModelLoadManager init started')
        self.timeinstance = None
        self.irmodel_dic = None
        self.irmodel = None

    def make_irmodels(self):
        self.logger.info('start make_model')
        dirmanager.dir_manager(PROJECT_ROOT + config.MODEL_IR_PATH)
        lastestdir  = dirmanager._get_latest_timestamp_dir(PROJECT_ROOT + config.MODEL_IR_PATH)


        tb_df = pd.read_sql_table('product_product', dbmanager.get_connect_engine_p())
        tb_df_name = tb_df['name']
        DEFAULT_ANALYZER = utilmanager.build_analyzer('sklearn', stop_words=False, lowercase=True)
        tb_df_name = tb_df_name.apply(lambda x: DEFAULT_ANALYZER(x))

        # train model
        tb_df_name_docs = tb_df_name.values.tolist()
        model = gensim.models.Word2Vec(tb_df_name_docs, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
        model.train(tb_df_name_docs, total_examples=len(tb_df_name_docs), epochs=config.MODEL_EPOCHS)

        # save model
        dir = PROJECT_ROOT + config.MODEL_IR_PATH
        dirmanager.dir_manager(dir)
        lastestdir = dirmanager._get_latest_timestamp_dir(dir)
        model.save(lastestdir + 'w2v_product_product_name')

        # load model
        w2v_product_product_name = gensim.models.Word2Vec.load(lastestdir + 'w2v_product_product_name')
        self.logger.info('end makemodel')
        self.irmodel = {'w2v_product_product_name': w2v_product_product_name}

    def get_irmodels(self):
        return self.irmodel

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
        DEFAULT_ANALYZER = utilmanager.build_analyzer('sklearn', stop_words=False, lowercase=True)
        gbook_df_title = gbook_df_title.apply(lambda x: ' '.join(DEFAULT_ANALYZER(x)))
        corpus = gbook_df_title.values.tolist()
        # train_set = ["The sky is blue.", "The sun is bright."] #Documents
        train_set = corpus #Documents
        stopWords = stopwords.words('english')
        vectorizer = CountVectorizer(stop_words=stopWords, lowercase=True)
        transformer = TfidfTransformer()
        trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()
        test_set = ["The sun in the sky is bright."] #Query

    def q_word2vec(self):
        ir_models = self.get_irmodels()
        match_op = Matching()
        wcd = WordCentroidDistance(ir_models.wv)
        retrieval = Retrieval(wcd, matching=match_op)

        retrieval.fit(documents)
        result = retrieval.query('art news')
        print(result)

        retrieval1 = Retrieval(wcd, matching=match_op, labels=['1번', '2번', '3번', '4번', '5번', '6번'])
        retrieval1.fit(documents)
        result1 = retrieval1.query('art news')
        print(result1)

    def get_preprocessed_data_df(self, conn, table, column):
        tb_df = pd.read_sql_table(table, conn)
        DEFAULT_ANALYZER = build_analyzer('sklearn', stop_words=False, lowercase=True)
        tb_df = tb_df[column].apply(lambda x: DEFAULT_ANALYZER(x))
        return tb_df

    def tb_docs(self):
        return None

def main():
    mm = ModelManager()
    mm.make_irmodels()
    mm.qtfidf()

if __name__ == "__main__":
    main()

