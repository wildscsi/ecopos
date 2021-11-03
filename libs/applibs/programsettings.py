# -*- coding: utf-8 -*-
# Copyright (c) 2020 CPV.BY
# LICENSE:  Commercial
#
# ProgramSettings.py
#
# настройки программы

from kivy.config import ConfigParser
from ast import literal_eval
from libs.translation import Translation
import os

class oConfig():
    oApp = None
    def __init__(self, oApp):
        self.oApp = oApp
        # проверяем, существует ли директорий с настройками
        if not os.path.exists('set'):
            os.makedirs('set')
        self.config = ConfigParser()


    # запись параметра
    def saveconfig(section, option, value):
        config = ConfigParser()
        config.read('{}/set/tconfig.ini')
        config.set(section, option, value)
        config.write()

# чтение файла импорта-экспорта и настройки по умолчанию
def readimpexpconfig(oApp):
    # проверяем, существует ли директорий с настройками
    if not os.path.exists('set'):
        os.makedirs('set')
    config = ConfigParser()
    config.read('set/impexp.ini')
    config.setdefaults('importtype',              {"ptype": "combo" ,"desc": "Тип импортируемого файла",           'pvalue': 'iiko',                     'options':'iiko,dbf'})
    config.setdefaults('importfrom',              {"ptype": "combo" ,"desc": "Тип приёма файла",                   'pvalue': 'directory',                'options':'directory,ftp'})
    config.setdefaults('importdir',               {"ptype": "file" ,"desc": "Директорий импорта файла",            'pvalue': ' ',                        'options':''})

    config.write()
    oApp.impexp = config._sections

# запись параметра
def saveimpexpconfig(section, option, value):
    config = ConfigParser()
    config.read('set/impexp.ini')
    config.set(section, option, value)
    config.write()


# чтение язывовых настроек
def readlang(oApp):
    config = ConfigParser()
    lang = oApp.tconfig.get('lang')
    config.read('set/lang.ini')
    config.setdefaults('ru', {'lang_select':'Выбор языка',
                                            'lang': 'язык',
                                            'lang_desc': 'выберите язык приложения',
                                            'programm_name': 'Касса',
                                            'imp-exp': 'имп-экс',
                                            'import': 'импорт',
                                            'import_setting': 'настройки импорта',
                                            'impexep_desc': 'импорт и экспорт',
                                            'cancel':'отмена',
                                            'save':'сохранить',
                                            'ticket_name':'Чек',
                                            'settings':'Настройки',
                                            'home':'главная',
                                            'info':'инфо',
                                            'exit':'выход',
                                            'Empty_choice':"Ничего не выбрано",
                                            'importtype':'Тип импортируемого файла',
                                            'importtype_desc':'Выберите тип импортируемого файла',
                                            'importfrom':'Тип приёма файла',
                                            'importfrom_desc':'Выберите вариант приниёма файла',
                                            'importdir':'Директорий импорта',
                                            'importdir_desc':'Выберите директорий импорта файла',
                                            'error':'Ошибка',
                                            'wrong_path':'Неверный путь',
                                            'attention':'Внимание',
                                            'import completed':'Импорт успешно завершен',
                                            'not_found_file':'Не найден файл',
                                            'error_imp_file':'Ошибка импорта файла'
                                            })
    config.setdefaults('en', {'lang_select':'Change languige',
                                            'lang': 'language',
                                            'lang_desc': 'select the language of the application',
                                            'programm_name': 'Cashbox',
                                            'imp-exp': 'imp-exp',
                                            'import': 'import',
                                            'import_setting': 'import setting',
                                            'impexep_desc': 'import and export',
                                            'cancel':'cancel',
                                            'save':'save',
                                            'ticket_name':'Ticket',
                                            'settings':'Settings',
                                            'home':'home',
                                            'info':'info',
                                            'exit':'exit',
                                            'Empty_choice':"Empty choice",
                                            'importtype':'Type of file to import',
                                            'importtype_desc':'Choose the type of file to import',
                                            'importfrom':'File Receive Type',
                                            'importfrom_desc':'Choose the option to take the file',
                                            'importdir':'Import Directory',
                                            'importdir_desc':'Select the file import directory',
                                            'error':'Error',
                                            'wrong_path':'Wrong_path',
                                            'attention':'Attention',
                                            'import completed':'Import completed successfully',
                                            'not_found_file':'Not found file',
                                            'error_imp_file':'Error import file'
                                            })


    config.write()
    oApp.lang = config._sections[lang['pvalue']]
