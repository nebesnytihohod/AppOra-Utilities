#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import json

valid = []
not_valid = []
regexp_pattern = []
valid_line = []
valid_file = []
not_valid_file = []

module_name = sys.argv[0]

if sys.argv[1] is None:
    config_file_name = 'config.json'
else:
    config_file_name = sys.argv[1]

with open(config_file_name, 'r') as config_file:
    config_param = json.loads(config_file.read())

name_res_file = config_param['name_res_file']
name_file = config_param['name_file']
#file_size = config_param['file_size']    # 500kB -> 512 000 byte
dimension = config_param['file_size'][1]
exclude = config_param['exclude']
search_substring = config_param['search_substring']

if dimension.lower() == 'kb':
    file_size = config_param['file_size'][0] * 1024
elif dimension.lower() == 'mb':
    file_size = config_param['file_size'][0] * 1024 * 1024
elif dimension.lower() == 'b':
    file_size = config_param['file_size'][0]
else:
    file_size = 0


exclude.append(name_res_file)
exclude.append(name_file)
exclude.append(module_name)
exclude.append(config_file_name)

for dir_path, subdir_list, files_list in os.walk(os.getcwd()):
    for f in files_list:
        mark = False
        temp_file_name = f.lower()
        full_name = os.path.join(os.path.abspath(os.path.normcase(dir_path)), f)
        for e in exclude:
            if (temp_file_name.find(e) != -1) or (os.path.getsize(full_name) > file_size):
                mark = True
                break
            
        if mark:
            not_valid.append(full_name)
        else:
            valid.append(full_name)

with open(name_res_file, 'w') as res_file:
    for i in valid:
        res_file.write(i)
        res_file.write('\n')

    res_file.write('===================================\n\n')

    for i in not_valid:
        res_file.write(i)
        res_file.write('\n')

for item in search_substring:
    regexp_pattern.append(re.compile(item))

for element in valid:
    mark = False
    with open(element, 'r') as file_obj:
        for line in file_obj:
            for item in regexp_pattern:
                if re.search(item, line) is None:    # Если тру – то значит не найдено; Если фальш – значит найдено
                    continue
                else:
                    valid_line.append(line)
                    mark = True
    
    if mark:
        valid_file.append(element)
    else:
        not_valid_file.append(element)

with open(name_file, 'w') as res_file:
    for i in valid_line:
        res_file.write(i)
        res_file.write('\n')

    res_file.write('===================================\n\n')

    for i in valid_file:
        res_file.write(i)
        res_file.write('\n')

    res_file.write('===================================\n\n')

    for i in not_valid_file:
        res_file.write(i)
        res_file.write('\n')