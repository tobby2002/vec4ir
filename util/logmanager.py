import os, sys
import datetime
import shutil
import config
import logging
import logging.config
import logging.handlers
from logzero import logger, logfile, setup_logger

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


def _timestamp():
    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d%H%M")
    return now_str


def _get_logger(logdir, logname, loglevel=logging.INFO):  # https://wikidocs.net/3736
    fmt = "[%(asctime)s] %(levelname)s: %(message)s"
    formatter = logging.Formatter(fmt)

    # handler = logging.handlers.RotatingFileHandler(
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=os.path.join(logdir, logname),
        # maxBytes=2 * 1024 * 1024 * 1024,
        # backupCount=10,
        when='midnight', interval=1, encoding='utf-8'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger("")
    logger.addHandler(handler)
    logger.setLevel(loglevel)
    return logger


def _makedirs(dir, force=False):
    if os.path.exists(dir):
        if force:
            shutil.rmtree(dir)
            os.makedirs(dir)
    else:
        os.makedirs(dir)

def logger(packagename, filename):
    pname = ''
    fname = ''
    if packagename:
        pname = packagename
    if filename:
        fname = filename
    _makedirs(PROJECT_ROOT + config.LOG_PATH + pname)
    logger = _get_logger(PROJECT_ROOT + config.LOG_PATH + pname, "%s_%s.log" % (fname, _timestamp()))
    return logger


def logz():
    format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s');
    custom_logger = setup_logger(
    name="Logger",
    logfile=PROJECT_ROOT + config.LOG_PATH + os.sep + "logger.log",
    formatter=format,
    # maxBytes=1000000,  # 1000000 = 1giga
    # backupCount=10,
    # maxBytes=200000,  # 200000 = 200MB
    # backupCount=50,  # 50회    => 200x50 = 10 GIGA
    maxBytes=100000,  # 100000 = 100MB
    backupCount=50,  # 50회    => 100x50 = 5 GIGA
    level=logging.INFO)
    return custom_logger