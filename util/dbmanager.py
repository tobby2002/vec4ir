import os, sys
from sqlalchemy import create_engine
from util.logmanager import logz
log = logz()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config


import psycopg2
import pandas.io.sql as psql

import pandas as pd
# Connection parameters, yours will be different
param_dic = {
    'host': 'localhost',
    'database': 'globaldata',
    'user': 'myuser',
    'password': 'Passw0rd'
}

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        log.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        log.error(error)
    log.info("Connection successful")
    return conn

def psql2df(conn, columns, table):
    try:
        df = psql.frame_query("SELECT id, price FROM stock_price", conn)
    except Exception as error:
        err = {'error': 'Error: %s' % error}
        log.error(err)
        return err
    finally:
        if conn is not None:
            conn.close()
    return df


def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1

    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()

    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df

def get_connect_engine_wi():
    conn = None
    engine = None
    try:
        dbinfo = config.DB_WI
        engine = create_engine(dbinfo, convert_unicode=True)
        conn = engine.connect()
    except Exception as e:
        err = {'error': 'get_connect_engine_wi exception:%s' % e}
        if conn is not None:
            log.error(err)
            conn.close()
        if engine is not None:
            log.error(err)
            engine.close()
        return err
    return conn, engine