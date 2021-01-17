import os, sys
import multiprocessing

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

DB_NAME = 'db.sqlite3'
LOG_PATH = '/log/'
DB_SOURCE = 'postgresql://saleor:saleor@127.0.0.1:5432/saleor'

MODEL_IR_PATH = '/model/ir/'
MODEL_LTR_PATH = '/model/ltr/'
# MODEL_SIZE = 100
# MODEL_MIN_COUNT = 1
# MODEL_WINDOW = 5
# MODEL_WORKERS = multiprocessing.cpu_count() - 2
# MODEL_EPOCHS = 5

MODEL_SIZE = 50
MODEL_MIN_COUNT = 1
MODEL_WINDOW = 5
MODEL_WORKERS = multiprocessing.cpu_count() - 2
MODEL_EPOCHS = 3

LTR_CID = 100000
