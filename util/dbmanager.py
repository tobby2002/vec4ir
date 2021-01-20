import os, sys
from sqlalchemy import create_engine
from util.logmanager import logger
log = logger('util', 'dbmanager')
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
    conn = None
    try:
        dbinfo = config.DB_WI
        engine = create_engine(dbinfo, convert_unicode=True)
        conn = engine.connect()
    except Exception as e:
        log.error('get_connect_engine_wi exception:%s' % e)
        print('get_connect_engine_wi exception:%s' % e)
    return engine.connect()
