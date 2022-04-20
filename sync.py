#!/usr/bin/env python3
# Author: Siqi Ma
# UPI: sma148

import os
from datetime import datetime
import shutil
import json
from pathlib import Path
import sys
import util


def single_dir_syncing(dir_path):
    if not util.is_sync_f_exist(dir_path):
        util.create_empty_sync_f(dir_path)

    file_obj_list = util.get_file_list_from_dir(dir_path)
    # dir_posix_list = util.get_dir_list_from_dir(dir_path)
    # print(dir_posix_list)


def main():
    # parse args from the stdin and make sure it contains only 2 dirs
    dir_list = sys.argv
    dir_list.pop(0)
    if not len(dir_list) == 2:
        print("\nYou have to enter EXACTLY 2 directories!!\n PROGRAM EXITED...")
        exit(1)
    # --------------------------------------------------------------------------

    # boolean list is dir exist
    boo_list = [Path(dir_list[0]).is_dir(), Path(dir_list[1]).is_dir()]
    if boo_list[0] == False and boo_list[1] == False:
        print("\nBOTH directories are not FOUND!!\n PROGRAM EXITED...")
        exit(1)
    elif boo_list[0] == True and boo_list[1] == False:
        os.mkdir(dir_list[1])
    elif boo_list[1] == True and boo_list[0] == False:
        os.mkdir(dir_list[0])
    # -------------------------------------------------------------------------

    dir_path_list = [Path(dir_list[0]), Path(dir_list[1])]
    for dir_path in dir_path_list:
        single_dir_syncing(dir_path)


main()
