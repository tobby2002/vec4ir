import os, sys, time, timeit
import pandas as pd
import numpy as np
import asyncio
from ir.base import Matching, Tfidf
from ir.core import Retrieval
from ir.utils import build_analyzer
from ir.word2vec import WordCentroidDistance
from util.dirmanager import _get_latest_timestamp_dir, dir_manager, _make_timestamp_dir
from util.dbmanager import get_connect_engine_wi
from util.logmanager import logger
from util.utilmanager import build_analyzer, dicfilter, tokenize_by_morpheme_char, \
    jamo_sentence, tokenize_by_morpheme_sentence, jamo_to_word
from ir.query_expansion import EmbeddedQueryExpansion
from tqdm import tqdm

log = logger('ir', 'irmanager')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

import config

documents = ["This article is about the general concept of art. For the group of creative disciplines, see The arts. For other uses, see Art (disambiguation). Clockwise from upper left: a self-portrait by Vincent van Gogh; a female ancestor figure by a Chokwe artist; detail from The Birth of Venus by Sandro Botticelli; and an Okinawan Shisa lion Art is a diverse range of human activities in creating visual, auditory or performing artifacts (artworks), expressing the author's imaginative, conceptual ideas, or technical skill, intended to be appreciated for their beauty or emotional power.[1][2] In their most general form these activities include the production of works of art, the criticism of art, the study of the history of art, and the aesthetic dissemination of art. The three classical branches of art are painting, sculpture and architecture.[3] Music, theatre, film, dance, and other performing arts, as well as literature and other media such as interactive media, are included in a broader definition of the arts.[1][4] Until the 17th century, art referred to any skill or mastery and was not differentiated from crafts or sciences. In modern usage after the 17th century, where aesthetic considerations are paramount, the fine arts are separated and distinguished from acquired skills in general, such as the decorative or applied arts.Though the definition of what constitutes art is disputed[5][6][7] and has changed over time, general descriptions mention an idea of imaginative or technical skill stemming from human agency[8] and creation.[9] The nature of art and related concepts, such as creativity and interpretation, are explored in a branch of philosophy known as aesthetics.[10]",
                "Science (from the Latin word scientia, meaning knowledge is a systematic enterprise that builds and organizes knowledge in the form of testable explanations and predictions about the universe.[2][3][4] The earliest roots of science can be traced to Ancient Egypt and Mesopotamia in around 3500 to 3000 BCE.[5][6] Their contributions to mathematics, astronomy, and medicine entered and shaped Greek natural philosophy of classical antiquity, whereby formal attempts were made to provide explanations of events in the physical world based on natural causes.[5][6] After the fall of the Western Roman Empire, knowledge of Greek conceptions of the world deteriorated in Western Europe during the early centuries (400 to 1000 CE) of the Middle Ages[7] but was preserved in the Muslim world during the Islamic Golden Age.[8] The recovery and assimilation of Greek works and Islamic inquiries into Western Europe from the 10th to 13th century revived natural philosophy,[7][9] which was later transformed by the Scientific Revolution that began in the 16th century[10] as new ideas and discoveries departed from previous Greek conceptions and traditions.[11][12][13][14] The scientific method soon played a greater role in knowledge creation and it was not until the 19th century that many of the institutional and professional features of science began to take shape;[15][16][17] along with the changing from natural philosophy to the natural sciences.[18] Modern science is typically divided into three major branches that consist of the natural sciences (e.g., biology, chemistry, and physics), which study nature in the broadest sense; the social sciences (e.g., economics, psychology, and sociology), which study individuals and societies; and the formal sciences (e.g., logic, mathematics, and theoretical computer science), which study abstract concepts. There is disagreement,[19][20] however, on whether the formal sciences actually constitute a science as they do not rely on empirical evidence.[21] Disciplines that use existing scientific knowledge for practical purposes, such as engineering and medicine, are described as applied sciences.[22][23][24][25] Science is based on research, which is commonly conducted in academic and research institutions as well as in government agencies and companies. The practical impact of scientific research has led to the emergence of science policies that seek to influence the scientific enterprise by prioritizing the development of commercial products, armaments, health care, and environmental protection.",
                "Deep learning (also known as deep structured learning or hierarchical learning) is part of a broader family of machine learning methods based on artificial neural networks. Learning can be supervised, semi-supervised or unsupervised.[1][2][3] Deep learning architectures such as deep neural networks, deep belief networks, recurrent neural networks and convolutional neural networks have been applied to fields including computer vision, speech recognition, natural language processing, audio recognition, social network filtering, machine translation, bioinformatics, drug design, medical image analysis, material inspection and board game programs, where they have produced results comparable to and in some cases superior to human experts.[4][5][6] Artificial Neural Networks (ANNs) were inspired by information processing and distributed communication nodes in biological systems. ANNs have various differences from biological brains. Specifically, neural networks tend to be static and symbolic, while the biological brain of most living organisms is dynamic (plastic) and analog.[7][8][9]",
                "Cable News Network (CNN) is an American news-based pay television channel owned by AT&T's WarnerMedia.[1] CNN was founded in 1980 by American media proprietor Ted Turner as a 24-hour cable news channel.[2] Upon its launch, CNN was the first television channel to provide 24-hour news coverage,[3] and was the first all-news television channel in the United States.[4] While the news channel has numerous affiliates, CNN primarily broadcasts from 30 Hudson Yards in New York City, and studios in Washington, D.C. and Los Angeles. Its headquarters at the CNN Center in Atlanta is only used for weekend programming. CNN is sometimes referred to as CNN/U.S. (or CNN Domestic)[5] to distinguish the U.S. channel from its international sister network, CNN International. As of August 2010, CNN is available in over 100 million U.S. households.[6] Broadcast coverage of the U.S. channel extends to over 890,000 American hotel rooms,[6] as well as carriage on subscription providers throughout Canada. As of July 2015, CNN is available to about 96,374,000 pay-television households (82.8% of households with at least one television set) in the United States.[7] Globally, CNN programming airs through CNN International, which can be seen by viewers in over 212 countries and territories.[8]The following is a list of notable current and past news anchors, correspondents, hosts, regular contributors and meteorologists from the CNN, CNN International and HLN news networks.[1]",
                "ABC News is the news division of the American Broadcasting Company (ABC), owned by the Disney Media Networks division of The Walt Disney Company. Its flagship program is the daily evening newscast ABC World News Tonight with David Muir; other programs include morning news-talk show Good Morning America, Nightline, Primetime, and 20/20, and Sunday morning political affairs program This Week with George Stephanopoulos.Only after Roone Arledge, the president of ABC Sports at the time, was appointed as president of ABC News in 1977, at a time when the network's prime-time entertainment programs were achieving stronger ratings and drawing in higher advertising revenue and profits to the ABC corporation overall, was ABC able to invest the resources to make it a major source of news content. Arledge, known for experimenting with the broadcast 'model', created many of ABC News' most popular and enduring programs, including 20/20, World News Tonight, This Week, Nightline and Primetime Live.[3] ABC News' longtime slogan, 'More Americans get their news from ABC News than from any other source' (introduced in the late 1980s), was a claim referring to the number of people who watch, listen to and read ABC News content on television, radio and (eventually) the Internet, and not necessarily to the telecasts alone.[4] In June 1998, ABC News (which owned an 80% stake in the service), Nine Network and ITN sold their respective interests in Worldwide Television News to the Associated Press. Additionally, ABC News signed a multi-year content deal with AP for its affiliate video service Associated Press Television News (APTV) while providing material from ABC's news video service ABC News One to APTV.[5]",
             "Computer scientists are lazy art"]
DEFAULT_ANALYZER = build_analyzer('sklearn', stop_words=False, lowercase=True)
# jamo process
# https://joyhong.tistory.com/137
class IrManager:

    def __init__(self):
        pass

    def get_tb_df(self, table=None, pklsave=False):
        try:
            conn = get_connect_engine_wi()
            if not pklsave:
                tb_df = self.get_analyzered_data_df(conn=conn, table=table, columns=None, analyzer_flag=False)
            else:
                dir = PROJECT_ROOT + config.MODEL_IR_PATH
                lastestdir = _get_latest_timestamp_dir(dir)
                if not lastestdir:
                    tb_df_table = self.get_analyzered_data_df(conn=conn, table=table, columns=None, analyzer_flag=False)
                    self.save_df2pickle(lastestdir, tb_df_table, table)
                    tb_df_table_loaded = self.load_pickle2df(lastestdir, table)
                    # print(tb_df_table_loaded.head(5))
                    tb_df = tb_df_table_loaded
            conn.close()
        except UnboundLocalError as e:
            log.error('error in get_tb_df:%s' % str(e))
            return None
        except Exception as e:
            log.error('error in get_tb_df:%s' % str(e))
            conn.close()
            return None
        finally:
            conn.close()
        return tb_df

    def set_init_models_and_get_retrievals(self, mode, modeltype, table, docid, columns, tb_df, onlymodel=False):
        """save and load query results"""
        log.info('set_init_models_and_get_retrievals')
        print('set_init_models_and_get_retrievals')
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
            print('There is no model type!! check modeltype, e.g. Word2Vec, FastText.')
        return retrievals, loaded_model

    def test_word2vec(self):
        doclist = [doc.split() for doc in documents]
        model = Word2Vec(doclist, iter=1, min_count=1)
        match_op = Matching()
        wcd = WordCentroidDistance(model.wv)
        retrieval = Retrieval(wcd, matching=match_op, labels=['1번', '2번', '3번', '4번', '5번', '6번'])
        retrieval.fit(documents)
        result, score = retrieval.query('art news', return_scores=True)
        print(result, score)

    def test_word2vec_bible(self):
        from ir.irmanager import IrManager
        from gensim.models import Word2Vec, FastText, Doc2Vec
        import pprint as pp

        irm = IrManager()
        tb_df = irm.get_tb_df(table='bibl', pklsave=False)

        doclist = tb_df['content'].values.tolist()
        bbid = tb_df['bbid'].values.tolist()
        model = Word2Vec([doc.split() for doc in doclist], iter=1, min_count=1)
        match_op = Matching()
        wcd = WordCentroidDistance(model.wv)
        retrieval = Retrieval(wcd, matching=match_op, labels=bbid)
        retrieval.fit(doclist)
        result, score = retrieval.query('세상에', return_scores=True)
        print(result, score)
        result, score = retrieval.query('in the beginning, God said love', return_scores=True)
        print(result, score)
        result, score = retrieval.query('in the beginning, God said love', return_scores=True)
        print(result, score)

    def test_tfidf(self):
        # Test tfidf retrieval with auto-generated ids
        tfidf = Tfidf()
        tfidf.fit(documents)
        result = tfidf.query('article')
        print(result)
        # assert result[0] == 1
        # assert result[1] == 0

    def get_docs_load_df_by_column(self, conn, table, column):
        cur = conn.cursor()
        cur.execute('select * from %s' % table)
        cols = [column[0] for column in cur.description]
        # print(dataframe.memory_usage())
        query_df = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)
        # query_df[column] = query_df[column].apply(lambda x: 'N' if x is None or x == '' else x)
        docs_list = query_df[column].values.tolist()
        return docs_list

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
            DEFAULT_ANALYZER = build_analyzer('sklearn', stop_words=True, lowercase=True)
        if columns:
            tb_df = pd.read_sql_table(table, conn, columns=columns)
            for col in columns:
                if analyzer_flag:
                    tb_df[col] = tb_df[col].apply(lambda x: ' '.join(DEFAULT_ANALYZER(' ' if (x is None or x == '') else x)))
                    # tb_df[col] = tb_df[col].apply(lambda x: ' '.join(DEFAULT_ANALYZER(x)))
                else:
                    tb_df[col] = tb_df[col]
        else:
            tb_df = pd.read_sql_table(table, conn)
            if analyzer_flag:
                tb_df = tb_df.apply(lambda x: ' '.join(DEFAULT_ANALYZER(' ' if (x is None or x == '') else x)))
        return tb_df

    def save_df2pickle(self, lastestdir, df, table):
        """pickle save"""
        st = time.time()
        tb_df_pkl_file = lastestdir + table + '.pkl'
        df.to_pickle(tb_df_pkl_file)
        print('save_df2pickle %s and time -> %s' % (tb_df_pkl_file, time.time() - st))

    def load_pickle2df(self, lastestdir, table):
        """pickle load"""
        st = time.time()
        tb_df_pkl_file = lastestdir + table + '.pkl'
        df = pd.read_pickle(tb_df_pkl_file)
        print('load_pickle2df %s and time -> %s' % (tb_df_pkl_file, time.time() - st))
        print(df.head())
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


    def aync_train_models(self, modeltype, df, columns, analyzer):
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
                if analyzer == 'jamo_sentence':
                    processed_document = list(map(lambda x: tokenize_by_morpheme_sentence(x), tqdm(df_docs)))
                    processed_document = list(map(lambda x: jamo_sentence(x), tqdm(processed_document)))
                    corpus = [s.split() for s in tqdm(processed_document)]
                    model = modeltype(corpus, size=100, workers=4, sg=1, iter=1, word_ngrams=5, min_count=1)
                else:
                    model = modeltype([tokenize_by_morpheme_char(doc) for doc in df_docs], iter=1, min_count=1)
                # model = modeltype([tokenize_by_morpheme_char(doc) for doc in df_docs],
                #                   sg=1, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
                # model.train(df_docs, total_examples=len(df_docs), epochs=config.MODEL_EPOCHS)
                models[col] = model
        return models


    async def a_save_func(self, models, modeltype, table, col):
        s0 = timeit.default_timer()
        try:
            dir = PROJECT_ROOT + config.MODEL_IR_PATH
            if True:
                dir_manager(dir)
            lastestdir = _get_latest_timestamp_dir(dir)
            if lastestdir is None:
                _make_timestamp_dir(dir)
                lastestdir = _get_latest_timestamp_dir(dir)

            print('saving model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
            log.info('saving model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
            models[col].save('%smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            # unload unnecessary memory after training
            models[col].init_sims(replace=True)
            log.info('saved %smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            print('saved %smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
        except Exception as e:
            print('a_save_func col(%s) exception:%s' % (col, e))
        ttime = timeit.default_timer() - s0
        print('%s a_save_func full time:%s' % (col, ttime))

    async def process_async_save_list(self, models, modeltype, table, columns):
        async_exec_func_list = []
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
            print('saving model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
            log.info('saving model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
            models[col].save('%smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            # unload unnecessary memory after training
            models[col].init_sims(replace=True)
            log.info('saved %smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            print('saved %smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))

    async def a_load_func(self, modeltype, table, col, models):
        s0 = timeit.default_timer()
        pid = os.getpid()
        dir = PROJECT_ROOT + config.MODEL_IR_PATH
        lastestdir = _get_latest_timestamp_dir(dir)
        if lastestdir is None:
            _make_timestamp_dir(dir)
            lastestdir = _get_latest_timestamp_dir(dir)
        log.info('loading model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
        print('loading model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
        startload = time.time()
        model = modeltype.load('%smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
        models[col] = model
        log.info('load time:%s' % str(time.time()-startload))
        print('load time:%s' % str(time.time()-startload))
        log.info('pid:%s done | load time: %s' % (pid, time.time()-startload))
        ttime = timeit.default_timer() - s0
        print('%s time:%s' % (col, ttime))

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
            print('loading model_%s_%s_%s' % (modeltype.__name__.lower(), table.lower(), col.lower()))
            startload = time.time()
            model = modeltype.load('%smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            models[col] = model
            log.info('load time:%s' % str(time.time()-startload))
            print('load time:%s' % str(time.time()-startload))
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

    def get_retrievals(self, mode, models, columns, tb_df_doc, labels):
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
                print('model type:%s' % mtype)
                print('query time:%f' % ts)
                query_results[mtype.__name__.lower()] = query_results
                # print('query result count:%s' % len(query_results[columns]))
                print(query_results)
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


    def get_query_results(self, q, retrievals,
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
        df = collection.get('df', None)
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
        }
        solr_json['responseHeader']['configset params'] = config_params

        # from url params
        df = dicfilter('df', solr_kwargs, collection, [])
        if not df:
            return {"error": "set the default field [df] to search !!"}
        boost = collection.get('boost', [])

        fl = dicfilter('fl', solr_kwargs, collection, [])
        fl_to_del = None
        if fl:
            fl_all = tb_df.columns
            fl_to_del = list(set(fl_all) - set(fl))

        start = solr_kwargs.get('start', 0)
        rows = dicfilter('rows', solr_kwargs, collection, 20)
        sort_column = solr_kwargs.get('sort', collection['sort']['column'])
        sort_asc = solr_kwargs.get('asc', collection['sort']['asc'])
        boost_fx_rank_df = None
        i = 0

        # display all list on tb_df
        if q.strip() == '' or q.strip() == '*:*':
            docids = list(np.array(tb_df[docid].tolist()))
            score = list(np.zeros(len(tb_df)))

        for col in df:
            if mode == 'wcd':
                docids, score = retrievals[modeltype.lower()][col].query(q=q, return_scores=True, k=k)
            elif mode == 'tfidf':
                docids, score = retrievals[modeltype.lower()][col].query(jamo_to_word(q), return_scores=True, k=k)
            elif mode == 'expansion':
                docids, score = retrievals[modeltype.lower()][col].query(q, return_scores=True, k=k)
            elif mode == 'combination':
                docids, score = retrievals[modeltype.lower()][col].query(q=q, return_scores=True, k=k)
            else:
                docids, score = retrievals[modeltype.lower()][col].query(q, return_scores=True, k=k)

            if boost:
                w = boost[i]
            else:
                w = list(map(lambda x: 1, df))[i]
            wscore = list(map(lambda x: x * w, score))
            f_rank_df = pd.DataFrame(list(zip(docids, wscore)), columns=[docid, str(i)])
            if i == 0:
                boost_fx_rank_df = f_rank_df
            else:
                boost_fx_rank_df = pd.merge(boost_fx_rank_df, f_rank_df, left_on=docid, right_on=docid, how='outer')

            if (len(df) - 1) == i:
                ls = range(len(df))
                ls = list(map(lambda x: str(x), ls))

                boost_fx_rank_df['score'] = boost_fx_rank_df[ls].sum(axis=1)
                boost_fx_rank_df = boost_fx_rank_df.sort_values(by=['score'], axis=0, ascending=False)
                boost_rows_df = boost_fx_rank_df[int(start):(int(start) + int(rows))]

                # boost_rows_df = boost_fx_rank_df[int(start):(int(start) + int(rows))]

                boost_rows_df = pd.merge(boost_rows_df, tb_df, left_on=docid, right_on=docid, how='inner'
                                            ).sort_values(by=['score'], axis=0, ascending=False)
                if fl_to_del:
                    # fl_to_del.append(ls) --> delete score
                    boost_rows_df.drop(fl_to_del, axis=1, inplace=True)

                group = solr_kwargs.get('group', collection.get('group', None))

                if group:
                    result = dict()
                    group_field = solr_kwargs.get('group_field', group.get('field', None))
                    group_limit = solr_kwargs.get('group_limit', group.get('limit', 5))
                    group_ngroup = solr_kwargs.get('group_ngroup', group.get('ngroup', True))
                    group_asc = solr_kwargs.get('group_asc', group.get('asc', True))
                    if group_field:
                        result.update({'grouped': {group_field: None}})
                        field = dict()
                        field.update({'matches': len(boost_rows_df)})
                        grouped = boost_rows_df.sort_values([group_field], ascending=group_asc).groupby(group_field)
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
                            doclist.update({'docs': list(agroup.head(group_limit).set_index(docid, drop=False).to_dict('index').values())})
                            gr.update({'doclist': doclist})
                            # print("* key", key)
                            # print("* count", len(group))
                            # print(group.head())
                            # print('\n')
                            groups.append(gr)
                        field.update({'groups': groups})
                        result.update({'grouped': {group_field: field}})

                        # boost_row_l = boost_rows_df.groupby(group_field).apply(list).to_dict()
                    solr_json.update(result)

                # if fl_to_del:
                #     # fl_to_del.append(ls) --> delete score
                #     boost_rows_df.drop(fl_to_del, axis=1, inplace=True)
                else:
                    # boost_rows_df = boost_fx_rank_df[int(start):(int(start) + int(rows))]
                    boost_dic_row = boost_rows_df.set_index(docid, drop=False).head(rows)
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
                #     qtime = str(timeit.default_timer() - st)
                #     print('col: %s' % col)
                #     # print('docids: %s' % docids)
                #     # print('score: %s' % score)
                #     print('%s take time: %s' % (col, qtime))
                #
                #     st1 = timeit.default_timer()
                #
                #     df_inner_join = pd.merge(idxrank_df, tb_df, left_on=docid, right_on=docid, how='inner'
                #                              ).sort_values(by=[sort_column], axis=0, ascending=sort_asc)
                #
                #     qtime1 = str(timeit.default_timer() - st1)
                #     print('%s - df_inner_join take time: %s' % (col, qtime1))
                #
                #     if fl_to_del:
                #         df_inner_join.drop(fl_to_del, axis=1, inplace=True)
                #              #     # print(list(df_INNER_JOIN.columns))             #     start_rows_df = df_inner_join[int(start):(int(start) + int(rows))]
                #     row_dic_row = start_rows_df.set_index('rank', drop=False).head(rows)
                #     row_dic = row_dic_row.to_dict('index')
                #     row_l = list(row_dic.values())
                #     numFound = len(docids)
                #     result_column[col] = {"numfound": numFound, "docs": row_l}
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




