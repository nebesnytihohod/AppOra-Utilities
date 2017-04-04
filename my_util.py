#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re

"""
получить список каталогов следующего уровня
получить список файлов на текущем уровне
проверить на исключения
файлы последовательно открыть, проверить внутри
зайти в следуующий каталог
повторить

os.chdir(path) - смена текущей директории.
os.getcwd() - текущая рабочая директория.
os.listdir(path=".") - список файлов и директорий в папке.
os.path.isfile(path) - является ли путь файлом.
os.path.isdir(path) - является ли путь директорией.
os.path.dirname(path) - возвращает имя директории пути path.
os.path.abspath(path) - возвращает нормализованный абсолютный путь.
os.path.basename(path) - базовое имя пути (эквивалентно os.path.split(path)[1]).
os.path.normcase(path) - нормализует регистр пути (на файловых системах, не учитывающих регистр, приводит путь к нижнему регистру).
os.path.normpath(path) - нормализует путь, убирая избыточные разделители и ссылки на предыдущие директории. На Windows преобразует прямые слеши в обратные.
os.path.realpath(path) - возвращает канонический путь, убирая все символические ссылки (если они поддерживаются).
os.path.relpath(path, start=None) - вычисляет путь относительно директории start (по умолчанию - относительно текущей директории).

"""
list_dir = []
list_file = []
list_fs_object = []
res = []
nv = []
exclude = ['log', 'css', 'htm', 'help', 'image', 'res', 'img', 'font', 'doс',
 'form', 'error', 'tmp', 'temp', 'db', 'png', 'gif', 'jpg', 'pdf', 'manifest', 'mf',
 'js', 'jar', 'war', 'jsp']

current_dir = os.getcwd()
list_fs_object = os.listdir(current_dir)

print('current directory ', current_dir)
print('-----------------------')
print('list of dir ', list_fs_object)

def sort(ld, excl):
    for i in ld:
        tmp=False
        for e in excl:
            if i.find(e) != -1:
                tmp=True
                break
        if tmp:
            nv.append(i)
        else:
            res.append(i)
    return

sort(list_fs_object, exclude)
print('res ', res)
print('-------------------------------')
print('nv ', nv)

for i in res:
	if os.path.isfile(i):
		list_file.append(i)
	elif os.path.isdir(i):
		list_dir.append(i)
		#ld = os.listdir(i)

print('file ', list_file)
print('-------------------------------')
print('directory ', list_dir)

for x in list_dir:
	list_fs_object = os.listdir(x)
	print('--------------------===>', x)
	print('list of dir ', list_fs_object)
	sort(list_fs_object, exclude)
	print('res ', res)
	print('-------------------------------')
	print('nv ', nv)