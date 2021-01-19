import os, sys
from sqlalchemy import create_engine

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

def get_connect_engine():
    dbinfo = 'sqlite:////' + PROJECT_ROOT + '/' + config.DB_NAME
    engine = create_engine(dbinfo, convert_unicode=True)
    return engine.connect()

def get_connect_engine_p():
    dbinfo = config.DB_SOURCE
    engine = create_engine(dbinfo, convert_unicode=True)
    return engine.connect()

def get_connect_engine_wi():
    dbinfo = config.DB_WI
    engine = create_engine(dbinfo, convert_unicode=True)
    return engine.connect()
