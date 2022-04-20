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

    # get current dir sync file info
    sync_file_path = Path(str(dir_path) + "/.sync")
    sync_dict = util.read_sync_f(sync_file_path)

    # part 1 of single dir sync ---------------------------------------------------------
    for file_obj in file_obj_list:
        key = file_obj.file_name


        if not (sync_dict.keys().__contains__(key)):
            util.new_key_entry_to_sync_dict(sync_dict, file_obj)
            continue
        else:
            # sync_dict[key][current_f_status_list][digest]
            if sync_dict[key][0][1] != file_obj.digest:
                util.insert_entry_to_sync_dict(sync_dict, file_obj)
                continue
            else:
                # sync_dict[key][current_f_status_list][mod_t_str]
                sync_log_mod_t_ts = util.convert_mod_str_to_ts(sync_dict[key][0][0])
                if sync_log_mod_t_ts != file_obj.mod_time_tstamp:
                    util.set_f_mod_time(file_obj.posix_path,sync_log_mod_t_ts)
                    continue
                else:
                    continue
    # -----------------------------------------------------------------------------------

    util.update_sync_f(sync_file_path, sync_dict)
    print(sync_dict)






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
