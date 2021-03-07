import os, sys
import multiprocessing
import socket
import jwt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

LOG_PATH = os.sep + 'irlog' + os.sep + 'logs'

# PRODUCTION CHECK
ip = socket.gethostbyname(socket.gethostname())
if ip in ['10.60.218.1', '10.60.218.2']:  # prod. server
    PRODUCTION = True
    DEBUG = False
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']
    # DB_INFO = jwt.decode('zzz', 'secret', algorithms=['HS256'])
    # DB_WI = DB_INFO['DB_WI']
    MODEL_SIZE = 100
elif ip in ['10.60.218.21']:  # dev. server
    PRODUCTION = True
    DEBUG = False
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']
    # DB_INFO = jwt.decode('zzz', 'secret', algorithms=['HS256'])
    # DB_WI = DB_INFO['DB_WI']
    MODEL_SIZE = 50
else:
    PRODUCTION = False
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']
    # DB_INFO = jwt.decode('zzz', 'secret', algorithms=['HS256'])
    # DB_WI = DB_INFO['DB_WI']
    MODEL_SIZE = 50

DB_WI = 'postgresql://wiap00:new1234!@127.0.0.1:5432/widev'

print('PRODUCTION:%s' % PRODUCTION)
print('DEBUG:%s' % DEBUG)
print('DB_WI:%s' % DB_WI)


MODEL_IR_PATH = '/model/ir/'
MODEL_LTR_PATH = '/model/ltr/'

# MODEL_SIZE = 100
MODEL_SIZE = 50
MODEL_MIN_COUNT = 1
MODEL_WINDOW = 5
MODEL_ITER = 1
MODEL_WORKERS = round(multiprocessing.cpu_count()/2)  # multiprocessing.cpu_count() - 2
# MODEL_WORKERS = 8

# only fasttext
MODEL_SG = 1
MODEL_WORD_NGRAMS = 5  #

MODEL_EPOCHS = 10
LTR_CID = 100000

# Scheduler
# job_api_v1_init
INIT_ID = 'init'
INIT_HOUR = '3'
INIT_REPLACE = True

# job_api_v1_start
START_ID = 'start'
START_MINUTE = '*/20'
START_REPLACE = False

