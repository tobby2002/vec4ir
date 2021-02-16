from datetime import date
from ninja import Router
from typing import List
from pydantic import BaseModel
from django.shortcuts import get_object_or_404
from .models import Event

import os, sys, timeit
import urllib.request
import json
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
log = logz()
api = NinjaAPI(version='1.0.0')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

IRM = IrManager()
CONFIGSET = dict()
TB_DB = None
MODEL = dict()
COLLECTION = dict()
RETRIEVAL = dict()

"""
http://127.0.0.1:8777/api/v1/init
"""
@api.get("/v1/init")
def job(request):
    global IRM
    global CONFIGSET
    global TB_DB
    global MODEL
    global RETRIEVAL

    CONFIGSET = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
    rmsg = {'msg': '/v1/api init',
     'action': 'init',
     'configset': CONFIGSET,
     }
    log.info(str(rmsg))
    return rmsg


"""
http://127.0.0.1:8777/api/v1/morph?q=고양이가 냐 하고 울면 나는 녜 하고 울어야지
"""
@api.get("/v1/morph")
def job(request, q: str):
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
http://127.0.0.1:8777/api/v1/propose?q=후대폰 플랜을 알려줘
"""
@api.get("/v1/{id}/propose")
def job(request, id: str, q: str):
    log.info('api/%s/propose?q=%s' % (id, q))
    global IRM
    global CONFIGSET
    global TB_DB
    global MODEL
    global RETRIEVAL

    global RETRIEVAL_ALL
    global LOADEDMODEL_ALL
    global VOCADOCS_ALL

    try:
        retrievals_ = RETRIEVALS_ALL
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
        print('e:%s' % error)
        log.error(str(error))

        return error

    log.info('api/v1/propose?q=%s' % q)
    st = timeit.default_timer()
    try:
        propose_q = get_q2propose_multi_by_query(q, voca_retrieval, vvoca_docs_d)
        jobtime = str(timeit.default_timer() - st)
    except Exception as e:
        jobtime = str(timeit.default_timer() - st)
        print('e:%s' % e)
        log.error(str(e))
        return {'error': str(e), 'jobtime': jobtime}
    return {"q": q,
            'jobtime': jobtime,
            "propose_q": propose_q,
            }


"""
0.set set configset /configset/collection.xml
1.exec [train+retrieval] job start by api : http://127.0.0.1:8777/api/{id}/job?action=start
2.exec search by api : http://127.0.0.1:8777/api/collection01/search?q=하나님께서 세상을 창조&start=0&rows=10
3.exec [retrieval]job restart by api : http://127.0.0.1:8777/api/{id}/job?action=restart
"""
@api.get("/v1/{id}/job")
def job(request, id: str, action: str):
    log.info('api/v1/%s/job?action=%s' % (id, action))
    s = timeit.default_timer()

    global IRM
    global TB_DB
    global RETRIEVAL
    global MODEL
    global CONFIGSET

    global LOADEDMODEL
    global RETRIEVALS_ALL
    global LOADEDMODEL_ALL
    global VOCADOCS_ALL

    configset_ = None

    if CONFIGSET:
        err = CONFIGSET.get('error', None)
        configset_ = CONFIGSET
        if err:
            print('e:%s' % err)
            log.error(str(err))
            return err
    else:
        try:
            urllib.request.urlopen("http://127.0.0.1:8777/api/v1/init").read()
            CONFIGSET = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
            configset_ = CONFIGSET
        except Exception as e:
            solr_json = {"error": "%s" % str(e)}
            print('e:%s' % solr_json)
            log.error(str(solr_json))

    collection = configset_.get('configset', {}).get(id, {})

    if collection:
        mode = collection.get('mode', None)
        analyzer = collection.get('analyzer', None)
        table = collection.get('table', None)
        modeltype = collection.get('modeltype', [FastText])
        columns = collection.get('columns', [])
        docid = collection.get('docid', None)
        fl = collection.get('fl', None)
        sort = collection.get('sort', None)
        rows = collection.get('rows', None)
        df = collection.get('df', None)
    else:
        e = {'error': 'There is no collection in job action - "%s"' % id}
        print('e:%s' % e)
        log.error(str(e))
        return e

    IRM_ = IrManager()
    if modeltype == 'fasttext':
        vmodel = [FastText]
    else:
        vmodel = [Word2Vec]

    tb_df = IRM_.get_tb_df(table=table, pklsave=False)
    # tb_df = tb_df[0:500]

    # add 'ALL' column for voca
    dfconcat(tb_df, columns, sep=' ', name='ALL')
    columns.append('ALL')

    RETRIEVALS_ = None
    LOADEDMODEL_ = None
    RETRIEVALS_ALL_ = None
    LOADEDMODEL_ALL_ = None
    VOCADOCS_ALL_ = None

    if not MODEL:
        MODEL = IRM_.load_models_by_collections(id, CONFIGSET, MODEL)
    try:
        if action == 'start':
            msg = 'job : action=start : train, save and load model'
            collection_models = IRM_.train_and_save_collections(id, tb_df, CONFIGSET, MODEL, saveflag=True)
            # vec_models = IRM_.async_train_models(vmodel[0], tb_df, columns, analyzer, collection)
            # IRM_.aync_save_models(vec_models, vmodel[0], table, columns)

        elif action == 'restart':
            msg = 'job restart load retrieval_*'
        elif action == 'propose':
            msg = 'job propose load retrieval_all'
            modeltype = 'fasttext'
            vmodel = [FastText]
            columns = ['ALL']
            _, LOADEDMODEL_ALL_ = IRM_.set_init_models_and_get_retrievals(
                mode,
                vmodel,
                table,
                docid,
                columns,
                tb_df,
                onlymodel=True
            )
            vaca_model = LOADEDMODEL_ALL_['ALL']
            vvoca_docs_d = LOADEDMODEL_ALL_['ALL'].wv.vocab
            vocab_len = len(vvoca_docs_d)
            print('total vvoc_l vocab_len = %s' % vocab_len)

            vvoc_l = list(vvoca_docs_d.keys())
            print('total vvoc_l count = %s' % vvoc_l)

            print('===== start ==== copus vocas ==========')
            print('vvoc_l:%s' % vvoc_l)
            print('===== end ==== copus vocas ==========')
            q = jamo_sentence('후대폰 하니님 kt')

            # wcd
            # match_op = Matching()
            # wcd = WordCentroidDistance(load_ft_model.wv)
            # vvoc_retrieval = Retrieval(wcd, matching=match_op, labels=vvoc_l)
            # vvoc_retrieval.fit(vvoc_l)

            # combination
            tfidf = Tfidf()
            tfidf.fit(vvoc_l)

            wcd = WordCentroidDistance(vaca_model.wv)
            wcd.fit(vvoc_l)

            # # they can operate on different feilds
            match_op = Matching().fit(vvoc_l)
            combined = wcd + tfidf ** 2
            vvoc_retrieval = Retrieval(combined, matching=match_op, labels=vvoc_l)
            RETRIEVALS_ALL_ = vvoc_retrieval
            VOCADOCS_ALL_ = vvoca_docs_d

        if not action == 'propose':
            RETRIEVALS_ = IRM_.get_retrievals_by_collections(id, tb_df, CONFIGSET, MODEL)

            # RETRIEVALS_, LOADEDMODEL_ = IRM_.set_init_models_and_get_retrievals(
            #     mode,
            #     vmodel,
            #     table,
            #     docid,
            #     columns,
            #     tb_df,
            #     onlymodel=False
            # )
    except Exception as e:
        jobtime = timeit.default_timer() - s
        err = {'error': str(e), 'jobtime': jobtime}
        print('e:%s' % err)
        log.error(str(err))
        return err
    finally:
        IRM = IRM_
        TB_DB = tb_df
        RETRIEVAL = RETRIEVALS_
        LOADEDMODEL = LOADEDMODEL_
        RETRIEVALS_ALL = RETRIEVALS_ALL_
        LOADEDMODEL_ALL = LOADEDMODEL_ALL_
        VOCADOCS_ALL = VOCADOCS_ALL_
        mode = mode
        CONFIGSET = configset_
    jobtime = timeit.default_timer() - s

    rmsg = {'msg': msg,
        'action': action,
        'mode': mode,
        'taken time': jobtime,
        'collection': id,
        '%s set' % id: collection,
        'collection.yml': configset_,
     }
    return rmsg


@api.get("/v1/{id}/delete")
def job(request, id: str, q: str):
    log.info('api/%s/job?q=%s' % (id, q))
    msg = 'job delete'
    jobname = 'delete job'
    RETRIEVAL = None
    rmsg = {'msg': msg,
     'jobname': jobname,
     }
    return rmsg


@api.get("/v1/{id}/search")
def search(request, id: str, q: str):
    log.info('api/%s/search?q=%s' % (id, q))
    global IRM
    global TB_DB
    global RETRIEVAL
    global LOADEDMODEL
    global mode
    global CONFIGSET

    if not RETRIEVAL:
        return {'error': 'There is no RETRIEVAL'}

    collection = dict()
    if CONFIGSET:
        err = CONFIGSET.get('error', None)
        if err:
            print(err)
            return err
        collection = CONFIGSET.get('configset', {}).get(id, None)

    if not collection:
        try:
            contents = urllib.request.urlopen("http://127.0.0.1:8777/api/v1/init").read()
            contents_dict = json.loads(contents.decode('utf-8'))
            CONFIGSET = contents_dict.get('configset', {})
            collection = CONFIGSET.get('configset', {}).get(id, {})
        except Exception as e:
            solr_json = {"error": "%s" % str(e)}
            print(solr_json)

    # q = ' '.join(tokenize_by_morpheme_char(q))
    print('(q):%s' % q)
    print('jamo_sentence(q):%s' % jamo_sentence(q))
    try:
        sparser = SolrAPIParser()
        solr_kwargs_url_params = sparser.query_parse_nofacet(request, q)

        log.info('solr_kwargs_url_params: %s' % solr_kwargs_url_params)
        print('solr_kwargs_url_params:%s' % solr_kwargs_url_params)

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
        print('e:%s' % solr_json)
        return solr_json

    return solr_json

# router = Router()
#
#
# class EventSchema(BaseModel):
#     title: str
#     start_date: date
#     end_date: date
#
#     class Config:
#         orm_mode = True
#
#
# @router.post("/create")
# def create_event(request, event: EventSchema):
#     Event.objects.create(**event.dict())
#     return event
#
#
# @router.get("", response=List[EventSchema])
# def list_events(request):
#     return list(Event.objects.all())
#
#
# @router.get("/{id}", response=EventSchema)
# def get_event(request, id: int):
#     event = get_object_or_404(Event, id=id)
#     return event
