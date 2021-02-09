from datetime import date
from ninja import Router
from typing import List
from pydantic import BaseModel
from django.shortcuts import get_object_or_404
from .models import Event

import os, sys, timeit
import urllib.request
import json
import pprint as pp
from util.logmanager import logger
from util.solrapiparser import SolrAPIParser
from util.utilmanager import get_configset
log = logger('ir', 'irmanager')



import config

from ninja import NinjaAPI
api = NinjaAPI(version='1.0.0')

from ir.irmanager import IrManager
from gensim.models import Word2Vec, FastText, Doc2Vec

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

IRM = IrManager()
TB_DB = None
RETRIEVALS = None
mode = None
CONFIGSET = None


@api.get("/v1/init")
def job(request):
    global IRM
    global TB_DB
    global RETRIEVALS
    global CONFIGSET

    CONFIGSET = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
    rmsg = {'msg': '/v1/api init',
     'action': 'init',
     'configset': CONFIGSET,
     }
    print(rmsg)
    return rmsg

@api.get("/v1/morph")
def job(request, q: str):
    log.info('api/v1/morph?q=%s' % q)
    return {"q": q,
            "pos": "pos values",
            "nouns": "nouns values",
            }

@api.get("/v1/propose")
def job(request, q: str):
    log.info('api/v1/propose?q=%s' % q)
    return {"q": q,
            "propose_q": "제안 검색어",
            }

"""
1.exec [train+retrieval] job start by api : http://127.0.0.1:8777/api/{id}/job?action=start
2.exec search by api : http://127.0.0.1:8777/api/collection01/search?q=하나님께서 세상을 창조&start=0&rows=10
3.exec [retrieval]job restart by api : http://127.0.0.1:8777/api/{id}/job?action=restart
4.exec [retrieval]job tfidf by api : http://127.0.0.1:8777/api/{id}/job?action=tfidf
"""
@api.get("/v1/{id}/job")
def job(request, id: str, action: str):
    log.info('api/v1/%s/job?action=%s' % (id, action))
    global IRM
    global TB_DB
    global RETRIEVALS
    global CONFIGSET

    _configset = None
    if CONFIGSET:
        err = CONFIGSET.get('error', None)
        _configset = CONFIGSET
        if err:
            print(err)
            return err
    else:
        try:
            urllib.request.urlopen("http://127.0.0.1:8777/api/v1/init").read()
            _configset = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)
        except Exception as e:
            solr_json = {"error": "%s" % str(e)}
            print(solr_json)


    collection = CONFIGSET.get('configset', {}).get(id, {})

    if collection:
        _mode = collection.get('mode', None)
        _table = collection.get('table', None)
        _modeltype = collection.get('modeltype', [FastText])
        _columns = collection.get('columns', [])
        _docid = collection.get('docid', None)
        _fl = collection.get('fl', None)
        _sort = collection.get('sort', None)
        _rows = collection.get('rows', None)
        _df = collection.get('df', None)
    else:
        return {'error': 'There is no collection in job - "%s"' % id}

    _IRM = IrManager()
    if _modeltype == 'fasttext':
        _vmodel = [FastText]
    else:
        _vmodel = [Word2Vec]

    _tb_df = _IRM.get_tb_df(table=_table, pklsave=False)
    # tb_df = tb_df[0:500]

    _RETRIEVALS = None
    jobtime = None
    try:
        if action == 'start':
            msg = 'job start'
            if not _mode:
                _mode = 'expansion'

            st = timeit.default_timer()
            jobname = 'retrieval'
            # word2vec
            if action:
                jobname = 'train + retrieval'
                vec_models = _IRM.train_models(_vmodel[0], _tb_df, _columns)
                # vec_models = fasttext.load_model(PROJECT_ROOT + os.sep + 'model' + os.sep + 'ft_morpheme_char_w_namu_nsmc.vec')
                # vec_models = fasttext.load_model(PROJECT_ROOT + os.sep + 'model' + os.sep + 'ft_morpheme_char_w_namu_nsmc.bin')
                _IRM.save_models(vec_models, _vmodel[0], _table, _columns, dirresetflag=True)

            try:
                _RETRIEVALS = _IRM.set_init_models_and_get_retrievals(_mode, _vmodel, _table, _docid, _columns, _tb_df)
            except Exception as e:
                jobtime = str(timeit.default_timer() - st)
                return {'error': str(e), 'jobtime': jobtime}
            jobtime = str(timeit.default_timer() - st)

            if not _RETRIEVALS:
                msg = 'no retrievals'
                jobname = 'start'
                jobtime = 0
        elif action == 'restart':
            msg = 'job restart'
            jobname = 'restart'
            if not _mode:
                mode = 'combination'
            st = timeit.default_timer()
            try:
                _RETRIEVALS = _IRM.set_init_models_and_get_retrievals(_mode, _vmodel, _table, _docid, _columns, _tb_df)
            except Exception as e:
                jobtime = str(timeit.default_timer() - st)
                return {'error': str(e), 'jobtime': jobtime}
            jobtime = str(timeit.default_timer() - st)
        elif action == 'tfidf':
            msg = 'job tfidf'
            jobname = 'tfidf'
            _mode = 'tfidf'
            st = timeit.default_timer()
            try:
                _RETRIEVALS = _IRM.set_init_models_and_get_retrievals(_mode, _vmodel, _table, _docid, _columns, _tb_df)
            except Exception as e:
                jobtime = str(timeit.default_timer() - st)
                return {'error': str(e), 'jobtime': jobtime}
            jobtime = str(timeit.default_timer() - st)
        else:
            msg = 'action init'
            action = 'init'
            jobtime = 0
            IRM = None
            RETRIEVALS = None
            CONFIGSET = get_configset(PROJECT_ROOT + os.sep + "configset", 'collection.yml', collection=None)

    except Exception as e:
        return {'error': str(e), 'action': 'start'}
    finally:
        IRM = _IRM
        TB_DB = _tb_df
        RETRIEVALS = _RETRIEVALS
        mode = _mode
        CONFIGSET = _configset

    rmsg = {'msg': msg,
        'action': action,
        'mode': mode,
        'taken time': jobtime,
        'collection': id,
        '%s set' % id: collection,
        'collection.yml': _configset,
     }
    print(rmsg)
    return rmsg

@api.get("/v1/{id}/delete")
def job(request, id: str, q: str):
    log.info('api/%s/job?q=%s' % (id, q))
    msg = 'job delete'
    jobname = 'delete job'
    RETRIEVALS = None
    rmsg = {'msg': msg,
     'jobname': jobname,
     }
    return rmsg


@api.get("/v1/{id}/search")
def search(request, id: str, q: str):
    log.info('api/%s/search?q=%s' % (id, q))
    st0 = timeit.default_timer()

    global IRM
    global TB_DB
    global RETRIEVALS
    global mode
    global CONFIGSET

    if not RETRIEVALS:
        return {'error': 'There is no RETRIEVALS'}

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

    mode = collection.get('mode', None)
    table = collection.get('table', None)
    modeltype = collection.get('modeltype', 'word2vec')
    columns = collection.get('columns', [])
    docid = collection.get('docid', None)
    fl = collection.get('fl', None)
    sort = collection.get('sort', None)
    rows = collection.get('rows', None)
    df = collection.get('df', None)

    if modeltype == 'fasttext':
        _vmodel = [FastText]
    else:
        _vmodel = [Word2Vec]

    # docid = 'bbid'
    # columns = ['bible_bcn', 'content', 'econtent']
    # modeltype = [FastText]
    # q = ' '.join(tokenize_by_morpheme_char(q))
    print('(q):%s' % q)
    try:
        sparser = SolrAPIParser()
        solr_kwargs_url_params = sparser.query_parse_nofacet(request, q)
        log.info('solr_kwargs_url_params: %s' % solr_kwargs_url_params)
        print('solr_kwargs_url_params:%s' % solr_kwargs_url_params)

        # default field
        # default_field = solr_kwargs_url_params.get('df', [])

        # parameter for solr kwargs
        solr_kwargs = solr_kwargs_url_params

        # mode
        if mode:
            solr_kwargs['mode'] = mode

        # if not default_field:
        #     solr_kwargs['df'] = []
        #     solr_kwargs = solr_kwargs

        log.info('solr_kwargs: %s' % solr_kwargs)
        print('solr_kwargs:%s' % solr_kwargs)

        default_k = None
        st = timeit.default_timer()
        query_results = IRM.get_query_results(q=q, mode=mode, modeltype=_vmodel, retrievals=RETRIEVALS,
                                              columns=columns, docid=docid, tb_df=TB_DB, k=default_k,
                                              solr_kwargs=solr_kwargs, collection=collection)
        qtime = str(timeit.default_timer() - st)
        status = 200
        start = solr_kwargs_url_params.get('start', 0)

        numfound = query_results[modeltype]['boost']['numfound']
        docs = query_results[modeltype]['boost']['docs']
        solr_json = IRM.solr_json_return(status, qtime, solr_kwargs, numfound, start, docs)
        qtime0 = str(timeit.default_timer() - st0)
        print('qtime0:%s' % qtime0)
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
