from datetime import date
from ninja import Router
from typing import List
from pydantic import BaseModel
from django.shortcuts import get_object_or_404

import os, sys, timeit
import urllib.request
import json
from tqdm import tqdm
from benedict import benedict
from util.solrapiparser import SolrAPIParser
from util.utilmanager import get_configset, q2morph, jamo_sentence, dfconcat
from util.apidefmanager import get_q2propose_multi_by_query
from ir.irmanager import IrManager
from ir.word2vec import WordCentroidDistance
from ir.base import Matching, Tfidf
from ir.core import Retrieval
from gensim.models import Word2Vec, FastText, Doc2Vec
from ninja import NinjaAPI
from util.logmanager import logz
from api.scheduler import Scheduler
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
jobsc.start()


@api.get("/v1/init")
def init(request, collection: str):
    log.info('api/v1/init?collection=%s' % collection)
    global IRM
    global CONFIGSET
    global TB_DB
    global MODEL
    global RETRIEVAL

    rmsg = benedict(dict())
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
                    CONFIGSET = configset_
                    TB_DB = tb_df_
                    MODEL = model_
                    RETRIEVAL = retrieval_
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
                    'action': '/v1/action?%s' % action_params,
                    'error': 'There is no collection %s' % url_collecton,
                    'collection': coll,
            }
            log.error(str(err))
            return err
    return rmsg


@api.get("/v1/start")
def start(request, collection: str):
    log.info('api/v1/start?collection=%s' % collection)
    global IRM
    global TB_DB
    global RETRIEVAL
    global MODEL
    global CONFIGSET

    rmsg = benedict(dict())
    url_dic = request.GET.copy()
    action_params = "&".join(["{}={}".format(k, v) for k, v in url_dic.items()])

    if 'collection' in url_dic:
        url_collecton = url_dic.get('collection', '')
        coll = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=url_collecton)
        rmsg = {
            'action': '/v1/start?%s' % action_params,
            'collection': coll,
        }
        if url_collecton and tqdm(coll):
            if url_collecton == 'ALL':  # init ALL collections
                try:
                    irm_ = IrManager()
                    configset_ = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
                    tb_df_ = irm_.get_tb_df_by_collection(None, configset_)
                    model_ = irm_.load_models_by_collections(None, configset_, dict())
                    retrieval_ = irm_.get_retrieval_by_collections(None, tb_df_, configset_, model_)
                    CONFIGSET = configset_
                    TB_DB = tb_df_
                    MODEL = model_
                    RETRIEVAL = retrieval_
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
                'action': '/v1/action?%s' % action_params,
                'error': 'There is no collection %s' % url_collecton,
                'collection': coll,
            }
            log.error(str(err))
            return err
    return rmsg


@api.get("/v1/{id}/search")
async def search(request, id: str, q: str):
    log.info('api/%s/search?q=%s' % (id, q))
    url_dic = request.GET.copy()
    action_params = "&".join(["{}={}".format(k, v) for k, v in url_dic.items()])
    log.info('action_params:%s' % action_params)

    global IRM
    global TB_DB
    global RETRIEVAL
    global MODEL
    global CONFIGSET

    if not RETRIEVAL:
        jobsc.job_api_v1_start()
        if not TB_DB and not MODEL and not RETRIEVAL and not CONFIGSET:
            jobsc.job_api_v1_init()
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
        solr_json = IRM.get_query_results(q=jamo_sentence(q), id=id, retrievals=RETRIEVAL,
                                              tb_df=TB_DB, k=default_k,
                                              solr_kwargs=solr_kwargs_url_params, collection=collection, solr_json=solr_json)
        solr_json['responseHeader']['status'] = 200
    except Exception as e:
        solr_json = {"error": "%s" % str(e)}
        log.info('e:%s' % solr_json)
        return solr_json

    return solr_json


@api.get("/v1/show")
def show(request):
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
def help(request):
    help = {
        'action': '/api/v1/help',
        'eg. /api/v1/help': 'explain examples',
        'eg. /api/v1/show': "show all collections's configset",
        'eg. /api/v1/init?collection=ALL': 'initiate all collections',
        'eg. /api/v1/init?collection=oj_kn': 'initiate oj_kn collection',
        'eg. /api/v1/oj_kn/search': 'retrieve oj_kn collection',
    }
    return help

"""
http://127.0.0.1:8800/api/v1/morph?q=고양이가 냐 하고 울면 나는 녜 하고 울어야지
"""
@api.get("/v1/morph")
def morph(request, q: str):
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
http://127.0.0.1:8800/api/v1/propose?q=후대폰 플랜을 알려줘
"""
@api.get("/v1/{collection}/propose")
async def propose(request, collection: str, q: str):
    log.info('api/%s/propose?q=%s' % (collection, q))
    global IRM
    global CONFIGSET
    global TB_DB
    global MODEL
    global RETRIEVAL

    global RETRIEVAL_ALL
    global LOADEDMODEL_ALL
    global VOCADOCS_ALL

    try:
        retrievals_ = RETRIEVAL_ALL
        loaded_model_ = LOADEDMODEL_ALL

        voca_retrieval = retrievals_
        voca_model = loaded_model_
        vvoca_docs_d = VOCADOCS_ALL
        vvoc_l = list(vvoca_docs_d.keys())
        # print('===== start ==== copus vocas ==========')
        # print('vvoc_l:%s' % vvoc_l)
        # print('===== end ==== copus vocas ==========')
    except Exception as e:
        error = {"error": "%s" % str(e)}
        log.info('e:%s' % error)
        log.error(str(error))
        return error

    log.info('api/v1/propose?q=%s' % q)
    st = timeit.default_timer()
    try:
        propose_q = get_q2propose_multi_by_query(q, voca_retrieval, vvoca_docs_d)
        jobtime = str(timeit.default_timer() - st)
    except Exception as e:
        jobtime = str(timeit.default_timer() - st)
        log.info('e:%s' % e)
        log.error(str(e))
        return {'error': str(e), 'jobtime': jobtime}
    return {"q": q,
            'jobtime': jobtime,
            "propose_q": propose_q,
            }

# contents = urllib.request.urlopen("http://127.0.0.1:8800/api/v1/init").read()
# contents_dict = json.loads(contents.decode('utf-8'))
# CONFIGSET = contents_dict.get('configset', {})


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