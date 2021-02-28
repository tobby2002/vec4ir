import os, sys
import multiprocessing

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

LOG_PATH = os.sep + 'irlog' + os.sep + 'logs'


DB_WI = 'postgresql://wiap00:new1234!@127.0.0.1:5432/widev'

MODEL_IR_PATH = '/model/ir/'
MODEL_LTR_PATH = '/model/ltr/'
# MODEL_SIZE = 100
# MODEL_MIN_COUNT = 1
# MODEL_WINDOW = 5
# MODEL_WORKERS = multiprocessing.cpu_count() - 2
# MODEL_EPOCHS = 5

# MODEL_SIZE = 100
MODEL_SIZE = 50
MODEL_MIN_COUNT = 1
MODEL_WINDOW = 5
MODEL_ITER = 1
MODEL_WORKERS = round(multiprocessing.cpu_count()/2)
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

