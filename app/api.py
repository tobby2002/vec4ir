from datetime import date
from ninja import Router
from typing import List
from pydantic import BaseModel
from django.shortcuts import get_object_or_404
from .models import Event

import os, sys, time, timeit
import pytest
import pandas as pd
import numpy as np
import gensim
from gensim.models import Word2Vec, FastText, Doc2Vec
from ir.base import Matching, Tfidf
from ir.core import Retrieval
from ir.utils import build_analyzer
from ir.word2vec import WordCentroidDistance, WordMoversDistance
from ir.irmanager import IrManager
from util.dirmanager import _get_latest_timestamp_dir, dir_manager, _make_timestamp_dir
from util.dbmanager import get_connect_engine_p
from util.dbmanager import get_connect_engine_wi
from util.logmanager import logger
from util.utilmanager import build_analyzer
# import cStringIO
from io import StringIO

log = logger('ir', 'irmanager')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

import config


from ninja import NinjaAPI

api = NinjaAPI(version='1.0.0')
tb_df = None
def get_tb_df():
    return tb_df
@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

@api.get("/setsearch")
def setsearch(request):
    irm = IrManager()
    conn = get_connect_engine_wi()
    table = 'bibl'
    modeltype = [Word2Vec, FastText]
    id = ['bbid']
    columns = ['bible_bcn', 'content', 'econtent']

    dir = PROJECT_ROOT + config.MODEL_IR_PATH
    lastestdir = _get_latest_timestamp_dir(dir)

    # save and load pickle
    tb_df_table = irm.get_preprocessed_data_df(conn=conn, table=table, columns=None, analyzer_flag=False)
    irm.save_df2pickle(lastestdir, tb_df_table, table)

    tb_df_table_loaded = irm.load_pickle2df(lastestdir, table)
    print(tb_df_table_loaded.head(5))
    tb_df = tb_df_table_loaded
    return {"result": tb_df.head(5).values.tolist()}

@api.get("/search")
def search(request, q: str):
    irm = IrManager()

    # table = 'tb_ir_kn_f'
    # modeltype = [Word2Vec, FastText]
    # id = ['doc_id']
    # columns = ['knwlg_name', 'knwlg_type_name']
    # q = '동시성오더'
    #
    # # word2vec
    # query_results = irm.train_save_load_query_results(modeltype, table, id, columns, q, k=20, trainingflag=True)
    conn = get_connect_engine_wi()
    table = 'bibl'
    modeltype = [Word2Vec, FastText]
    id = ['bbid']
    columns = ['bible_bcn', 'content', 'econtent']

    dir = PROJECT_ROOT + config.MODEL_IR_PATH
    lastestdir = _get_latest_timestamp_dir(dir)

    query = q
    print('query:%s' % q)
    tb_df = get_tb_df()
    # print('tb_df:%s' % tb_df.head(5).values.tolist())
    query_results = irm.query_results(modeltype, lastestdir, table, id, columns, q=query, k=10, tb_df=tb_df)
    print(query_results)
    return {"result": "done"}


router = Router()


class EventSchema(BaseModel):
    title: str
    start_date: date
    end_date: date

    class Config:
        orm_mode = True


@router.post("/create")
def create_event(request, event: EventSchema):
    Event.objects.create(**event.dict())
    return event


@router.get("", response=List[EventSchema])
def list_events(request):
    return list(Event.objects.all())


@router.get("/{id}", response=EventSchema)
def get_event(request, id: int):
    event = get_object_or_404(Event, id=id)
    return event
