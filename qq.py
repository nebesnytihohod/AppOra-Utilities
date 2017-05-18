#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
utilities for app on Oracle platform
'''

import os
import sys
import re
import json
import logging

valid = []
not_valid = []
regexp_pattern = []
valid_line = []
valid_file = []
not_valid_file = []

module_name = sys.argv[0]
__version__ = "1.1"


def main():

    # создание объекта класса логгер
    logger = logging.getLogger(__name__)
    # уровень приоритета начиная с которого начинают выводиться сообщения
    logger.setLevel(logging.DEBUG)
    # задаем консольный handler и его уровень
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # задаем файловый handler и его уровень
    file_handler = logging.FileHandler('logfile.log', 'w')
    console_handler.setLevel(logging.WARNING)
    # формат сообщения при выводе на экран
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # добавление formatter'a к конкретному handler'y
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    # добавление конкретного handler'a к logger'y
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Program started")
    # Создать объект парсера c возможностью вывода справки –h|--help и номера версии –v|--version
    cli_parser = argparse.ArgumentParser(
        description='Great Description To Be Here',
        add_help=True,
        version=__version__)

    # добавить в парсер параметры – аргументы комм.строки
    cli_parser.add_argument(
        '-i',
        '--interactive',
        action='store',
        dest='interactive',
        help='Interactive mode - specifying the parameters of the utility operator')
    cli_parser.add_argument(
        '-c',
        '--config',
        action='store',
        dest='create_config_file',
        help='Create configuration file')
    cli_parser.add_argument(
        '-ncf',
        '--not_config',
        action='store',
        dest='not_use_config_file',
        help='Not use existing configuration file')
    cli_parser.add_argument('configuration', help='Specifying')
    cli_parser.add_argument(
        'result', help='A file with the result of program using')

    args = cli_parser.parse_args()

    if sys.argv[1] is None:
        config_file_name = 'config.json'
        logger.info("Default configuration file")
    else:
        config_file_name = sys.argv[1]
        logger.info("Existing configuration file")

    with open(config_file_name, 'r') as config_file:
        config_param = json.loads(config_file.read())
        logger.info("Parameters loading...")

    name_res_file = config_param['name_res_file']
    final_res_file = config_param['name_file']
    dimension = config_param['file_size'][1]
    exclude_list = config_param['exclude']
    search_substring = config_param['search_substring']

    if dimension.lower() == 'kb':
        file_size = config_param['file_size'][0] * 1024
    elif dimension.lower() == 'mb':
        file_size = config_param['file_size'][0] * 1024 * 1024
    elif dimension.lower() == 'b':
        file_size = config_param['file_size'][0]
    else:
        file_size = 0

    exclude_list.append(name_res_file)
    exclude_list.append(name_file)
    exclude_list.append(module_name)
    exclude_list.append(config_file_name)

    logger.info("File search and sort is starting...")
    fileSort(exclude_list, file_size)
    logger.info("...file search and sort is finishing")

    outputResult(name_res_file, valid)
    logger.info("Valid data saved in resulting file")

    outputResult(name_res_file, not_valid)
    logger.info("Not-Valid data saved in resulting file")

    for item in search_substring:
        regexp_pattern.append(re.compile(item))

    logger.info("Pattern search is starting...")
    searchPattern(valid, regexp_pattern)
    logger.info("...pattern search is finishing")

    outputResult(final_res_file, valid_line)
    logger.info("Line with searching data saved in resulting file")

    outputResult(final_res_file, valid_file)
    logger.info("UNC filename with searching data saved in resulting file")

    outputResult(final_res_file, not_valid_file)
    logger.info(
        "UNC filename witch not contained data saved in resulting file")


def fileSort(exclude, f_size):
    for dir_path, subdir_list, files_list in os.walk(os.getcwd()):
        for f in files_list:
            mark = False
            temp_file_name = f.lower()
            full_name = os.path.join(
                os.path.abspath(os.path.normcase(dir_path)), f)
            for e in exclude:
                if (temp_file_name.find(e) != -1) or (
                        os.path.getsize(full_name) > f_size):
                    mark = True
                    break

            if mark:
                not_valid.append(full_name)
            else:
                valid.append(full_name)


def outputResult(name_file, result_list):
    with open(name_file, 'w') as res_file:
        for i in result_list:
            res_file.write(i)
            res_file.write('\n')

        res_file.write('===================================\n\n')


def searchPattern(result_list, pattern):
    for element in result_list:
        mark = False
        with open(element, 'r') as file_obj:
            for line in file_obj:
                for item in pattern:
                    if re.search(
                            item, line
                    ) is None:  # Если тру – то значит не найдено; Если фальш – значит найдено
                        continue
                    else:
                        valid_line.append(line)
                        mark = True

        if mark:
            valid_file.append(element)
        else:
            not_valid_file.append(element)


if __name__ == '__main__':
    import argparse

    main()
