import os, sys
import multiprocessing

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config

DB_NAME = 'db.sqlite3'
MODEL_W2V_PATH = '/model/'
LOG_PATH = '/log/'

MODEL_SIZE = 100
MODEL_MIN_COUNT = 1
MODEL_WINDOW = 5
MODEL_WORKERS = multiprocessing.cpu_count()
MODEL_EPOCHS = 5
