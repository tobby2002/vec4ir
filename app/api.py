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
import json

global IRM
IRM = IrManager()
tb_df = IRM.get_tb_df()
table = 'bibl'
# modeltype = [Word2Vec, FastText]
modeltype = [Word2Vec]
docid = 'bbid'
columns = ['bible_bcn', 'content', 'econtent']
global RETRIEVALS
RETRIEVALS = IRM.set_init_models_and_get_retrievals(modeltype, table, docid, columns, tb_df)


@api.get("/{id}/search")
def search(request, id: str, q: str):
    print('collection:%s' % id)

    sparser = SolrAPIParser()
    solr_kwargs = sparser.query_parse_nofacet(request, q)
    print('solr_kwargs:%s' % solr_kwargs)
    default_k = None
    log.info('api/%s/search?q=%s' % (id, q))
    print('q:%s' % q)
    st = timeit.default_timer()
    query_results = IRM.get_query_results(q=q, modeltype=modeltype, retrievals=RETRIEVALS, columns=columns, docid=docid,
                                          tb_df=tb_df, k=default_k, solr_kwargs=solr_kwargs)
    qtime = str(timeit.default_timer() - st)
    print('take time: %s' % qtime)
    status = 200
    params = solr_kwargs
    start = 0
    start = get_dicvalue(solr_kwargs, key='start', initvalue=0)

    # default field to search
    default_field = get_dicvalue(solr_kwargs, key='df', initvalue='content')
    numfound = query_results[modeltype[0].__name__.lower()][default_field]['numfound']
    docs = query_results[modeltype[0].__name__.lower()][default_field]['docs']
    solr_json = IRM.solr_json_return(status, qtime, params, numfound, start, docs)
    # print('solr_json: %s' % solr_json)
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
