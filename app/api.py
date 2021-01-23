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
from django.conf import settings


log = logger('ir', 'irmanager')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

import config


from ninja import NinjaAPI
api = NinjaAPI(version='1.0.0')


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@api.get("/search")
def search(request, q: str):
    table = 'bibl'
    modeltype = [Word2Vec, FastText]
    id = 'bbid'
    columns = ['bible_bcn', 'content', 'econtent']

    IRM = settings.__dict__.get('IRM', None)
    print('query:%s' % q)
    RETRIEVALS = settings.__dict__.get('RETRIEVALS', None)
    query_results = RETRIEVALS.get_query_results(q=q, retrievals=RETRIEVALS, columns=columns, k=10)
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
