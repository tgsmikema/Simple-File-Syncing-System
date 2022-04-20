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


def set_f_mod_time(f_path, dt_time):
    """set file modification time to an inputted file_path"""
    dt_mod_time = dt_time.timestamp()
    os.utime(f_path, (dt_mod_time, dt_mod_time))


def convert_dt_to_ts(dt_time):
    """convert DATETIME format into int TIMESTAMP format"""
    return int(dt_time.timestamp())


def get_f_mod_time_string(f_path):
    """get modification time of FILE into STRING format"""
    dt_time = get_f_mod_time(f_path)
    dt_string = dt_time.strftime("%Y-%m-%d %H:%M:%S %z")
    return dt_string


def convert_mod_str_to_dt(dt_str):
    """convert modification time STRING into DATETIME format"""
    dt_obj = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S %z')
    return dt_obj


def gen_f_status_list(f_path):
    """generate file status list including """
    status_list = [get_f_mod_time_string(f_path), gen_digest(read_file(f_path))]
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


def get_file_list_from_dir(dir_path):
    """get all files(except .sync) in the dir and return a `list` of file Object"""
    dir_path = Path(dir_path)
    dir_list = os.listdir(dir_path)
    print(dir_list)
    f_obj_list = []

    for file in dir_list:
        f_posix_path = dir_path.joinpath(file)
        if os.path.isfile(f_posix_path) and not (os.path.basename(f_posix_path) == ".sync"):
            f_obj_list.append(File(f_posix_path))

    return f_obj_list

def get_dir_list_from_dir(dir_path):
    dir_list = os.listdir(dir_path)
    d_list = []

    for file in dir_list:
        if os.path.isdir(Path(file)):
            d_list.append(file)

    return d_list
