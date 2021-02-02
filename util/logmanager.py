import os, sys
import datetime
import logging.handlers
import shutil
import logging

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config


def _timestamp():
    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d%H%M")
    return now_str


def _get_logger(logdir, logname, loglevel=logging.INFO):  # https://wikidocs.net/3736
    fmt = "[%(asctime)s] %(levelname)s: %(message)s"
    formatter = logging.Formatter(fmt)

    handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(logdir, logname),
        maxBytes=2 * 1024 * 1024 * 1024,
        backupCount=10)
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
