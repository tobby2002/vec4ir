import os
import shutil
from datetime import datetime

def dir_manager(dir):
    _make_timestamp_dir(dir)
    _delete_timestamp_dir(dir)

def _make_timestamp_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    (dt, micro) = datetime.now().strftime('%Y%m%d%H%M%S.%f').split('.')
    dt = "%s%03d" % (dt, int(micro) / 1000)
    os.mkdir(dir + str(dt))
    print('_make_time_dir:%s' % dt)


def _delete_timestamp_dir(dir):
    for root, dirs, files in os.walk(dir):
        for idx, dir in enumerate(reversed(sorted(dirs))):
            if idx > 1:
                shutil.rmtree(root + dir)


def _get_latest_timestamp_dir(dir):
    for root, dirs, files in os.walk(dir):
        for idx, dir in enumerate(reversed(sorted(dirs))):
            if idx == 0:
                lastestdir = root + dir
                return lastestdir + '/'
    return None


def purgedir(parent):
    for root, dirs, files in os.walk(parent):
        for item in files:
            # Delete subordinate files
            filespec = os.path.join(root, item)
            if filespec.endswith('*.*'):
                os.unlink(filespec)
        for item in dirs:
            os.removedirs(root + item)
            # Recursively perform this operation for subordinate directories
            purgedir(os.path.join(root, item))
