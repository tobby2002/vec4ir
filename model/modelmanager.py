import os, sys
import gensim
import pandas as pd
from ir.utils import build_analyzer
from utils import dbmanager, logmanager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

def makemodel():
    logger = logmanager.logger('model', 'modelmanager')
    logger.info('start makemodel')
    gbook_df = pd.read_sql_table('api_googlebook', dbmanager.get_connect_engine())

    gbook_df_title = gbook_df['title']
    DEFAULT_ANALYZER = build_analyzer('sklearn', stop_words=False, lowercase=True)
    gbook_df_title = gbook_df_title.apply(lambda x: DEFAULT_ANALYZER(x))

    title_docs = gbook_df_title.values.tolist()
    model = gensim.models.Word2Vec(title_docs, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
    model.train(title_docs, total_examples=len(title_docs), epochs=config.MODEL_EPOCHS)
    model.save('w2v_title_model')
    model.wv.save_word2vec_format(fname='w2v_title_vector.bin', binary=False)
    w2v = gensim.models.Word2Vec.load(PROJECT_ROOT + config.MODEL_W2V_PATH + 'w2v_title_model')
    # w2v = gensim.models.Word2Vec.load(PROJECT_ROOT + config.MODEL_W2V_PATH + 'w2v_title_vector.bin')
    rs_similar = w2v.most_similar('song')
    print(rs_similar)

    gbook_df_authors = gbook_df['authors']
    gbook_df_authors = gbook_df_authors.apply(lambda x: DEFAULT_ANALYZER(x))
    authors_docs = gbook_df_authors.values.tolist()
    model = gensim.models.Word2Vec(authors_docs, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
    model.train(authors_docs, total_examples=len(authors_docs), epochs=config.MODEL_EPOCHS)
    model.save('w2v_authors_model')
    model.wv.save_word2vec_format(fname='w2v_authors_vector.bin', binary=False)
    w2v = gensim.models.Word2Vec.load(PROJECT_ROOT + config.MODEL_W2V_PATH + 'w2v_authors_model')

    rs_similar = w2v.most_similar('john')
    print(rs_similar)
    logger.info('end makemodel')

makemodel()
