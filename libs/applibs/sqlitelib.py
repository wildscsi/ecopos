# -*- coding: utf-8 -*-
# Copyright (c) 2020 CPV.BY
# LICENSE:  Commercial

# класс работы с локальной БД SQL



# таблицы - GRUPPA, TOVAR, MOD, CASHIER, CLIENT
import os
from libs.base.lbsql import qsql
import json
import time
from datetime import datetime
from libs.applibs.programsettings import oConfig
from kivy.config import ConfigParser


class Oqsql(qsql):
    dbname = 'localdb'
    ctables = 'gruppa','tovar','cashier'
    lopen =False
    dictstru =[]                # структура таблиц
    config = None
    dictstrusave = []         # структурвтаблицы для записи


    def __init__(self, **kwargs):
        super(Oqsql, self).__init__(**kwargs)
        self.sqlstrconnect = self.dbname + '.db'
        self.config = oConfig(oApp = self)
        # проверка наличия БД, при отсутствии-создание БД и таблицctable
        self.dictstru = []
        self.dictstrusave = []
        #if not self.dbcheck_lite():return True

    # проверка наличия БД
    # создание БД при отсутствии
    # сверка структуры БД
    def dbcheck_lite(self):
        if not self.open():return False
        ctxt = "SELECT " + "name FROM sqlite_master WHERE type='table' AND name='tovar';"
        if not self.execute(ctxt): return False
        allrec = self.getresult()
        if len(allrec) > 0: return True

        # Образы берём из файла структур.
        if not self.getstru():return False
        # проверяем наличие таблиц в БД,если нет- создаём
        for item in self.dictstru:
            for ctable in item:
                # пропускаем служебные таблицы
                if ctable in ['index','proc', 'work_id'] : continue
                self.dictstrusave = []
                # формируем структуру
                script = ''
                for csr in item[ctable]:
                    if len(script) > 0: script +=', '
                    script += csr['column'] + ' ' + self.gettype(csr['field'], csr['description'],csr['column'])
                script =   "CREATE TABLE IF NOT EXISTS " + ctable + "(" + script + ")"
                try:

                    self.execute(script)
                    self.commit()
                    aa = 123
                except:
                    self.errmsg = 'Error create sqlite table'
                    return False
                # сохраняем поля сформированной таблицыв настройках
                if not self.savetoini('structure',ctable, self.dictstrusave): return False
        return True

    # импорт структуры таблиц
    def getstru(self):
        cfile = "data/update/structure"
        # проверяем наличие файла со структурой, читаем файл, импортируем структуру
        if not os.path.isfile(cfile):
            self.errmsg = 'Not found structure file'
            return False
        try:
            f = open(cfile, encoding='utf-8')
        except:
            self.errmsg = 'Error reading structure file'
            return False

        alljson = json.loads(f.read())
        if len(alljson) == 0:
            self.errmsg ='Empty structure file'
            return False
        for cstr in alljson:
            self.dictstru.append({cstr:alljson[cstr]})
        f.close()
        return True

    # возвращает тип поля SQL соответствующий структуры и дефолтное значени
    def gettype(self, field, description, column):
        if field == 'serial':
            #self.dictstrusave.append({column:'integer'})
            return "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"
        elif field == 'integer':
            self.dictstrusave.append({column:'integer'})
            return "INTEGER NOT NULL DEFAULT 0"
        elif field == 'text':
            self.dictstrusave.append({column:'text'})
            return "TEXT NOT NULL DEFAULT ''"
        elif field == 'boolean':
            self.dictstrusave.append({column:'integer'})
            return "INTEGER NOT NULL DEFAULT 0"
        elif field == 'character':
            self.dictstrusave.append({column:'TEXT'})
            return "TEXT NOT NULL DEFAULT ''"
        elif field == 'decimal':
            self.dictstrusave.append({column:'real'})
            return "REAL NOT NULL DEFAULT 0"
        elif field == 'timestamp':
            self.dictstrusave.append({column:'integer'})
            default = datetime.today()
            unixtime = time.mktime(default.timetuple())
            return "INTEGER NOT NULL DEFAULT " + str(unixtime)
        else:
            self.dictstrusave.append({column:'text'})
            return 'TEXT NOT NULL DEFAULT "" '

    # сохранение структуры
    def savetoini(self, structure,option, value):
        config = ConfigParser()
        config.read('set/worksetting.ini')
        try:
            config.setdefaults('tblstru',{option: value })
            config.write()
        except:
            self.errmsg = 'Error save structure table'
            return False
        return True

    def select(self,ctable, cwhere):
        if len(cwhere) > 0:
            if not self.execute('SELECT ' + '* FROM ' + ctable +' WHERE ' + cwhere+ ';'):
                return False
        else:
            if not self.execute('SELECT ' + '* FROM ' + ctable + ';'):
                return False
        return True

    # вставляем данные в таблицу
    def insert(self, ctable, dictdata):
        column = ''; value =''
        for item in dictdata:
            if len(column) != 0: column += ', '
            if len(value) != 0: value += ', '
            column += item
            if type(dictdata[item]) != str: value  += str(dictdata[item])
            else: value  += '"'+dictdata[item]+'"'
        if not self.execute('INSERT INTO ' + ctable + '(' + column + ') VALUES('+ value +');' ): return False
        return True

    # удаление строк
    def delete(self, ctable, cwhere):
        csript = 'DELETE FROM '+ ctable + ' WHERE '+ cwhere +';'
        if not self.execute(csript): return False
        return True

    # обновление данных
    def update(self,ctable, dictdata, cwhere):
        cstr =''
        for item in dictdata:
            if len(cstr) != 0: cstr += ', '
            cstr += item + '='
            if type(dictdata[item]) != str: cstr  += str(dictdata[item])
            else: cstr  += '"'+dictdata[item]+'"'

        csript = 'UPDATE '+ ctable + ' SET '+ cstr + ' WHERE ' + cwhere +';'
        if not self.execute(csript): return False
        return True