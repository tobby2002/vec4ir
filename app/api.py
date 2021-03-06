import os, sys, timeit
from tqdm import tqdm
from benedict import benedict
from util.solrapiparser import SolrAPIParser
from util.utilmanager import get_configset, q2morph, jamo_sentence, dfconcat
from util.apidefmanager import get_q2propose_multi_by_query
from ir.irmanager import IrManager
from ninja import NinjaAPI
from util.logmanager import logz
from api.scheduler import Scheduler
from konlpy.tag import Mecab

MECAB = Mecab()
log = logz()
api = NinjaAPI(version='1.0.0')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

IRM = IrManager()
CONFIGSET = dict()
TB_DB = dict()
MODEL = dict()
COLLECTION = dict()
RETRIEVAL = dict()
jobsc = Scheduler()

RETRIEVAL_ATACH_CONTENTS = dict()
MODEL_ATACH_CONTENTS = dict()
VOCADOCS_ATACH_CONTENTS = dict()

RETRIEVAL_RT_TERM = dict()
MODEL_RT_TERM = dict()
VOCADOCS_RT_TERM = dict()

def start_fc():
    global IRM
    global CONFIGSET
    global TB_DB
    global MODEL
    global RETRIEVAL

    succsss = True
    rmsg = dict
    try:
        irm_ = IrManager()
        configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
        tb_df_ = irm_.get_tb_df_by_collection(None, configset_)
        model_ = irm_.train_and_save_by_collection(None, tb_df_, configset_, dict(),
                                                   saveflag=True,  # save model file
                                                   dirresetflag=True  # make new recent directory
                                                   )
        retrieval_ = irm_.get_retrieval_by_collections(None, tb_df_, configset_, model_)
        CONFIGSET = configset_
        TB_DB = tb_df_
        MODEL = model_
        RETRIEVAL = retrieval_
        rmsg['msg'] = 'initiated all collection'
    except Exception as e:
        log.error(str(e))
        rmsg = {'error': str(e)}
        succsss = False
    return succsss, rmsg


def propose_fc():
    global MODEL_ATACH_CONTENTS
    global RETRIEVAL_ATACH_CONTENTS
    global VOCADOCS_ATACH_CONTENTS
    global MODEL_RT_TERM
    global RETRIEVAL_RT_TERM
    global VOCADOCS_RT_TERM

    succsss = True
    rmsg = dict
    MODEL_ATACH_CONTENTS = MODEL['oj_kn']['tb_ir_kn']['ATACH_CONTENTS']

jobsc.start()


@api.get("/v1/init")
async def init(request, collection: str):
    """
    init collection with training, saving model, and getting retrieval
    :param request:
    :param collection:
    :return:
    """
    log.info('api/v1/init?collection=%s' % collection)
    global IRM
    global CONFIGSET
    global TB_DB
    global MODEL
    global RETRIEVAL

    rmsg = benedict(dict())
    try:
        url_dic = request.GET.copy()
        action_params = "&".join(["{}={}".format(k, v) for k, v in url_dic.items()])

        if not url_dic:
            info = {'error': 'Follow under command!',
                   '/v1/init?collection=ALL': 'initiate all collections',
                   '/v1/init?collection=oj_kn': 'initiate collection oj_kn',
                   }
            return info

        if 'collection' in url_dic:
            url_collecton = url_dic.get('collection', '')
            coll = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=url_collecton)
            rmsg = {
                'action': '/v1/init?%s' % action_params,
                'collection': coll,
            }
            if url_collecton and tqdm(coll):
                if url_collecton == 'ALL':  # init ALL collections
                    try:
                        irm_ = IrManager()
                        configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
                        tb_df_ = irm_.get_tb_df_by_collection(None, configset_)
                        model_ = irm_.train_and_save_by_collection(None, tb_df_, configset_, dict(),
                                                                   saveflag=True,  # save model file
                                                                   dirresetflag=True  # make new recent directory
                                                                   )
                        retrieval_ = irm_.get_retrieval_by_collections(None, tb_df_, configset_, model_)
                        CONFIGSET.update(configset_)
                        TB_DB.update(tb_df_)
                        MODEL.update(model_)
                        RETRIEVAL.update(retrieval_)
                        rmsg['msg'] = 'initiated all collection'
                    except Exception as e:
                        rmsg['error'] = str(e)
                        log.error(rmsg)
                        return rmsg
                else:
                    irm_ = IrManager()
                    configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
                    tb_df_ = irm_.get_tb_df_by_collection(collection, configset_)
                    model_ = irm_.train_and_save_by_collection(collection, tb_df_, configset_, dict(),
                                                               saveflag=True,  # save model file
                                                               dirresetflag=False  # no make new recent directory
                                                               )
                    retrieval_ = irm_.get_retrieval_by_collections(collection, tb_df_, configset_, model_)
                    CONFIGSET.update(configset_)
                    TB_DB.update(tb_df_)
                    MODEL.update(model_)
                    RETRIEVAL.update(retrieval_)
                    rmsg['msg'] = 'initiated the collection %s' % collection
            else:
                err = {
                        'action': '/v1/init?%s' % action_params,
                        'error': 'There is no collection %s' % url_collecton,
                        'collection': coll,
                }
                log.error(str(err))
                return err

        if TB_DB:
            rmsg['TB_DB'] = str(TB_DB)
        if MODEL:
            rmsg['MODEL'] = str(MODEL)
        if RETRIEVAL:
            rmsg['RETRIEVAL'] = str(RETRIEVAL)

    except Exception as e:
        rmsg['error'] = str(e)
        log.error(rmsg)
        return rmsg

    return rmsg


@api.get("/v1/start")
async def start(request, collection: str):
    """
    start collection with loading model but not training
    :param request:
    :param collection:
    :return:
    """
    log.info('api/v1/start?collection=%s' % collection)
    global IRM
    global TB_DB
    global RETRIEVAL
    global MODEL
    global CONFIGSET

    rmsg = benedict(dict())
    url_dic = request.GET.copy()
    url_dic_d = dict(url_dic)
    action_params = "&".join(["{}={}".format(k, v) for k, v in url_dic_d.items()])
    log.info('action_params:%s' % url_dic_d)
    try:
        if 'collection' in url_dic:
            url_collecton = url_dic.get('collection', '')
            coll = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=url_collecton)
            rmsg = {
                'action': '/v1/start?%s' % action_params,
                'collection': coll,
            }
            if url_collecton and tqdm(coll):
                if url_collecton == 'ALL':  # start ALL collections
                    try:
                        irm_ = IrManager()
                        configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
                        tb_df_ = irm_.get_tb_df_by_collection(None, configset_)
                        model_ = irm_.load_models_by_collections(None, configset_, dict())
                        retrieval_ = irm_.get_retrieval_by_collections(None, tb_df_, configset_, model_)
                        CONFIGSET.update(configset_)
                        TB_DB.update(tb_df_)
                        MODEL.update(model_)
                        RETRIEVAL.update(retrieval_)
                        rmsg['msg'] = 'start all collection'
                    except Exception as e:
                        rmsg['error'] = str(e)
                        log.error(rmsg)
                        return rmsg
                else:
                    irm_ = IrManager()
                    configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
                    tb_df_ = irm_.get_tb_df_by_collection(collection, configset_)
                    model_ = irm_.load_models_by_collections(collection, configset_, dict())
                    retrieval_ = irm_.get_retrieval_by_collections(collection, tb_df_, configset_, model_)
                    CONFIGSET.update(configset_)
                    TB_DB.update(tb_df_)
                    MODEL.update(model_)
                    RETRIEVAL.update(retrieval_)
                    rmsg['msg'] = 'start the collection %s' % collection
            else:
                err = {
                    'action': '/v1/start?%s' % action_params,
                    'error': 'There is no collection %s' % url_collecton,
                    'collection': coll,
                }
                log.error(str(err))
                return err

        if TB_DB:
            rmsg['TB_DB'] = str(TB_DB)
        if MODEL:
            rmsg['MODEL'] = str(MODEL)
        if RETRIEVAL:
            rmsg['RETRIEVAL'] = str(RETRIEVAL)

    except Exception as e:
        rmsg['error'] = str(e)
        log.error(rmsg)
        return rmsg
    return rmsg


@api.get("/v1/refresh")
async def refresh(request, collection: str):
    """
    refresh collection without re-model
    :param request:
    :param collection:
    :return:
    """
    log.info('api/v1/refresh?collection=%s' % collection)
    global IRM
    global TB_DB
    global RETRIEVAL
    global MODEL
    global CONFIGSET


    rmsg = benedict(dict())
    url_dic = request.GET.copy()
    url_dic_d = dict(url_dic)
    action_params = "&".join(["{}={}".format(k, v) for k, v in url_dic_d.items()])
    log.info('action_params:%s' % url_dic_d)
    if not MODEL:
        err = {
            'action': '/v1/refresh?%s' % action_params,
            'collection': collection,
            'error': 'There is no model. Init or start "%s" collection.' % collection
        }
        log.error(str(err))
        return err

    try:
        if 'collection' in url_dic:
            url_collecton = url_dic.get('collection', '')
            coll = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=url_collecton)
            rmsg = {
                'action': '/v1/refresh?%s' % action_params,
                'collection': coll,
            }
            if url_collecton and tqdm(coll):
                if url_collecton == 'ALL':  # refresh ALL collections
                    try:
                        irm_ = IrManager()
                        configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
                        tb_df_ = irm_.get_tb_df_by_collection(None, configset_)
                        retrieval_ = irm_.get_retrieval_by_collections(None, tb_df_, configset_, MODEL)
                        CONFIGSET.update(configset_)
                        TB_DB.update(tb_df_)
                        RETRIEVAL.update(retrieval_)
                        rmsg['msg'] = 'refresh all collection'
                    except Exception as e:
                        rmsg['error'] = str(e)
                        log.error(rmsg)
                        return rmsg
                else:
                    irm_ = IrManager()
                    configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
                    tb_df_ = irm_.get_tb_df_by_collection(collection, configset_)
                    retrieval_ = irm_.get_retrieval_by_collections(collection, tb_df_, configset_, MODEL)
                    CONFIGSET.update(configset_)
                    TB_DB.update(tb_df_)
                    RETRIEVAL.update(retrieval_)
                    rmsg['msg'] = 'refresh "%s" collection. ' % collection
            else:
                err = {
                    'action': '/v1/refresh?%s' % action_params,
                    'error': 'There is no collection - %s' % url_collecton,
                    'collection': coll,
                }
                log.error(str(err))
                return err

        if TB_DB:
            rmsg['TB_DB'] = str(TB_DB)
        if MODEL:
            rmsg['MODEL'] = str(MODEL)
        if RETRIEVAL:
            rmsg['RETRIEVAL'] = str(RETRIEVAL)

    except Exception as e:
        rmsg['error'] = str(e)
        log.error(rmsg)
        return rmsg
    return rmsg

"""
http://127.0.0.1:8800/api/v1/propose?q=인터넷휴대폰 기가지니
"""
@api.get("/v1/propose")
async def propose(request, q: str):
    log.info('api/v1/propose?q=%s' % q)
    st = timeit.default_timer()
    global IRM
    global TB_DB
    global RETRIEVAL
    global MODEL
    global CONFIGSET
    global MECAB

    rmsg = {"q": q,
     'propose_q': '',
     }

    q = q.strip()
    print('q:%s' % q)
    q_mecab_nouns = MECAB.nouns(q)
    print('q_mecab_nouns:%s' % q_mecab_nouns)
    rmsg['q_mecab_nouns'] = q_mecab_nouns
    q_splits = q.split()
    rmsg['q_splits'] = q_splits
    print('q_splits:%s' % q_splits)
    propose_q = ''

    try:
        if not TB_DB:
            rmsg['propose_q'] = ''
            rmsg['error'] = 'there is no data on TB_DB'

        else:
            if TB_DB['propose']:
                tb_df_propose = TB_DB['propose']['bibl']
                glossary_all_l = tb_df_propose['bible_bcn'].values.tolist()
                glossary_match_l = list()
                for value in glossary_all_l:
                    print(value)
                    if q.find(value) > -1:
                        glossary_match_l.append(value)
                        print(value)
                print(glossary_match_l)
                rmsg['propose_q'] = ' '.join(glossary_match_l)

    except Exception as e:
        jobtime = str(timeit.default_timer() - st)
        log.error(str(e))
        rmsg['propose_q'] = ''
        rmsg['error'] = str(e)
        rmsg['jobtime'] = jobtime
        return rmsg
    jobtime = str(timeit.default_timer() - st)
    rmsg['jobtime'] = jobtime

    if TB_DB:
        rmsg['TB_DB'] = str(TB_DB)
    if MODEL:
        rmsg['MODEL'] = str(MODEL)
    if RETRIEVAL:
        rmsg['RETRIEVAL'] = str(RETRIEVAL)

    return rmsg


@api.get("/v1/{id}/search")
async def search(request, id: str, q: str):
    log.info('api/%s/search?q=%s' % (id, q))
    url_dic = request.GET.copy()
    url_dic_d = dict(url_dic)
    # action_params = "&".join(["{}={}".format(k, v) for k, v in url_dic_d.items()])
    log.info('action_params:%s' % url_dic_d)

    global IRM
    global TB_DB
    global RETRIEVAL
    global MODEL
    global CONFIGSET

    try:
        if not RETRIEVAL:
            # jobsc.job_api_v1_start()
            if not TB_DB and not MODEL and not RETRIEVAL and not CONFIGSET:
                # jobsc.job_api_v1_init()
                if not RETRIEVAL:
                    err = {'error': 'There is fatal error on system. Check the system and call system admin! when exec collection - %s' % id}
                    return err

        if RETRIEVAL:
            if not RETRIEVAL.get(id, None):
                return {'error': 'There is no %s RETRIEVAL in collection. Set start the collection' % id}

        collection = dict()
        if CONFIGSET:
            err = CONFIGSET.get('error', None)
            if err:
                log.error(err)
                return err
            collection = CONFIGSET.get(id, None)
    except Exception as e:
        solr_json = {"error": "%s" % str(e)}
        log.info('e:%s' % solr_json)
        return solr_json

    if not collection:
        try:
            collection = CONFIGSET.get(id, {})
        except Exception as e:
            solr_json = {"error": "%s" % str(e)}
            log.info(solr_json)

    # q = ' '.join(tokenize_by_morpheme_char(q))
    log.info('(q):%s' % q)
    log.info('jamo_sentence(q):%s' % jamo_sentence(q))
    try:
        sparser = SolrAPIParser()
        solr_kwargs_url_params = sparser.query_parse_nofacet(request, q)

        log.info('solr_kwargs_url_params: %s' % solr_kwargs_url_params)
        solr_json = {
            "responseHeader": {
                "status": 0,
                "Qtime": 0,
                "params": solr_kwargs_url_params
            },
        }

        default_k = None
        solr_json = IRM.get_query_results(q=q, id=id, retrievals=RETRIEVAL,
                                              tb_df=TB_DB, k=default_k,
                                              solr_kwargs=solr_kwargs_url_params, collection=collection, solr_json=solr_json)
        solr_json['responseHeader']['status'] = 200
    except Exception as e:
        solr_json = {"error": "%s" % str(e)}
        log.info('e:%s' % solr_json)
        return solr_json

    return solr_json


@api.get("/v1/show")
async def show(request):
    collections = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
    global CONFIGSET
    global TB_DB
    global MODEL
    global RETRIEVAL

    if collections:
        rmsg = {
                'action': '/v1/show',
                'collection': collections,
                }
    else:
        rmsg = {
                'action': '/v1/show',
                'collection': 'There is no collections on collection.yml. Set the /configset/conllection.yml',
                }

    if CONFIGSET:
        rmsg['CONFIGSET'] = str(CONFIGSET)
    if TB_DB:
        rmsg['TB_DB'] = str(TB_DB)
    if MODEL:
        rmsg['MODEL'] = str(MODEL)
    if RETRIEVAL:
        rmsg['RETRIEVAL'] = str(RETRIEVAL)
    return rmsg


@api.get("/v1/help")
async def help(request):
    help = {
        'eg. /api/v1/help': 'explain help',
        'eg. /api/v1/show': "show all collections's configset",
        'eg. /api/v1/init?collection=ALL': 'init all collections',
        'eg. /api/v1/start?collection=oj_kn': 'start oj_kn collection',
        'eg. /api/v1/refresh?collection=oj_kn': 'refresh oj_kn collection',
        'eg. /api/v1/oj_kn/search?q=인터넷폰 기가지니': 'retrieve oj_kn collection',
    }
    return help

"""
http://127.0.0.1:8800/api/v1/morph?q=고양이가 냐 하고 울면 나는 녜 하고 울어야지
"""
@api.get("/v1/morph")
async def morph(request, q: str):
    log.info('api/v1/morph?q=%s' % q)
    st = timeit.default_timer()
    try:
        pos, nouns, morphs = q2morph(q)
        jobtime = str(timeit.default_timer() - st)
    except Exception as e:
        jobtime = str(timeit.default_timer() - st)
        log.error(str({'error': str(e), 'jobtime': jobtime}))
        return {'error': str(e), 'jobtime': jobtime}
    return {"q": q,
            'jobtime': jobtime,
            "pos": pos,
            "nouns": nouns,
            "morphs": morphs,
            }


"""
/api/scheduler.py
http://127.0.0.1:8800/api/v1/scheduler?job=init&action=start
http://127.0.0.1:8800/api/v1/scheduler?job=start&action=stop
http://127.0.0.1:8800/api/v1/scheduler?job=refresh&action=stop
"""
@api.get("/v1/scheduler")
async def scheduler(request, job: str, action: str):
    log.info('api/v1/scheduler?job=%s&action=%s' % (job, action))
    st = timeit.default_timer()
    global JOB

    try:
        if job == 'init' and action == 'start':
            JOB.job_api_v1_init()
        elif job == 'init' and action == 'stop':
            JOB.kill_scheduler('init')
        if job == 'start' and action == 'start':
            JOB.job_api_v1_start()
        elif job == 'start' and action == 'stop':
            JOB.kill_scheduler('start')
        if job == 'refresh' and action == 'start':
            JOB.job_api_v1_refresh()
        elif job == 'refresh' and action == 'stop':
            JOB.kill_scheduler('refresh')
    except Exception as e:
        jobtime = str(timeit.default_timer() - st)
        log.error(str({'error': str(e), 'jobtime': jobtime}))
        return {'error': str(e), 'jobtime': jobtime}

    jobtime = str(timeit.default_timer() - st)
    rmsg = {"scheduler": job,
            'action': action,
            'jobtime': jobtime,
            }
    log.info(rmsg)
    return rmsg






# async def propose(request, q: str):
#     log.info('api/v1/propose?q=%s' % q)
#     global IRM
#     global CONFIGSET
#     global TB_DB
#     global MODEL
#     global RETRIEVAL
#
#     global RETRIEVAL_ALL
#     global LOADEDMODEL_ALL
#     global VOCADOCS_ALL
#
#     try:
#         retrievals_ = RETRIEVAL_ALL
#         loaded_model_ = LOADEDMODEL_ALL
#
#         voca_retrieval = retrievals_
#         voca_model = loaded_model_
#         vvoca_docs_d = VOCADOCS_ALL
#         vvoc_l = list(vvoca_docs_d.keys())
#         # print('===== start ==== copus vocas ==========')
#         # print('vvoc_l:%s' % vvoc_l)
#         # print('===== end ==== copus vocas ==========')
#     except Exception as e:
#         error = {"error": "%s" % str(e)}
#         log.info('e:%s' % error)
#         log.error(str(error))
#         return error
#
#     log.info('api/v1/propose?q=%s' % q)
#     st = timeit.default_timer()
#     try:
#         propose_q = get_q2propose_multi_by_query(q, voca_retrieval, vvoca_docs_d)
#         jobtime = str(timeit.default_timer() - st)
#     except Exception as e:
#         jobtime = str(timeit.default_timer() - st)
#         log.info('e:%s' % e)
#         log.error(str(e))
#         return {'error': str(e), 'jobtime': jobtime}
#     return {"q": q,
#             'jobtime': jobtime,
#             "propose_q": propose_q,
#             }















#"""
# 0.set set configset /configset/collection.xml
# 1.exec [train+retrieval] job start by api : http://127.0.0.1:8800/api/{collection}/job?action=start
# 2.exec search by api : http://127.0.0.1:8800/api/collection01/search?q=하나님께서 세상을 창조&start=0&rows=10
# 3.exec [retrieval]job restart by api : http://127.0.0.1:8800/api/{collection}/job?action=restart
# """
# @api.get("/v1/{collection}/job")
# def job(request, collection: str, action: str):
#     log.info('api/v1/%s/job?action=%s' % (collection, action))
#     s = timeit.default_timer()
#     global IRM
#     global TB_DB
#     global RETRIEVAL
#     global MODEL
#     global CONFIGSET
#
#     global RETRIEVAL_ALL
#     global LOADEDMODEL_ALL
#     global VOCADOCS_ALL
#
#     url_dic = request.GET.copy()
#     action_params = "&".join(["{}={}".format(k, v) for k, v in url_dic.items()])
#
#     try:
#         configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
#     except Exception as e:
#         solr_json = {"error": "%s" % str(e)}
#         log.error(str(solr_json))
#         return solr_json
#
#     coll = configset_.get(collection, {})
#
#     if coll:
#         mode = coll.get('mode', None)
#         analyzer = coll.get('analyzer', None)
#         table = coll.get('table', None)
#         modeltype = coll.get('modeltype', [FastText])
#         columns = coll.get('columns', [])
#         docid = coll.get('docid', None)
#         fl = coll.get('fl', None)
#         sort = coll.get('sort', None)
#         rows = coll.get('rows', None)
#         df = coll.get('df', None)
#     else:
#         err = {'error': 'There is no collection for %s' % collection}
#         log.error(str(err))
#         return err
#
#     irm_ = IrManager()
#     retrieval_ = dict()
#     model_ = dict()
#     tb_df_ = irm_.get_tb_df_by_collection(coll_key=collection, configset=configset_, pklsave=False)
#     # tb_df_ = tb_df_[0:500]
#
#     if not MODEL or not MODEL.get(collection, None):
#         model_ = irm_.load_models_by_collections(collection, configset_, dict())
#     try:
#         if action == 'start':
#             msg = 'job : action=start : train, save and load model'
#             collection_models = irm_.train_and_save_by_collection(id, tb_df_, configset_, model_, saveflag=True)
#             # vec_models = IRM_.async_train_models(vmodel[0], tb_df_, columns, analyzer, collection)
#             # IRM_.aync_save_models(vec_models, vmodel[0], table, columns)
#         elif action == 'restart':
#             msg = 'job restart load retrieval_*'
#         elif action == 'propose':
#             # add 'ALL' column for voca
#             dfconcat(tb_df_, columns, sep=' ', name='ALL')
#             columns.append('ALL')
#
#             msg = 'job propose load retrieval_all'
#             modeltype = 'fasttext'
#             vmodel = [FastText]
#             columns = ['ALL']
#             _, LOADEDMODEL_ALL_ = irm_.set_init_models_and_get_retrievals(
#                 mode,
#                 vmodel,
#                 table,
#                 docid,
#                 columns,
#                 tb_df_,
#                 onlymodel=True
#             )
#             vaca_model = LOADEDMODEL_ALL_['ALL']
#             vvoca_docs_d = LOADEDMODEL_ALL_['ALL'].wv.vocab
#             vocab_len = len(vvoca_docs_d)
#             print('total vvoc_l vocab_len = %s' % vocab_len)
#
#             vvoc_l = list(vvoca_docs_d.keys())
#             print('total vvoc_l count = %s' % vvoc_l)
#
#             print('===== start ==== copus vocas ==========')
#             print('vvoc_l:%s' % vvoc_l)
#             print('===== end ==== copus vocas ==========')
#             q = jamo_sentence('후대폰 하니님 kt')
#
#             # wcd
#             # match_op = Matching()
#             # wcd = WordCentroidDistance(load_ft_model.wv)
#             # vvoc_retrieval = Retrieval(wcd, matching=match_op, labels=vvoc_l)
#             # vvoc_retrieval.fit(vvoc_l)
#
#             # combination
#             tfidf = Tfidf()
#             tfidf.fit(vvoc_l)
#
#             wcd = WordCentroidDistance(vaca_model.wv)
#             wcd.fit(vvoc_l)
#
#             # # they can operate on different feilds
#             match_op = Matching().fit(vvoc_l)
#             combined = wcd + tfidf ** 2
#             vvoc_retrieval = Retrieval(combined, matching=match_op, labels=vvoc_l)
#             RETRIEVAL_ALL_ = vvoc_retrieval
#             VOCADOCS_ALL_ = vvoca_docs_d
#
#             RETRIEVAL_ALL.update(RETRIEVAL_ALL_)
#             LOADEDMODEL_ALL.update(LOADEDMODEL_ALL_)
#             VOCADOCS_ALL.update(VOCADOCS_ALL_)
#
#         if not action == 'propose':
#             retrieval_ = irm_.get_retrieval_by_collections(collection, tb_df_, configset_, model_)
#
#             # RETRIEVALS_, LOADEDMODEL_ = IRM_.set_init_models_and_get_retrievals(
#             #     mode,
#             #     vmodel,
#             #     table,
#             #     docid,
#             #     columns,
#             #     tb_df_,
#             #     onlymodel=False
#             # )
#
#     except Exception as e:
#         jobtime = timeit.default_timer() - s
#         err = {'error': str(e), 'jobtime': jobtime}
#         print('e:%s' % err)
#         log.error(str(err))
#         return err
#
#     IRM = irm_
#     CONFIGSET.update(configset_)
#     TB_DB.update(tb_df_)
#     RETRIEVAL.update(retrieval_)
#     MODEL.update(model_)
#
#     jobtime = timeit.default_timer() - s
#     action = '/v1/%s/job?%s' % (collection, action_params)
#     rmsg = {'msg': msg,
#             'action': action,
#             'jobtime': jobtime,
#             'collection': collection,
#             'configset': configset_,
#         }
#     return rmsg