import os, sys
import gensim
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config
from utils import dbmanager, logmanager, dirmanager, utilmanager

class ModelManager():

    def __init__(self):
        print('ModelManager init')
        self.logger = logmanager.logger('model', 'modelmanager')
        self.irmodel = None

    def make_irmodels(self):
        self.logger.info('start make_model')
        gbook_df = pd.read_sql_table('api_googlebook', dbmanager.get_connect_engine())
        gbook_df_title = gbook_df['title']
        DEFAULT_ANALYZER = utilmanager.build_analyzer('sklearn', stop_words=False, lowercase=True)
        gbook_df_title = gbook_df_title.apply(lambda x: DEFAULT_ANALYZER(x))

        title_docs = gbook_df_title.values.tolist()
        model = gensim.models.Word2Vec(title_docs, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
        model.train(title_docs, total_examples=len(title_docs), epochs=config.MODEL_EPOCHS)

        # control directory
        dir = PROJECT_ROOT + config.MODEL_IR_PATH
        dirmanager.dir_manager(dir)
        lastestdir = dirmanager._get_latest_timestamp_dir(dir)
        print('lastestdir:%s' % lastestdir)

        model.save(lastestdir + 'w2v_title_model')
        w2v_title = gensim.models.Word2Vec.load(lastestdir + 'w2v_title_model')

        rs_similar = w2v_title.most_similar('song')
        self.logger.info(rs_similar)
        print(rs_similar)

        gbook_df_authors = gbook_df['authors']
        gbook_df_authors = gbook_df_authors.apply(lambda x: DEFAULT_ANALYZER(x))
        authors_docs = gbook_df_authors.values.tolist()
        model = gensim.models.Word2Vec(authors_docs, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
        model.train(authors_docs, total_examples=len(authors_docs), epochs=config.MODEL_EPOCHS)

        model.save(lastestdir + 'w2v_authors_model')
        w2v_authors = gensim.models.Word2Vec.load(lastestdir + 'w2v_authors_model')

        rs_similar = w2v_authors.most_similar('john')
        self.logger.info(rs_similar)
        print(rs_similar)
        self.logger.info('end makemodel')
        self.irmodel = {'w2v_title': w2v_title, 'w2v_authors': w2v_authors}

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

def main():
    mm = ModelManager()
    mm.make_irmodels()
    mm.qtfidf()

if __name__ == "__main__":
    main()
