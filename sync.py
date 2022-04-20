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
    print(dir_list)
    # -------------------------


    # print(dt_c.astimezone())
    # dt = datetime.fromtimestamp(os.path.getmtime(path))
    # print(dt)

    file_path_name = "dir1" + "/" + "123.txt"
    path = Path(file_path_name)

    print(path)
    print(util.read_file(path))

    mod_t = util.get_mod_time_f(path)
    print(mod_t)
    print(util.convert_dt_to_ts(mod_t))


main()

