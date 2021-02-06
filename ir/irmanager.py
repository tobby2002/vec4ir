import os, sys, time, timeit
import pytest
import pandas as pd
from scipy.stats import rankdata
import numpy as np
import gensim
from gensim.models import Word2Vec, FastText, Doc2Vec
from ir.base import Matching, Tfidf
from ir.core import Retrieval
from ir.utils import build_analyzer
from ir.word2vec import WordCentroidDistance, WordMoversDistance
from ir.word2vec import Word2VecRetrieval, WordCentroidRetrieval
from util.dirmanager import _get_latest_timestamp_dir, dir_manager, _make_timestamp_dir
from util.dbmanager import get_connect_engine_p
from util.dbmanager import get_connect_engine_wi
from util.logmanager import logger
from util.utilmanager import build_analyzer, to_jaso, tokenize_by_morpheme_jaso, tokenize_by_morpheme_char
from ir.text_preprocessing import TextPreprocessing
from ir.query_expansion import CentroidExpansion, EmbeddedQueryExpansion

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
                    print(tb_df_table_loaded.head(5))
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

    def set_init_models_and_get_retrievals(self, mode, modeltype, table, docid, columns, tb_df):
        """save and load query results"""
        log.info('set_init_models_and_get_retrievals')
        print('set_init_models_and_get_retrievals')
        retrievals = {}
        tb_df_id = tb_df[docid]
        tb_df_columns_doc = tb_df[columns]
        if modeltype:
            for mtype in modeltype:
                loaded_model = None
                if mode != 'tfidf':
                    loaded_model = self.load_models(mtype, table, columns)
                retrieval = self.get_retrievals(mode=mode, models=loaded_model, columns=columns, tb_df_doc=tb_df_columns_doc, labels=tb_df_id.values.tolist())
                retrievals[mtype.__name__.lower()] = retrieval
        else:
            log.info('There is no model type!! check modeltype, e.g. Word2Vec, FastText.')
            print('There is no model type!! check modeltype, e.g. Word2Vec, FastText.')
        return retrievals

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
        if mode == 'wcd':
            match_op = Matching()
            wcd = WordCentroidDistance(model.wv)
            retrieval = Retrieval(wcd, matching=match_op, labels=labels)
            retrieval.fit(documents)
        elif mode == 'tfidf':
            retrieval = Tfidf()
            retrieval.fit(documents)
        elif mode == 'tfidf+vec+expansion':
            n_expansions = 2
            tfidf = Tfidf()
            match_op = Matching()
            expansion_op = EmbeddedQueryExpansion(model.wv, m=n_expansions)
            retrieval = Retrieval(tfidf,  # The retrieval model
                                  matching=match_op,
                                  query_expansion=expansion_op, labels=labels)
            retrieval.fit(documents)
        elif mode == 'combination':
            wcd = WordCentroidDistance(model.wv)
            tfidf = Tfidf()
            wcd.fit(documents)
            # # they can operate on different feilds
            tfidf.fit(documents)
            match_op = Matching().fit(documents)
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

    def train_models(self, modeltype, df, columns):
        models = {}
        if columns:
            for col in columns:
                df_docs = df[col].values.tolist()
                # model = modeltype([doc.split() for doc in df_docs], size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
                # model = modeltype([doc.split() for doc in df_docs], iter=1, min_count=1)
                # model = modeltype([tokenize_by_eojeol_jaso(doc) for doc in df_docs], iter=1, min_count=1)
                # model = modeltype([tokenize_by_morpheme_jaso(doc) for doc in df_docs], iter=1, min_count=1)
                model = modeltype([tokenize_by_morpheme_char(doc) for doc in df_docs], iter=1, min_count=1)
                # model = modeltype([tokenize_by_morpheme_char(doc) for doc in df_docs],
                #                   sg=1, size=config.MODEL_SIZE, window=config.MODEL_WINDOW, min_count=config.MODEL_MIN_COUNT, workers=config.MODEL_WORKERS)
                model.train(df_docs, total_examples=len(df_docs), epochs=config.MODEL_EPOCHS)
                models[col] = model
        return models

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
            log.info('saved %smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))
            print('saved %smodel_%s_%s_%s' % (lastestdir, modeltype.__name__.lower(), table.lower(), col.lower()))

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
                # retrieval = self.get_fit_retrieval(mode='tfidf+vec+expansion', model=models[col], documents=tb_df_doc[col].values.tolist(), labels=labels)
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


    def get_query_results(self, q, mode, modeltype, retrievals, columns, docid, tb_df, k, solr_kwargs):
        """
        https://wikidocs.net/3400
        """
        df = solr_kwargs.get('df', [])
        if not df:
            return {"error": "set the default field [df] to search !!"}

        fl = solr_kwargs.get('fl', [])
        fl_to_del = None
        if fl:
            fl_all = tb_df.columns
            fl_to_del = list(set(fl_all) - set(fl))

        if df:
            columns = df

        start = solr_kwargs.get('start', 0)
        rows = solr_kwargs.get('rows', 20)

        results = {}
        for mtype in modeltype:
            result_column = {}
            for col in columns:

                st = timeit.default_timer()

                if mode == 'wcd':
                    docids, score = retrievals[mtype.__name__.lower()][col].query(q=q, return_scores=True, k=k)
                elif mode == 'tfidf':
                    docids, score = retrievals[mtype.__name__.lower()][col].query(q, return_scores=True, k=k)
                elif mode == 'tfidf+vec+expansion':
                    docids, score = retrievals[mtype.__name__.lower()][col].query(q, return_scores=True, k=k)
                elif mode == 'combination':
                    docids, score = retrievals[mtype.__name__.lower()][col].query(q=q, return_scores=True, k=k)
                else:
                    docids, score = retrievals[mtype.__name__.lower()][col].query(q, return_scores=True, k=k)

                # display all list on tb_df
                if q == '' or q == '*:*':
                    docids = list(np.array(tb_df[docid].tolist()))

                rank = list(range(1, len(docids)+1))  # rank = rankdata(score, method='ordinal')
                idxrank_df = pd.DataFrame(list(zip(docids, rank, score)),
                             columns=[docid, 'rank', 'score'])
                qtime = str(timeit.default_timer() - st)
                print('col: %s' % col)
                # print('docids: %s' % docids)
                # print('score: %s' % score)
                print('%s take time: %s' % (col, qtime))

                st1 = timeit.default_timer()
                df_inner_join = pd.merge(idxrank_df, tb_df, left_on=docid, right_on=docid, how='inner').sort_values(by=['rank'], axis=0, ascending=True)
                qtime1 = str(timeit.default_timer() - st1)
                print('%s - df_inner_join take time: %s' % (col, qtime1))

                if fl_to_del:
                    df_inner_join.drop(fl_to_del, axis=1, inplace=True)

                # print(list(df_INNER_JOIN.columns))
                start_rows_df = df_inner_join[int(start):(int(start) + int(rows))]
                row_dic_row = start_rows_df.set_index('rank', drop=False).head(rows)
                row_dic = row_dic_row.to_dict('index')
                row_l = list(row_dic.values())
                numFound = len(docids)

                result_column[col] = {"numfound": numFound, "docs": row_l}
            results[mtype.__name__.lower()] = result_column
        return results

    def solr_json_return(self, status, qtime, params, numfound, start, docs):
        solr_json_return = {
            "responseHeader": {
                "status": status,
                "Qtime": qtime,
                "params": params
            },
            "response": {"numFound": numfound, "start": start, "docs": docs
            }
        }
        return solr_json_return


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

if __name__ == "__main__":
    from ir.irmanager import IrManager
    from gensim.models import Word2Vec, FastText, Doc2Vec
    irm = IrManager()
    # irm.test_word2vec()
    # irm.test_word2vec_bible()

    test_all_process_ir()




