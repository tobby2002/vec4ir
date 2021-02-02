#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from glob import glob
import shutil
from pathlib import Path, PurePath
import pprint
pp = pprint.PrettyPrinter(indent=4)


def mkdirRecursive(dirpath):
    import os
    if os.path.isdir(dirpath): return

    h, t = os.path.split(dirpath)  # head/tail
    if not os.path.isdir(h):
        mkdirRecursive(h)
    os.mkdir(os.path.join(h, t))

def repacefile(fullpathin,fullpathout, search_pattern, replace_pattern):
    # input file
    fin = open(fullpathin, "rt")
    # output file to write the result to
    fout = open(fullpathout, "wt")
    # for each line in the input file
    for line in fin:
        # read replace the string and write to output file
        newline = line
        for i, v in enumerate(search_pattern):
            newline = newline.replace(v, replace_pattern[i])
        fout.write(newline)
    # close input and output files
    fin.close()
    fout.close()

def filterfile(file, fileterfiles):
    for i, v in enumerate(fileterfiles):
        if file.find(v) != -1:
            # print("contains given substring")
            return False
    return True


class refactory():

    def rename_files(self, src_dir, target_dir, srcappkeyword, targetappkeyword, search_pattern, replace_pattern, fileterfiles):
        print('================================================================')
        print('src_dir ==> [{}], target_dir ==> [{}]'.format(src_dir, target_dir))
        print('================================================================')

        files = []
        pattern = "*.*"
        for dir, _, _ in os.walk(src_dir):
            files.extend(glob(os.path.join(dir, pattern)))
        pp.pprint(files)
        for i, v in enumerate(files):
            newfilename = v.rsplit('/%s' % srcappkeyword, 1)
            # pp.pprint(newfilename)
            beforepath = newfilename[0]
            afterpathplusfile = newfilename[-1]

            targetfile = afterpathplusfile
            for j, value in enumerate(search_pattern):
                targetfile = targetfile.replace(value, replace_pattern[j])

            target_items_path = ''
            target_items_file = ''
            target_items = targetfile.rsplit('/', 1)

            if not len(target_items[0]):
                target_items_path = target_items[0].replace('/', '')
                target_items_file = target_items[1].strip().replace('/', '')
                target_full_path = beforepath + '/' + targetappkeyword

                mkdirRecursive(target_full_path)
                targetfile = target_full_path + '/' + target_items_file

                if filterfile(v, fileterfiles):
                    shutil.copy(v, targetfile)
                    repacefile(v, targetfile, search_pattern, replace_pattern)
            else:
                target_items_path = target_items[0]
                target_items_file = target_items[1].strip().replace('/', '')
                target_full_path = beforepath + '/' + targetappkeyword + '/' + target_items_path
                mkdirRecursive(target_full_path)
                targetfile = target_full_path + '/' + target_items_file
                # shutil.copy(v, targetfile)
                # repacefile(v, targetfile, search_pattern, replace_pattern)
                if filterfile(v, fileterfiles):
                    shutil.copy(v, targetfile)
                    repacefile(v, targetfile, search_pattern, replace_pattern)
            print('%s --> %s' % (v, (target_full_path + '/' + target_items_file)))


if __name__ == '__main__':

    # https://hyeshinoh.github.io/2018/10/12/python_09_OS%20&%20shutil/
    import refactory as rf
    src_dir = '/Users/neo1/PycharmProjects/saleor/app/wallet'  # work dir
    target_dir = '/Users/neo1/PycharmProjects/saleor/app/exchange'  # target dir
    srcappkeyword = 'wallet'  # src app keyword
    targetappkeyword = 'exchange'  # target app keyword
    search_regex = ['wallet', 'Wallet', 'WALLET']  # search regex
    replace_regex = ['exchange', 'Exchange', 'EXCHANGE']  # replace regex
    fileterfiles = ['__pycache__', 'migrations', '.pyc']  # filter files or directory

    rf.refactory.rename_files(rf, src_dir, target_dir, srcappkeyword, targetappkeyword, search_regex, replace_regex, fileterfiles)
