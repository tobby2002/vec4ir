import os, sys
from sqlalchemy import create_engine
from util.logmanager import logz
log = logz()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

def get_connect_engine_p():
    try:
        dbinfo = config.DB_SOURCE
        engine = create_engine(dbinfo, convert_unicode=True)
        conn = engine.connect()
    except Exception as e:
        err = {'error': 'get_connect_engine_p exception:%s' % e}
        log.error(err)
        conn.close()
        return err
    return conn

def get_connect_engine_wi():
    try:
        dbinfo = config.DB_WI
        engine = create_engine(dbinfo, convert_unicode=True)
        conn = engine.connect()
    except Exception as e:
        err = {'error': 'get_connect_engine_wi exception:%s' % e}
        log.error(err)
        conn.close()
        return err
    return conn