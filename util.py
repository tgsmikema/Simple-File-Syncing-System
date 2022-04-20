# Author: Siqi Ma
# UPI: sma148

import hashlib
import json
import os
from pathlib import Path
from datetime import datetime
from file import File


def gen_digest(f_content):
    """parameter: `string` type file content"""
    hashed_string = hashlib.sha256(f_content.encode('utf-8')).hexdigest()
    return hashed_string


def read_file(f_path):
    """parameter: `path` of the file ; return: `string` of file content"""
    text_file = open(f_path, "r")
    data = text_file.read()
    text_file.close()
    return data


def write_to_file(f_path, f_content):
    """parameters: `path` of file, `string` content of message"""
    file = open(f_path, "w")
    success = file.write(f_content)
    file.close()


def get_f_mod_time(f_path):
    """get modification time of a file, return a datetime format."""
    time = os.path.getmtime(f_path)
    time = time.__trunc__()
    dt_time = datetime.fromtimestamp(time)
    dt_time = dt_time.astimezone()
    return dt_time


def set_f_mod_time(f_path, ts_time):
    """set file modification time to an inputted file_path"""
    dt_mod_time = ts_time.timestamp()
    os.utime(f_path, (dt_mod_time, dt_mod_time))


def convert_dt_to_ts(dt_time):
    """convert DATETIME format into int TIMESTAMP format"""
    return int(dt_time.timestamp())


def get_f_mod_time_string(f_path):
    """get modification time of FILE into STRING format"""
    dt_time = get_f_mod_time(f_path)
    dt_string = dt_time.strftime("%Y-%m-%d %H:%M:%S %z")
    return dt_string


def get_current_time_str():
    ct = datetime.now()
    dt_string = ct.astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    return dt_string


def convert_mod_str_to_dt(dt_str):
    """convert modification time STRING into DATETIME format"""
    dt_obj = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S %z')
    return dt_obj


def convert_mod_str_to_ts(dt_str):
    """convert modification time STRING into TIMESTAMP format"""
    dt_obj = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S %z')
    return convert_dt_to_ts(dt_obj)


def gen_f_status_list(f_obj):
    """generate file status list including mod_time and digest"""
    status_list = [f_obj.mod_time_str, f_obj.digest]
    return status_list


def gen_deleted_status_list():
    mod_time_str = get_current_time_str()
    digest = "deleted"
    status_list = [mod_time_str, digest]
    return status_list


def create_empty_sync_f(dir_path):
    f_path_str = str(dir_path) + "/.sync"
    f_path = Path(f_path_str)
    new_dict = {}
    json_str = json.dumps(new_dict, indent=2)
    write_to_file(f_path, json_str)
    return f_path


def update_sync_f(f_path, content_dict):
    json_str = json.dumps(content_dict, indent=2)
    write_to_file(f_path, json_str)


def read_sync_f(f_path):
    """return DICT type"""
    json_str = read_file(f_path)
    json_dict = json.loads(json_str)
    return json_dict


def is_sync_f_exist(dir_path):
    path_sync = str(dir_path) + "/.sync"
    path_s = Path(path_sync)
    return path_s.is_file()


def insert_entry_to_sync_dict(sync_dict, file_object):
    f_status_list = gen_f_status_list(file_object)
    f_name_key = file_object.file_name
    if sync_dict.keys().__contains__(f_name_key):
        sync_dict[f_name_key].insert(0, f_status_list)


def insert_delete_to_sync_dict(sync_dict, key_name):
    f_status_list = gen_deleted_status_list()
    if sync_dict.keys().__contains__(key_name):
        sync_dict[key_name].insert(0, f_status_list)


def new_key_entry_to_sync_dict(sync_dict, file_object):
    f_status_list = gen_f_status_list(file_object)
    f_name_key = file_object.file_name
    if not (sync_dict.keys().__contains__(f_name_key)):
        sync_dict[f_name_key] = [f_status_list]


def get_file_list_from_dir(dir_path):
    """get all files(except .sync) in the dir and return a `list` of file Object"""
    dir_path = Path(dir_path)
    dir_list = os.listdir(dir_path)
    f_obj_list = []

    for file in dir_list:
        f_posix_path = dir_path.joinpath(file)
        if os.path.isfile(f_posix_path) and not (os.path.basename(f_posix_path) == ".sync"):
            f_obj_list.append(File(f_posix_path))

    return f_obj_list


def get_dir_list_from_dir(dir_path):
    """return posix path format of dir paths in a list"""
    dir_path = Path(dir_path)
    dir_list = os.listdir(dir_path)
    d_list = []

    for each_dir in dir_list:
        dir_posix_path = dir_path.joinpath(each_dir)
        if os.path.isdir(Path(dir_posix_path)):
            d_list.append(dir_posix_path)

    return d_list
