from datetime import date
from ninja import Router
from typing import List
from pydantic import BaseModel
from django.shortcuts import get_object_or_404
from .models import Event

import os, sys, timeit
from util.logmanager import logger
from util.solrapiparser import SolrAPIParser
from util.utilmanager import get_dicvalue, build_analyzer

log = logger('ir', 'irmanager')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

import config

from ninja import NinjaAPI
api = NinjaAPI(version='1.0.0')

from ir.irmanager import IrManager
from gensim.models import Word2Vec, FastText, Doc2Vec

"""
1.exec job by api : http://127.0.0.1:8777/api/11/job?q=시작
2.exec search by api : http://127.0.0.1:8777/api/collection01/search?q=하나님께서 세상을 창조&start=0&rows=10
"""
@api.get("/{id}/job")
def job(request, id: str, q: str):
    log.info('api/%s/job?q=%s' % (id, q))

    global IRM
    IRM = IrManager()

    global tb_df
    tb_df = IRM.get_tb_df()
    table = 'bibl'
    # modeltype = [Word2Vec, FastText]
    modeltype = [Word2Vec]

    global docid
    docid = 'bbid'

    global columns
    columns = ['bible_bcn', 'content', 'econtent']
    # RETRIEVALS = IRM.set_init_models_and_get_retrievals(modeltype, table, docid, columns, tb_df)

    global RETRIEVALS
    st = timeit.default_timer()

    jobname = 'retrieval'
    # word2vec
    if q:
        jobname = 'train + retrieval'
        word2vec_models = IRM.train_models(Word2Vec, tb_df, columns)
        IRM.save_models(word2vec_models, Word2Vec, table, columns, dirresetflag=True)

    try:
        RETRIEVALS = IRM.set_init_models_and_get_retrievals(modeltype, table, docid, columns, tb_df)
    except Exception as e:
        jobtime = str(timeit.default_timer() - st)
        return {'error': str(e), 'jobtime': jobtime}
    jobtime = str(timeit.default_timer() - st)

    if not RETRIEVALS:
        return {'error': 'no retrievals',
                'jobname': jobname,
                'jobtime': jobtime}
    return {'msg': 'job success',
            'jobname' : jobname,
            'taken time': jobtime
            }


@api.get("/{id}/search")
def search(request, id: str, q: str):
    log.info('api/%s/search?q=%s' % (id, q))
    modeltype = [Word2Vec]
    try:
        sparser = SolrAPIParser()
        solr_kwargs_url_params = sparser.query_parse_nofacet(request, q)
        log.info('solr_kwargs_url_params: %s' % solr_kwargs_url_params)
        print('solr_kwargs_url_params:%s' % solr_kwargs_url_params)

        # default field
        default_field = get_dicvalue(solr_kwargs_url_params, key='df', initvalue=[])

        solr_kwargs = solr_kwargs_url_params
        if not default_field:
            solr_kwargs['df'] = ['content']
            solr_kwargs = solr_kwargs
        log.info('solr_kwargs: %s' % solr_kwargs)
        print('solr_kwargs:%s' % solr_kwargs)

        default_k = None
        st = timeit.default_timer()
        query_results = IRM.get_query_results(q=q, modeltype=modeltype, retrievals=RETRIEVALS, columns=columns, docid=docid,
                                              tb_df=tb_df, k=default_k, solr_kwargs=solr_kwargs)
        qtime = str(timeit.default_timer() - st)
        status = 200
        start = get_dicvalue(solr_kwargs_url_params, key='start', initvalue=0)

        numfound = query_results[modeltype[0].__name__.lower()][solr_kwargs['df'][0]]['numfound']
        docs = query_results[modeltype[0].__name__.lower()][solr_kwargs['df'][0]]['docs']
        solr_json = IRM.solr_json_return(status, qtime, solr_kwargs, numfound, start, docs)
    except Exception as e:
        solr_json = {"error": "%s" % str(e)}
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
