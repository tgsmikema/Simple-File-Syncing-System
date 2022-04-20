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


def main():
    # parse args from the stdin
    dir_list = sys.argv
    dir_list.pop(0)
    if not len(dir_list) == 2:
        print("\nYou have to enter EXACTLY 2 directories!!\n PROGRAM EXITED...")
        exit(1)
    # -------------------------

    # boolean list is dir exist
    boo_list = [Path(dir_list[0]).is_dir(), Path(dir_list[1]).is_dir()]

    # file_path_name = "README.md"
    # path = Path(file_path_name)
    #
    # path1 = os.getcwd()



main()
