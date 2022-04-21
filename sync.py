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
                    util.set_f_mod_time(file_obj.posix_path, sync_log_mod_t_ts)
                    continue
                else:
                    continue
    # -----------------------------------------------------------------------------------

    # util.update_sync_f(sync_file_path, sync_dict)
    # print(sync_dict)

    # part 2 of single dir sync ---------------------------------------------------------
    dir_fname_list = []
    for file_obj in file_obj_list:
        dir_fname_list.append(file_obj.file_name)

    for f_name_key in sync_dict.keys():
        if f_name_key in dir_fname_list:
            continue
        else:
            util.insert_delete_to_sync_dict(sync_dict, f_name_key)
    # -----------------------------------------------------------------------------------
    util.update_sync_f(sync_file_path, sync_dict)

    # recursive function call for all subdirectories (single-dir-syncing) --------------
    sub_dir_list = util.get_dir_list_from_dir(dir_path)
    if len(sub_dir_list) != 0:
        for sub_dir in sub_dir_list:
            single_dir_syncing(sub_dir)
    # -----------------------------------------------------------------------------------


def merge_dir_syncing(curr_dir, other_dir):
    file_obj_l_curr = util.get_file_list_from_dir(curr_dir)
    file_obj_l_other = util.get_file_list_from_dir(other_dir)

    # get current dir sync file info
    sync_f_path_curr = Path(str(curr_dir) + "/.sync")
    sync_dict_curr = util.read_sync_f(sync_f_path_curr)

    # get other dir sync file info
    sync_f_path_other = Path(str(other_dir) + "/.sync")
    sync_dict_other = util.read_sync_f(sync_f_path_other)

    curr_f_name_list = []
    for file_obj_c_temp_ONLY in file_obj_l_curr:
        curr_f_name_list.append(file_obj_c_temp_ONLY.file_name)

    other_f_name_list = []
    for file_obj_o_temp_ONLY in file_obj_l_other:
        other_f_name_list.append(file_obj_o_temp_ONLY.file_name)

    for file_obj_curr in file_obj_l_curr:
        # is file DOESN'T exist in OTHER dir file list?
        if file_obj_curr.file_name not in other_f_name_list:
            # is file deleted in OTHER dir?
            if (file_obj_curr.file_name in sync_dict_other.keys()) and (sync_dict_other[file_obj_curr.file_name][0][1] == "deleted"):
                # Has the file been just deleted in CURRENT dir?
                if (len(sync_dict_curr[file_obj_curr.file_name]) > 1) and (sync_dict_curr[file_obj_curr.file_name][1][1] == "deleted"):
                    # ACTION 2
                    util.copy_to_other_dir(file_obj_curr.posix_path, other_dir)
                    util.update_sync_dict_entry(file_obj_curr, sync_dict_other)
                    continue
                # the file has not been just deleted in CURRENT dir.
                else:
                    # ACTION 1
                    util.delete_file(file_obj_curr.posix_path)
                    util.insert_delete_to_sync_dict(sync_dict_curr, file_obj_curr.file_name)
                    continue
            # file is NOT deleted in OTHER dir
            else:
                # ACTION 2
                util.copy_to_other_dir(file_obj_curr.posix_path, other_dir)
                util.update_sync_dict_entry(file_obj_curr, sync_dict_other)
                continue
        # file EXIST in OTHER dir file list
        else:
            pass


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

    merge_dir_syncing(dir_path_list[0], dir_path_list[1])


main()
