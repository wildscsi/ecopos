#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# модуль с общими функциями


import zipfile, os
import datetime
import random


# разархивирование файла (путь для разархивации , имя и путь архивного файла)
def unzip(cpath, cfile):
    try:
        fh = open(cfile, 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            z.extract(name, cpath)
        fh.close()
    except: return False
    return True

# делает из курсора dict
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

# удалить директорий
def DeleteDir(dir):
    for name in os.listdir(dir):
        file = os.path.join(dir, name)
        if not os.path.islink(file) and os.path.isdir(file):
            DeleteDir(file)
        else:
            os.remove(file)
    os.rmdir(dir)

# рекурсивная обработка директория
def DeleteFileDir(dir):
    for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
        for name in files:
            fullname = os.path.join(root, name) # получаем полное имя файла
            os.remove(fullname)                 # удаляем


# пишем данные в файл
def writeFile(content, fileName):
    # открываем для записи
    try:
        file = open(fileName, 'wb')
    except:
        return False

    file.write(content)
    # flush content so that file will be modified.
    file.flush()
    # close file
    file.close()

# открываем фпйл в режиме read
def openFile(fileName, mode, context):
    try:
        fileHandler = open(fileName, mode)
        return {'opened':True, 'handler':fileHandler}
    except IOError:
        context['error'] += 'Unable to open file ' + fileName + '\n'
    except:
        context['error'] += 'Unexpected exception in openFile method.\n'
    return {'opened':False, 'handler':None}

# выгрузка в ODS
# GET, таблица, поле по которому ещем
def odsexp(request,table,cfields):
    cpath = ''
    cfile = 'report_' + str(request.user.pk) + '_' + str(int(random.random()*10000)) + '.odt'
    # есть ли в пост-запроск период дат
    if 'ds_year' in request.GET and 'de_year' in request.GET:
        ds = validTime(request.GET['ds_year'],request.GET['ds_month'],request.GET['ds_day'],'00:00:00')
        de = validTime(request.GET['de_year'],request.GET['de_month'],request.GET['de_day'],'23:59:59')
        otable=eval(table + ".objects.filter("+cfields+"__gte = '"+ds+"').filter("+cfields+"__lte='"+de+"')")
    else:
        otable = eval(table +'.objects.all()')
    posts = otable.values()
    with ods.writer(open(cpath+cfile, "wb")) as odsfile:
        i = 0
        for post in posts:
            if i == 0:
                # записываем шапку
                odsfile.writerow(post.keys())
            odsfile.writerow(post.values())
            i = i+1


# проверка на валидность даты (YYYY.MM,DD,HH:MM). Возвращает валидную дата - время
def validTime(cY,cM,cD,cT):
    lret = False
    while lret is False:
        lret = validDate(cY,cM,cD)
        if lret == False:
            cD=str(int(cD)-1)
    return cY+'-'+cM+'-'+ cD+' '+cT

def validDate(y, m, d):
    Result = True
    try:
        datetime.strptime(y+'-'+m+'-'+d,'%Y-%m-%d')
    except ValueError:
        Result = False
    return Result

