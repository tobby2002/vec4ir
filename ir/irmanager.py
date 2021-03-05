import os, sys, time, timeit
import pandas as pd
import numpy as np
import asyncio
import multiprocessing
from benedict import benedict
from ir.base import Matching, Tfidf
from ir.core import Retrieval
from ir.utils import build_analyzer
from ir.word2vec import WordCentroidDistance
from util.dirmanager import _get_latest_timestamp_dir, dir_manager, _make_timestamp_dir
from util.dbmanager import get_connect_engine_wi
from util.utilmanager import build_analyzer, dicfilter, tokenize_by_morpheme_char, \
    jamo_sentence, tokenize_by_morpheme_sentence, jamo_to_word, highlight_list, fq_exp
from ir.query_expansion import EmbeddedQueryExpansion
from tqdm import tqdm
from gensim.models import Word2Vec, FastText, Doc2Vec
from util.logmanager import logz

log = logz()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

# jamo process
# https://joyhong.tistory.com/137
class IrManager:

    def __init__(self):
        pass

    def get_tb_df(self, table=None, pklsave=False):
        conn = None
        engine = None
        try:
            conn, engine = get_connect_engine_wi()
            if not pklsave:
                tb_df = self.get_analyzered_data_df(conn=conn, table=table, columns=None, analyzer_flag=False)
            else:
                dir = PROJECT_ROOT + config.MODEL_IR_PATH
                lastestdir = _get_latest_timestamp_dir(dir)
                if not lastestdir:
                    tb_df_table = self.get_analyzered_data_df(conn=conn, table=table, columns=None, analyzer_flag=False)
                    self.save_df2pickle(lastestdir, tb_df_table, '', table)
                    tb_df_table_loaded = self.load_pickle2df(lastestdir, '', table)
                    # print(tb_df_table_loaded.head(5))
                    tb_df = tb_df_table_loaded
        except UnboundLocalError as e:
            err = {'error': 'error in get_tb_df:%s' % str(e)}
            log.error(err)
            return err
        except Exception as e:
            err = {'error': 'error in get_tb_df:%s' % str(e)}
            log.error(err)
            return err
        finally:
            if conn is not None:
                conn.close()
            if engine is not None:
                engine.dispose()
        return tb_df

    def get_tb_df_by_collection(self, coll_key, configset, pklsave=False):
        conn = None
        engine = None
        rt_tb_df = benedict(dict())
        try:
            conn, engine = get_connect_engine_wi()
            if coll_key:
                coll_keys = [coll_key]
            else:
                coll_keys = configset.keys()
            for ckey in coll_keys:

                table = configset.get(ckey, None)['table']
                if table:
                    columns = configset.get(ckey, None)['columns']
                    # dfields = configset.get(ckey, None)['df']
                    if not pklsave:
                        rt_tb_df[ckey+'.'+table] = self.get_analyzered_data_df(conn=conn, table=table, columns=columns, analyzer_flag=False)
                    else:
                        dir = PROJECT_ROOT + config.MODEL_IR_PATH
                        lastestdir = _get_latest_timestamp_dir(dir)
                        if not lastestdir:
                            tb_df_table = self.get_analyzered_data_df(conn=conn, table=table, columns=columns, analyzer_flag=False)
                            self.save_df2pickle(lastestdir, tb_df_table, ckey, table)
                            tb_df_table_loaded = self.load_pickle2df(lastestdir, ckey, table)
                            rt_tb_df[ckey+'.'+table] = tb_df_table_loaded
        except UnboundLocalError as e:
            err = {'error': 'error in get_tb_df_by_collection:%s' % str(e)}
            log.error(err)
            return err
        except Exception as e:
            err = {'error': 'error in get_tb_df_by_collection:%s' % str(e)}
            log.error(err)
            return err
        finally:
            if conn is not None:
                conn.close()
            if engine is not None:
                engine.dispose()
        return rt_tb_df


    def set_init_models_and_get_retrievals(self, mode, modeltype, table, docid, columns, tb_df, onlymodel=False):
        """save and load query results"""
        log.info('set_init_models_and_get_retrievals')
        retrievals = {}
        tb_df_id = tb_df[docid]
        tb_df_columns_doc = tb_df[columns]
        if modeltype:
            for mtype in modeltype:
                # loaded_model = self.load_models(mtype, table, columns)
                loaded_model = self.aync_load_models(mtype, table, columns)
                if not onlymodel:
                    retrieval = self.get_retrievals(mode=mode, models=loaded_model, columns=columns, tb_df_doc=tb_df_columns_doc, labels=tb_df_id.values.tolist())
                    retrievals[mtype.__name__.lower()] = retrieval
        else:
            log.info('There is no model type!! check modeltype, e.g. Word2Vec, FastText.')
        return retrievals, loaded_model


    # def get_docs_load_df_by_column(self, conn, table, column):
    #     cur = conn.cursor()
    #     cur.execute('select * from %s' % table)
    #     cols = [column[0] for column in cur.description]
    #     query_df = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)
    #     print(query_df.memory_usage())
    #     docs_list = query_df[column].values.tolist()
    #     return docs_list

    def get_fit_retrieval(self, mode, model, documents, labels):
        analyzered_documents = list(map(lambda x: jamo_sentence(x), documents))
        if mode == 'wcd':
            match_op = Matching()
            wcd = WordCentroidDistance(model.wv)
            retrieval = Retrieval(wcd, matching=match_op, labels=labels)
            retrieval.fit(analyzered_documents)
        elif mode == 'tfidf':
            retrieval = Tfidf()
            retrieval.fit(documents)
        elif mode == 'expansion':
            n_expansions = 2
            tfidf = Tfidf()
            match_op = Matching()
            expansion_op = EmbeddedQueryExpansion(model.wv, m=n_expansions)
            retrieval = Retrieval(tfidf,  # The retrieval model
                                  matching=match_op,
                                  query_expansion=expansion_op, labels=labels)
            retrieval.fit(analyzered_documents)
        elif mode == 'combination':
            wcd = WordCentroidDistance(model.wv)
            tfidf = Tfidf()
            wcd.fit(analyzered_documents)
            # # they can operate on different feilds
            tfidf.fit(analyzered_documents)
            match_op = Matching().fit(analyzered_documents)
            combined = wcd + tfidf ** 2
            retrieval = Retrieval(combined, matching=match_op, labels=labels)
        return retrieval

    def get_analyzered_data_df(self, conn=None, table=None, columns=None, analyzer_flag=False):
        """get data dataframe"""
        if analyzer_flag:
            analyzer = build_analyzer('sklearn', stop_words=True, lowercase=True)
        if columns:
            tb_df = pd.read_sql_table(table, conn, columns=columns)
            for col in columns:
                if analyzer_flag:
                    tb_df[col] = tb_df[col].apply(lambda x: ' '.join(analyzer(' ' if (x is None or x == '') else x)))
                    # tb_df[col] = tb_df[col].apply(lambda x: ' '.join(analyzer(x)))
                else:
                    tb_df[col] = tb_df[col]
        else:
            tb_df = pd.read_sql_table(table, conn)
            if analyzer_flag:
                tb_df = tb_df.apply(lambda x: ' '.join(analyzer(' ' if (x is None or x == '') else x)))
        tb_df.fillna(' ', inplace=True)
        return tb_df

    def save_df2pickle(self, lastestdir, df, collkey, table):
        """pickle save"""
        st = time.time()
        tb_df_pkl_file = lastestdir + collkey + '_' + table + '.pkl'
        df.to_pickle(tb_df_pkl_file)
        log.info('save_df2pickle %s and time -> %s' % (tb_df_pkl_file, time.time() - st))

    def load_pickle2df(self, lastestdir, collkey, table):
        """pickle load"""
        st = time.time()
        tb_df_pkl_file = lastestdir + collkey + '_' + table + '.pkl'
        df = pd.read_pickle(tb_df_pkl_file)
        log.info('load_pickle2df %s and time -> %s' % (tb_df_pkl_file, time.time() - st))
        log.info(str(df.head()))
        return df

    async def a_train_func(self, modeltype, df, col, analyzer, models):
        s0 = timeit.default_timer()
        try:
            df_docs = df[col].values.tolist()
            if analyzer == 'jamo_sentence':
                processed_document = list(map(lambda x: tokenize_by_morpheme_sentence(x), tqdm(df_docs)))
                processed_document = list(map(lambda x: jamo_sentence(x), processed_document))
                corpus = [s.split() for s in tqdm(processed_document)]
                model = modeltype(corpus, size=100, workers=4, sg=1, iter=1, word_ngrams=5, min_count=1)
            else:
                model = modeltype([tokenize_by_morpheme_char(doc) for doc in df_docs], iter=1, min_count=1)
            models[col] = model
        except Exception as e:
            print('a_train_func col(%s) exception:%s' % (col, e))
        ttime = timeit.default_timer() - s0
        print('%s time:%s' % (col, ttime))

    async def process_async_exec_list(self, modeltype, df, columns, analyzer, models):
        async_exec_func_list = []
        for col in columns:
            async_exec_func_list.append(self.a_train_func(modeltype, df, col, analyzer, models))
        await asyncio.wait(async_exec_func_list)


    def async_train_models(self, modeltype, df, columns, analyzer):
        models = {}
        asyncio.run(self.process_async_exec_list(modeltype, df, columns, analyzer, models))
        return models

    def train_models(self, modeltype, df, columns, analyzer):
        models = {}
        if columns:
            for col in columns:
                df_docs = df[col].values.tolist()
                # model = modeltype([doc.split() for doc in df_docs], size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
                # model = modeltype([doc.split() for doc in df_docs], iter=1, min_count=1)
                # model = modeltype([tokenize_by_eojeol_jaso(doc) for doc in df_docs], iter=1, min_count=1)
                # model = modeltype([tokenize_by_morpheme_jaso(doc) for doc in df_docs], iter=1, min_count=1)
                cores = round(multiprocessing.cpu_count() / 2)
                if analyzer == 'jamo_sentence':
                    processed_document = list(map(lambda x: tokenize_by_morpheme_sentence(x), tqdm(df_docs)))
                    processed_document = list(map(lambda x: jamo_sentence(x), tqdm(processed_document)))
                    corpus = [s.split() for s in tqdm(processed_document)]
                    # model = modeltype(corpus, size=100, workers=4, sg=1, iter=1, word_ngrams=5, min_count=1)
                    model = modeltype(corpus,
                                      sg=1, # skip gram : sg = 1 in case of fasttext
                                      size=config.MODEL_SIZE, window=config.MODEL_WINDOW,
                                      min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS,
                                      iter=config.MODEL_ITER
                                      )
                else:
                    model = modeltype([tokenize_by_morpheme_char(doc) for doc in df_docs], size=100, workers=cores, iter=1, min_count=1)
                # model.train(df_docs, total_examples=len(df_docs), epochs=config.MODEL_EPOCHS)
                models[col] = model
        return models


    def train_and_save_by_collection(self, id, tb_df, configset, model, saveflag=True, dirresetflag=False):
        log.info('train_and_save_by_collection start : collection - %s' % (lambda x: x if x else 'ALL')(id))
        rt_model = benedict(model)
        if id:
            train_list = [id]
        else:
            train_list = configset.keys()
        resetflg = dirresetflag
        log.info('train list : collection - %s' % train_list)
        for coll_key in train_list:
            collection = configset.get(coll_key, {})
            if collection:
                analyzer = collection.get('analyzer', None)
                table = collection.get('table', None)
                modeltype = collection.get('modeltype', None)
                # columns = collection.get('columns', [])
                dfields = collection.get('df', [])
            # if columns:
            #     for col in columns:
            if dfields:
                for dfield in dfields:
                    log.info('train field :: collection name: %s | default field - %s' % (coll_key, dfield))
                    df_docs = tb_df[coll_key + '.' + table][dfield].values.tolist()
                    if modeltype == 'fasttext':
                        processed_document = list(map(lambda x: tokenize_by_morpheme_sentence(x), tqdm(df_docs)))
                        if analyzer == 'jamo_sentence':
                            processed_document = list(map(lambda x: jamo_sentence(x), processed_document))
                        # corpus = [s.encode('utf-8').split() for s in processed_document]
                        corpus = [s.split() for s in processed_document]
                        m = FastText(corpus,
                                         sg=config.MODEL_SG,  # 학습 알고리즘 : 스킵 그램의 경우 1; 그렇지 않으면 CBOW (기본 스킵 그램).
                                         word_ngrams=config.MODEL_WORD_NGRAMS,  # 5 ngram
                                         size=config.MODEL_SIZE,  #100 문장 내에서 현재 단어와 예상 단어 사이의 최대 거리
                                         window=config.MODEL_WINDOW,  #5 단어 윈도우 크기
                                         workers=config.MODEL_WORKERS,  #round(multiprocessing.cpu_count()/2) 모델을 훈련 할 작업자 스레드
                                         iter=config.MODEL_ITER,  #1회반복학습
                                         min_count=config.MODEL_MIN_COUNT,  #1총 빈도가 이보다 낮은 모든 단어를 무시
                                         )
                    else:
                        m = Word2Vec([tokenize_by_morpheme_char(doc) for doc in df_docs],
                                         size=config.MODEL_SIZE,  #100 단어크기
                                         window=config.MODEL_WINDOW,  #5 단어 윈도우 크기
                                         workers=config.MODEL_WORKERS,  #round(multiprocessing.cpu_count()/2)
                                         iter=config.MODEL_ITER,  #1회반복학습
                                         min_count=config.MODEL_MIN_COUNT,  #1회이상단어
                                         )
                    log.info('train field done :: collection name: %s | default field - %s' % (coll_key, dfield))
                    # m.build_vocab(corpus, update=False)
                    rt_model[coll_key+'.'+table+'.'+dfield] = m
                    if saveflag:
                        log.info('saveing field :: collection name: %s | default field - %s' % (coll_key, dfield))
                        self.save_a_model(m, coll_key, modeltype, table, dfield, dirresetflag=resetflg)
                        log.info('saved field :: collection name: %s | default field - %s' % (coll_key, dfield))
                        resetflg = False
        log.info('train_and_save_by_collection end : collection - %s' % (lambda x: x if x else 'ALL')(id))
        return rt_model

    def save_a_model(self, model, coll_key, modeltype, table, col, dirresetflag=False):
        dir = PROJECT_ROOT + config.MODEL_IR_PATH
        if dirresetflag:
            dir_manager(dir)
        lastestdir = _get_latest_timestamp_dir(dir)
        if lastestdir is None:
            _make_timestamp_dir(dir)
            lastestdir = _get_latest_timestamp_dir(dir)
        log.info('saving model_%s_%s_%s_%s' % (coll_key.lower(), modeltype.lower(), table.lower(), col.lower()))
        model.save('%smodel_%s_%s_%s_%s' % (lastestdir, coll_key.lower(), modeltype.lower(), table.lower(), col.lower()))
        # unload unnecessary memory after training
        model.init_sims(replace=True)
        log.info('saved %smodel_%s_%s_%s_%s' % (lastestdir, coll_key.lower(), modeltype.lower(), table.lower(), col.lower()))

    def get_retrieval_by_collections(self, id, tb_df, configset, model):
        r = benedict(dict())
        if id:
            coll_list = [id]
        else:
            coll_list = configset.keys()

        for coll_key in coll_list:
            collection = configset.get(coll_key, {})
            if collection:
                docid = collection.get('docid', None)
                # columns = collection.get('columns', None)
                mode = collection.get('mode', None)
                analyzer = collection.get('analyzer', None)
                table = collection.get('table', None)
                modeltype = collection.get('modeltype', [FastText])
                dfields = collection.get('df', [])

            tb_df_id = tb_df[coll_key][table][docid]
            tb_df_dfields_doc = tb_df[coll_key][table][dfields]
            r = self.get_retrievals_by_collkey(coll_key=coll_key, table=table,
                                                       mode=mode, models=model, dfields=dfields, retrieval=r,
                                                tb_df_doc=tb_df_dfields_doc, labels=tb_df_id.values.tolist())
        return r


    def get_retrievals_by_collkey(self, coll_key, table, mode, models, dfields, retrieval, tb_df_doc, labels):
        rt = benedict(retrieval)
        if dfields:
            for dfield in dfields:
                model = models[coll_key+'.'+table+'.'+dfield]
                retrieval = self.get_fit_retrieval(mode=mode, model=model, documents=tb_df_doc[dfield].values.tolist(), labels=labels)
                rt[coll_key+'.'+table+'.'+dfield] = retrieval
        return rt

    def load_models_by_collections(self, id, configset, model):
        try:
            pid = os.getpid()
            dir = PROJECT_ROOT + config.MODEL_IR_PATH
            lastestdir = _get_latest_timestamp_dir(dir)
            if lastestdir is None:
                _make_timestamp_dir(dir)
                lastestdir = _get_latest_timestamp_dir(dir)
            md = benedict(model)
            if id:
                load_model_list = [id]
            else:
                load_model_list = configset.keys()

            for coll_key in tqdm(load_model_list):
                collection = configset.get(coll_key, {})
                if collection:
                    table = collection.get('table', None)
                    modeltype = collection.get('modeltype', [FastText])
                    # columns = collection.get('columns', [])
                    dfields = collection.get('df', [])
                    if modeltype == 'fasttext':
                        vmodel = FastText
                    else:
                        vmodel = Word2Vec
                    for dfield in dfields:
                        log.info('loading model_%s_%s_%s_%s' % (coll_key.lower(), modeltype.lower(), table.lower(), dfield.lower()))
                        startload = time.time()
                        model = vmodel.load('%smodel_%s_%s_%s_%s' % (lastestdir, coll_key.lower(), modeltype.lower(), table.lower(), dfield.lower()))
                        md[coll_key + '.' + table + '.' + dfield] = model
                        log.info('load time:%s' % str(time.time()-startload))
                        log.info('pid:%s done | load time: %s' % (pid, time.time()-startload))
        except Exception as e:
            err = {'error': 'load_models_by_collections exception:%s' % e}
            log.error(err)
            return err
        return md

    async def a_save_func(self, models, modeltype, table, col):
        s0 = timeit.default_timer()
        try:
            dir = PROJECT_ROOT + config.MODEL_IR_PATH
            lastestdir = _get_latest_timestamp_dir(dir)
            if lastestdir is None:
                _make_timestamp_dir(dir)
                lastestdir = _get_latest_timestamp_dir(dir)

            log.info('saving model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
            models[col].save('%smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            # unload unnecessary memory after training
            models[col].init_sims(replace=True)
            log.info('saved %smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
        except Exception as e:
            log.info('a_save_func col(%s) exception:%s' % (col, e))
        ttime = timeit.default_timer() - s0
        log.info('%s a_save_func full time:%s' % (col, ttime))


    async def process_async_save_list(self, models, modeltype, table, columns):
        async_exec_func_list = []
        dir = PROJECT_ROOT + config.MODEL_IR_PATH
        dir_manager(dir)
        for col in columns:
            async_exec_func_list.append(self.a_save_func(models, modeltype, table, col))
        await asyncio.wait(async_exec_func_list)


    def aync_save_models(self, models, modeltype, table, columns):
        asyncio.run(self.process_async_save_list(models, modeltype, table, columns))

    def save_models(self, models, modeltype, table, columns, dirresetflag=True):
        dir = PROJECT_ROOT + config.MODEL_IR_PATH
        if dirresetflag:
            dir_manager(dir)
        lastestdir = _get_latest_timestamp_dir(dir)
        if lastestdir is None:
            _make_timestamp_dir(dir)
            lastestdir = _get_latest_timestamp_dir(dir)
        for col in columns:
            log.info('saving model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
            models[col].save('%smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            # unload unnecessary memory after training
            models[col].init_sims(replace=True)
            log.info('saved %smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))

    async def a_load_func(self, modeltype, table, col, models):
        s0 = timeit.default_timer()
        pid = os.getpid()
        dir = PROJECT_ROOT + config.MODEL_IR_PATH
        lastestdir = _get_latest_timestamp_dir(dir)
        if lastestdir is None:
            _make_timestamp_dir(dir)
            lastestdir = _get_latest_timestamp_dir(dir)
        log.info('loading model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
        startload = time.time()
        model = modeltype.load('%smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
        models[col] = model
        log.info('load time:%s' % str(time.time()-startload))
        log.info('pid:%s done | load time: %s' % (pid, time.time()-startload))
        ttime = timeit.default_timer() - s0
        log.info('%s time:%s' % (col, ttime))

    async def process_async_load_list(self, modeltype, table, columns, models):
        async_exec_func_list = []
        for col in tqdm(columns):
            async_exec_func_list.append(self.a_load_func(modeltype, table, col, models))
        await asyncio.wait(async_exec_func_list)


    def aync_load_models(self, modeltype, table, columns):
        models = {}
        asyncio.run(self.process_async_load_list(modeltype, table, columns, models))
        return models


    def load_models(self, modeltype, table, columns):
        pid = os.getpid()
        dir = PROJECT_ROOT + config.MODEL_IR_PATH
        lastestdir = _get_latest_timestamp_dir(dir)
        if lastestdir is None:
            _make_timestamp_dir(dir)
            lastestdir = _get_latest_timestamp_dir(dir)
        models = {}
        for col in columns:
            log.info('loading model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
            startload = time.time()
            model = modeltype.load('%smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            models[col] = model
            log.info('load time:%s' % str(time.time()-startload))
            time.sleep(1)
            log.info('pid:%s done | load time: %s' % (pid, time.time()-startload))
        return models

    def uptrain(self, modeltype, table, columns, more_sentences):
        models = self.load_models(modeltype, table, columns)
        # Resume Training on pre-trained model
        # more_sentences = [
        #     ['Advanced', 'users', 'can', 'load', 'a', 'model',
        #      'and', 'continue', 'training', 'it', 'with', 'more', 'sentences']
        # ]
        # 일단 vocabn을 업데이트해줘야 함.
        for col in columns:
            models[col].build_vocab(more_sentences, update=True)
            models[col].train(more_sentences, total_examples=len(more_sentences), epochs=10)
        return models


    def get_retrievals(self, coll_key, table, mode, models, columns, tb_df_doc, labels):
        retrievals = {}
        if columns:
            for col in columns:
                model = None
                if models:
                    model = models[col]
                # retrieval = self.get_fit_retrieval(mode='wcd', model=models[col], documents=tb_df_doc[col].values.tolist(), labels=labels)
                # retrieval = self.get_fit_retrieval(mode='combination', model=models[col], documents=tb_df_doc[col].values.tolist(), labels=labels)
                # retrieval = self.get_fit_retrieval(mode='tfidf', model=models[col], documents=tb_df_doc[col].values.tolist(), labels=labels)
                # retrieval = self.get_fit_retrieval(mode='expansion', model=models[col], documents=tb_df_doc[col].values.tolist(), labels=labels)
                retrieval = self.get_fit_retrieval(mode=mode, model=model, documents=tb_df_doc[col].values.tolist(), labels=labels)
                retrievals[col] = retrieval
        return retrievals

    def query_results_with_train(self, conn, modeltype, table, id, columns, q, k, trainingflag=True):
        """save and load query results"""
        tb_df_id = self.get_analyzered_data_df(conn=conn, table=table, columns=id, analyzer_flag=False)
        tb_df_columns_doc = self.get_analyzered_data_df(conn=conn, table=table, columns=columns, analyzer_flag=True)
        query_results = None
        if trainingflag:
            if modeltype:
                dirresetflag = True
                for mtype in modeltype:
                    model = self.train_models(mtype, tb_df_columns_doc, columns)
                    self.save_models(model, mtype, table, columns, dirresetflag)
                    dirresetflag = False
        if modeltype:
            for mtype in modeltype:
                loaded_model = self.load_models(mtype, table, columns)
                retrievals = self.get_retrievals(models=loaded_model, columns=columns, tb_df_doc=tb_df_columns_doc, labels=tb_df_id.values.tolist())
                start = timeit.default_timer()
                # query_results = self.get_query_results(q, modeltype, retrievals, columns, k=k)

                query_results = self.get_query_results(q=q, mode='wcd', modeltype=modeltype, retrievals=retrievals, columns=columns, docid=id[0],
                                  tb_df=tb_df_columns_doc, k=k, solr_kwargs={"df": ["content"]})

                ts = timeit.default_timer() - start
                query_results[mtype.__name__.lower()] = query_results
        return query_results

    def query_results(self, modeltype, lastestdir, table, id, columns, q, k, tb_df):
        """save and load query results"""
        # tb_df = self.load_pickle2df(lastestdir, table)
        tb_df_id = tb_df[id]
        tb_df_columns_doc = tb_df[columns]
        query_results = None
        if modeltype:
            for mtype in modeltype:
                loaded_model = self.load_models(mtype, table, columns)
                retrievals = self.get_retrievals(models=loaded_model, columns=columns, tb_df_doc=tb_df_columns_doc, labels=tb_df_id.values.tolist())
                start = timeit.default_timer()
                query_results = self.get_query_results(q, 'wcd', modeltype, retrievals, columns, k=k)
                ts = timeit.default_timer() - start
                print('model type:%s' % mtype)
                print('query time:%f' % ts)
                query_results[mtype.__name__.lower()] = query_results
                # print('query result count:%s' % len(query_results[columns]))
                print(query_results)
        else:
            print('There is no model type!! check modeltype, e.g. Word2Vec, FastText.')
        return query_results


    def get_query_results(self, q, id, retrievals,
                          tb_df, k, solr_kwargs, collection, solr_json):
        """
        https://wikidocs.net/3400
        """
        st = timeit.default_timer()

        # from configset params
        mode = collection.get('mode', None)
        table = collection.get('table', None)
        modeltype = collection.get('modeltype', 'word2vec')
        columns = collection.get('columns', [])
        docid = collection.get('docid', None)
        fl = collection.get('fl', None)
        sort = collection.get('sort', None)
        rows = collection.get('rows', None)
        df = collection.get('df', [])
        hl = collection.get('hl', False)
        facet = collection.get('facet', False)


        config_params = {
            'mode': mode,
            'table': table,
            'modeltype': modeltype,
            'columns': columns,
            'docid': docid,
            'fl': fl,
            'sort': sort,
            'mode': mode,
            'rows': rows,
            'df': df,
            'hl': hl,
            'facet': facet,
        }

        solr_json['responseHeader']['configset params'] = config_params

        # from url params
        df = dicfilter('df', solr_kwargs, collection, [])
        if not df:
            return {"error": "set the default field [df] to search !!"}
        boost = collection.get('boost', [])

        fl = dicfilter('fl', solr_kwargs, collection, [])
        qf = solr_kwargs.get('qf', '')
        print('qf:%s' % qf)

        fl_to_del = None
        tb_df_id_table = tb_df[id][table]
        tb_df_filtered = tb_df_id_table

        fq = solr_kwargs.get('fq', '')
        print('fq:%s' % fq)

        # filter query
        if fq:
            fq_e = fq_exp(fq)
            print('fq_e:%s' % fq_e)
            print('columns:%s' % columns)
            print(tb_df_id_table.head())
            tb_df_id_table_fq = tb_df_id_table.query(fq_e)
            print(tb_df_id_table_fq.head())
            tb_df_filtered = tb_df_id_table_fq

        # show field
        if qf:
            qf = qf.lower()
            qf_l = qf.split()
            print('qf_l:%s' % qf_l)
            fl = qf_l

        # field list
        if fl:
            fl_all = tb_df_id_table.columns
            fl_to_del = list(set(fl_all) - set(fl))
            fl_to_del = fl_to_del.append(docid)


        start = solr_kwargs.get('start', 0)
        rows = dicfilter('rows', solr_kwargs, collection, 20)
        # sort_column = solr_kwargs.get('sort', collection['sort']['column'])
        # sort_asc = solr_kwargs.get('asc', collection['sort']['asc'])


        boost_fx_rank_df = None
        i = 0


        # display all list on tb_df
        if q.strip() == '' or q.strip() == '*:*' or q.strip() == '*':
            docids = list(np.array(tb_df[docid].tolist()))
            score = list(np.zeros(len(tb_df)))

        for dfield in df:
            if mode == 'wcd':
                docids, score = retrievals[id.lower()][table.lower()][dfield.lower()].query(q=q, return_scores=True, k=k)
            elif mode == 'tfidf':
                docids, score = retrievals[id.lower()][table.lower()][dfield.lower()].query(jamo_to_word(q), return_scores=True, k=k)
            elif mode == 'expansion':
                docids, score = retrievals[id.lower()][table.lower()][dfield.lower()].query(q, return_scores=True, k=k)
            elif mode == 'combination':
                docids, score = retrievals[id.lower()][table.lower()][dfield.lower()].query(q=q, return_scores=True, k=k)
            else:
                docids, score = retrievals[id.lower()][table.lower()][dfield.lower()].query(q, return_scores=True, k=k)

            if boost:
                w = boost[i]
            else:
                w = list(map(lambda x: 1, df))[i]
            wscore = list(map(lambda x: x * w, score))
            f_rank_df = pd.DataFrame(list(zip(docids, wscore)), columns=[docid, str(i)])

            if i == 0:
                boost_fx_rank_df = f_rank_df
            else:
                boost_fx_rank_df = pd.merge(boost_fx_rank_df, f_rank_df, left_on=docid, right_on=docid, how='inner')
            boost_fx_rank_df.drop_duplicates(docid, keep='first', inplace=True)


            # last process
            if (len(df) - 1) == i:
                ls = range(len(df))
                ls = list(map(lambda x: str(x), ls))

                boost_fx_rank_df['score'] = boost_fx_rank_df[ls].sum(axis=1)
                boost_fx_rank_df = boost_fx_rank_df.sort_values(by=['score'], axis=0, ascending=False)
                boost_rows_df = boost_fx_rank_df[int(start):(int(start) + int(rows))]

                # boost_rows_df = boost_fx_rank_df[int(start):(int(start) + int(rows))]

                # if qf_l:
                #     fl_all = tb_df.columns
                #     qf_to_del = list(set(fl_all) - set(qf_l))
                #     tb_df.drop(qf_to_del, axis=1, inplace=True)

                boost_rows_df = pd.merge(boost_rows_df, tb_df_filtered, left_on=docid, right_on=docid, how='inner'
                                            ).sort_values(by=['score'], axis=0, ascending=False)

                if hl:
                    hl_b = benedict(hl)
                    h_field = hl_b.get('fl', None)
                    h_tag_pre = hl_b.get('tag.pre', '&lt;span style="font-weight:bold;"&gt;')
                    h_tag_post = hl_b.get('tag.post', '&lt;/span&gt;')
                    h_snippets = hl_b.get('snippets', 4)
                    h_alternateField = hl_b.get('alternateField', None)
                    h_maxlength = hl_b.get('maxAlternateFieldLength', 50)
                    h_word_list = ['a', '가']
                    boost_rows_df[h_alternateField] = boost_rows_df.apply(lambda x: highlight_list(x[h_field], h_word_list, h_tag_pre, h_tag_post, h_snippets, h_maxlength), axis=1)
                    h_df = boost_rows_df[[docid, h_alternateField]]
                    solr_json.update({'highlighting': h_df.set_index(docid, drop=True).to_dict('index')})

                if fl_to_del:
                    # fl_to_del.append(ls) --> delete score
                    boost_rows_df.drop(fl_to_del, axis=1, inplace=True)

                group = solr_kwargs.get('group', collection.get('group', None))

                if group:
                    collection_d = benedict(collection)
                    result = dict()
                    group_field = solr_kwargs.get('group.field', collection_d['group.field'])
                    group_limit = solr_kwargs.get('group.limit', collection_d['group.limit'])
                    group_ngroup = solr_kwargs.get('group.ngroup', collection_d['group.ngroup'])
                    group_sort_info = solr_kwargs.get('group.sort', collection_d['group.sort'])
                    group_sort = True

                    if group_sort_info:
                        group_sort_target_field = group_sort_info.a()[0]
                        group_sort = group_sort_info.split()[1]
                        if group_sort == 'desc' or group_sort == 'DESC':
                            group_sort = True
                        else:
                            group_sort = False

                    if group_field:

                        group_field_u = group_field.upper()
                        group_field = group_field.lower()
                        # result.update({'grouped': {group_field: None}})
                        result.update({'grouped': {group_field_u: None}})
                        field = dict()
                        field.update({'matches': len(boost_rows_df)})
                        # grouped = boost_rows_df.sort_values([group_field], ascending=group_sort).groupby(group_field)
                        grouped = boost_rows_df.sort_values([group_field], ascending=group_sort).groupby(group_field)
                        if group_ngroup:
                            field.update({'ngroups': len(grouped)})
                        # field.update({'groups': list()})
                        groups = list()
                        for key, agroup in grouped:
                            gr = dict()
                            gr.update({'groupValue': key})
                            doclist = dict()
                            doclist.update({'numFound': len(agroup)})
                            doclist.update({'start': 0})
                            doclist.update({'maxScore': None})
                            doclist.update({'docs': list(agroup.head(group_limit).set_index(docid, drop=True).to_dict('index').values())})
                            gr.update({'doclist': doclist})
                            # print("* key", key)
                            # print("* count", len(group))
                            # print(group.head())
                            # print('\n')
                            groups.append(gr)
                        field.update({'groups': groups})
                        # result.update({'grouped': {group_field: field}})
                        result.update({'grouped': {group_field_u: field}})

                        # boost_row_l = boost_rows_df.groupby(group_field).apply(list).to_dict()
                    solr_json.update(result)

                # if fl_to_del:
                #     # fl_to_del.append(ls) --> delete score
                #     boost_rows_df.drop(fl_to_del, axis=1, inplace=True)
                else:
                    # boost_rows_df = boost_fx_rank_df[int(start):(int(start) + int(rows))]
                    boost_dic_row = boost_rows_df.set_index(docid, drop=True).head(rows)
                    boost_dic = boost_dic_row.to_dict('index')
                    boost_row_l = list(boost_dic.values())
                    result = {'response':
                        {"numfound": len(boost_fx_rank_df), "docs": boost_row_l}
                    }
                    solr_json.update(result)

                # print(df['col1'].rank(method='min', ascending=False))
                # https://ponyozzang.tistory.com/612?category=800537
                # if not boost:
                #     rank = list(range(1, len(docids)+1))  # rank = rankdata(score, method='ordinal')
                #     idxrank_df = pd.DataFrame(list(zip(docids, rank, score)),
                #                  columns=[docid, 'rank', 'score'])
                #

            i += 1
        qtime = str(timeit.default_timer() - st)
        solr_json['responseHeader']['Qtime'] = qtime

        return solr_json
        #     results[mtype.__name__.lower()] = result_column
        # return results


def test_all_process_ir():
    from ir.irmanager import IrManager
    from gensim.models import Word2Vec, FastText, Doc2Vec
    import pprint as pp

    irm = IrManager()
    tb_df = irm.get_tb_df(table='bibl', pklsave=False)
    table = 'bibl'
    modeltype = [Word2Vec]
    docid = 'bbid'
    # columns = ['bible_bcn', 'content', 'econtent']
    columns = ['content']
    # word2vec
    word2vec_models = irm.train_models(Word2Vec, tb_df, columns)
    irm.save_models(word2vec_models, Word2Vec, table, columns, dirresetflag=True)

    retrievals = irm.set_init_models_and_get_retrievals(modeltype, table, docid, columns, tb_df)

    docids, score = retrievals[Word2Vec.__name__.lower()]['content'].query(q='예수께서 가라사대', return_scores=True)
    print(docids, score)
    q = '주께서 태초에 일하실 때에'
    print('q:%s' % q)
    st = timeit.default_timer()
    query_results = irm.get_query_results(q=q, mode='wcd', modeltype=modeltype, retrievals=retrievals, columns=columns,
                                          docid=docid, tb_df=tb_df, k=None, solr_kwargs={"df": ["content"]})

    qtime = str(timeit.default_timer() - st)
    print('take time: %s' % qtime)
    status = 200
    params = {
        "q": q
    }
    start = 0
    numfound = query_results[modeltype[0].__name__.lower()]['content']['numfound']
    docs = query_results[modeltype[0].__name__.lower()]['content']['docs']
    solr_json = irm.solr_json_return(status, qtime, params, numfound, start, docs)
    pp = pp.PrettyPrinter(indent=2)
    pp.pprint(solr_json)


def test_q2propost():
    from ir.irmanager import IrManager
    from gensim.models import Word2Vec, FastText, Doc2Vec
    import pprint as pp

    irm = IrManager()
    tb_df = irm.get_tb_df(table='bibl', pklsave=False)
    table = 'bibl'
    modeltype = [Word2Vec]
    docid = 'bbid'
    # columns = ['bible_bcn', 'content', 'econtent']
    columns = ['content']
    # word2vec
    model = irm.train_models(Word2Vec, tb_df, columns)

    # # 단어 리스트 작성
    # vocab = model.index2word
    # # 전체 단어벡터 추출
    # wordvectors = []
    # for v in vocab:
    #     wordvectors.append(model.wv[v])

    rtjson = model.most_similar('하나님', topn=10)
    pp = pp.PrettyPrinter(indent=2)
    pp.pprint(rtjson)
    return rtjson


if __name__ == "__main__":
    from ir.irmanager import IrManager
    from gensim.models import Word2Vec, FastText, Doc2Vec
    irm = IrManager()
    # irm.test_word2vec()
    # irm.test_word2vec_bible()

    # test_all_process_ir()
    test_q2propost()




