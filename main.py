# -*- coding: utf-8 -*-

"""

ECOPOS
=============
HoReCa & Retail 2022

# Copyright (c) 2022 CPV.BY
# LICENSE:  Commercial

"""

import os, sys, platform
from pathlib import Path
from kivy.lang import Builder
from kivy.utils import get_hex_from_color, get_color_from_hex
from kivy.config import ConfigParser
from kivymd.app import MDApp
from ast import literal_eval
from libs.translation import Translation
from libs.applibs.sqlitelib import Oqsql        # sql
from libs.applibs.calclib import Calc           # расчёты
from libs.applibs.eq import eq                  # работа с оборудованием
from libs.applibs.keyboard import ekeyboard
import libs.applibs.equaction as equ

if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["RALLY_ROOT"] = sys._MEIPASS
else:
    os.environ["RALLY_ROOT"] = str(Path(__file__).parent)


KV_DIR = f"{os.environ['RALLY_ROOT']}/libs/kv/"

for kv_file in os.listdir(KV_DIR):
    with open(os.path.join(KV_DIR, kv_file), encoding="utf-8") as kv:
        Builder.load_string(kv.read())

KV = """
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import RallyRegisterScreen libs.baseclass.register_screen.RallyRegisterScreen
#:import RallyRootScreen libs.baseclass.root_screen.RallyRootScreen
#:import AboutScreen libs.baseclass.about_screen.AboutScreen
#:import ImpexpScreen libs.baseclass.impexp_screen.ImpexpScreen
#:import KassaScreen libs.baseclass.kassa_screen.KassaScreen

ScreenManager:
    transition: FadeTransition()

    RallyRootScreen:
        name: "rally root screen"

    RallyRegisterScreen:
        name: "rally register screen"

    AboutScreen:
        name: "about screen"

    ImpexpScreen:
        name: "impexp screen"

    KassaScreen:
        name: "kassa screen"
"""

class ecopos(MDApp):
    lang = 'en'
    platform = None
    osql = None
    oeq = None          # объект оборудования
    kob = 10            # номер объекта
    cval = '$'          # валюта
    iround = 2          # округление
    alldsc = 0          # общая скидка
    aticket=[]          # перечень позиций чека
    aticket_save=[]     # сохранённый чек
    version = '1.1'     # номер версии для сборки и About
    keyboard = None     # виртуальная клавиатура
    lalldsc = False     # применение общей скидки
    firm = ''           # название организации
    addressfirm = ''    # адресс организации
    inn = ''            # УНН - ИНН

    # цвета ------------------------------------------------------------------------------------
    main_background = get_color_from_hex('ffffff')
    color_white = get_color_from_hex('ffffff')
    color_gray = get_color_from_hex('757575')
    color_lgray = get_color_from_hex('a7a7a7')
    color_igray = get_color_from_hex('d5d5d5')
    color_green = get_color_from_hex('85ba6f')
    color_dgreen = get_color_from_hex('288023')
    color_sgray = get_color_from_hex('515151')
    color_black = get_color_from_hex('000000')
    color_lblack = get_color_from_hex('33464d')
    color_sblack = get_color_from_hex('3f565f')

    color_blue = get_color_from_hex('2196f3')
    color_lblue = get_color_from_hex('efedff')
    color_darkblue = get_color_from_hex('5b93c8')
    color_hdarkblue = get_color_from_hex('4176a2')
    color_red = get_color_from_hex('ff0000')
    color_search = get_color_from_hex('ffee00')
    color_but = get_color_from_hex('f5f5f5')
    bcolor1 = get_color_from_hex("#60a8f0")
    bcolor2 = get_color_from_hex('589dd4')
    bcolor3 = get_color_from_hex('3f6f9c')
    bcolor4 = get_color_from_hex('f6f6f6')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'ecopos'
        self.icon = f"{os.environ['RALLY_ROOT']}/assets/images/logo.png"
        icon = 'icon.png'
        self.config = ConfigParser()
        self.window_language = None
        self.translation = Translation(self.lang, 'ecopos', os.path.join(self.directory, 'data', 'locales'))
        self.dict_language = literal_eval(open(os.path.join(self.directory, 'data', 'locales', 'locales.txt')).read())
        self.dict_cval = {'€': 'EUR', '$': 'Dollar', 'R': 'Рубль',' ': self.translation._('не используется')}
        self.dict_iround = {'2': '11.11', '1': '11.10', '0': '11.00', '-1': '10.00'}

        # объект фискальника

        self.ofr1 = {'model':'comcheck','file':'ticket.txt','tapewidth':40,
                        'upper':1,'tags':1,'codepage':'cp866','scode':[27,64,27,116,7],'ecode':[27,100,4,29,86,49],
                        'config':{'port':'/dev/ttyUSB0','baud':19200,'bits':8,'parity':'N','stop':0,'soft':0,'hard':0}}



        # SENOR
        #self.ofr =  {'model':'comcheck','file':'ticket.txt','tapewidth':40,
        #      'upper':1,'tags':1,'codepage':'cp866','scode':[27,64,27,116,17],'ecode':[27,100,4,29,86,49],
        #      'config':{'port':'COM3','baud':115200,'bits':8,'parity':'N','stop':0,'soft':0,'hard':0}}
        # настройки приложения
        self.sodll = ''
        self.setvalue()


    # настройки приложения
    def setvalue(self):
        # выбор загружаемой DLL в зависимости от ОС
        self.platform = platform.system()
        if platform.system() == "Windows":
            self.sodll = './dll/data.dll'
        elif platform.system() == "Linux":
            self.sodll = './so64/data.so'
        else:
            self.sodll = './soarm/data.so'

        #создание директория
        try:
            os.mkdir('temp')
        except OSError:
            print ("Error create dir TEMP")

        self.osql = Oqsql()                 # объект SQL
        self.ocalc = Calc(self)             # объект расчёта сумм
        self.oeq = eq()                     # объект оборудования

        # виртуальная клавиатура для DESKTOP версий
        if platform.system() in ["Windows","Linux"]: self.keyboard= ekeyboard()

        if not self.osql.dbcheck_lite(): return False

    # Загрузка настроек из файла настроек. Создание файла настроек
    def set_value_from_config(self):
        if not os.path.exists(self.directory+'/'+self.name+'.ini'):
            # файла конфига нет - создаём
            self.config.filename = self.directory+'/'+self.name+'.ini'
            self.config.adddefaultsection('General')
            self.config.setdefault('General', 'language', 'en')
            self.config.setdefault('General', 'currency', '€')
            self.config.setdefault('General', 'rounding', '2')
            self.config.setdefault('General', 'alldsc', '1')
            self.config.setdefault('General', 'firm', 'T-E-S-T Company')
            self.config.setdefault('General', 'addressfirm', 'Vanencia, Ctra Del Pi, 100')
            self.config.setdefault('General', 'inn', '100100100')
            self.config.write()

        # читаем общие настройки
        self.config.read(os.path.join(self.directory, self.name+'.ini'))
        try: self.lang = self.config.get('General', 'language')
        except: pass
        try: self.cval = self.config.get('General', 'currency')
        except: pass
        try: self.iround = int(self.config.get('General', 'rounding'))
        except: pass
        try: self.alldsc = int(self.config.get('General', 'alldsc'))
        except: pass
        try: self.firm = self.config.get('General', 'firm')
        except: pass
        try: self.addressfirm = self.config.get('General', 'addressfirm')
        except: pass
        try: self.inn = self.config.get('General', 'inn')
        except: pass

        self.translation = Translation(self.lang, 'ecopos', os.path.join(self.directory, 'data', 'locales'))
        # читаем настройки оборудования
        self.oeq.getini()
        # установка языка DLL. При смене языка, язык в DLL тоже меняем
        js = {'class':'setvalue','name':'lang','value':self.lang}
        equ.action(js)
        js = {'class':'getvalue','name':'lang'}


    def build(self):
        self.set_value_from_config()                # читаем настройки приложения
        self.oeq.getini()                           # читаем настройки оборудования
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        FONT_PATH = f"{os.environ['RALLY_ROOT']}/assets/fonts/"

        self.theme_cls.font_styles.update(
            {
                "H1": [FONT_PATH + "RobotoCondensed-Light", 96, False, -1.5],
                "H2": [FONT_PATH + "RobotoCondensed-Regular", 20, False, 0],
                "H3": [FONT_PATH + "Eczar-Regular", 48, False, 0],
                "H4": [FONT_PATH + "RobotoCondensed-Regular", 34, False, 0.25],
                "H5": [FONT_PATH + "RobotoCondensed-Regular", 24, False, 0],
                "H6": [FONT_PATH + "RobotoCondensed-Bold", 20, False, 0.15],
                "H7": [FONT_PATH + "RobotoCondensed-Regular", 15, False, 0.15],
                "Subtitle1":[FONT_PATH + "RobotoCondensed-Regular", 16, False, 0.15, ],
                "Subtitle2":[FONT_PATH + "RobotoCondensed-Medium",  14, False, 0.1,  ],
                "Body1":    [FONT_PATH + "Eczar-Regular", 16, False, 0.5],
                "Body2":    [FONT_PATH + "RobotoCondensed-Light", 14, False, 0.25],
                "Button":   [FONT_PATH + "RobotoCondensed-Bold", 14, True, 1.25],
                "Caption":  [FONT_PATH + "RobotoCondensed-Regular", 12, False, 0.4,],
                "Overline": [FONT_PATH + "RobotoCondensed-Regular",10, True,  1.5,],
                "Money":    [FONT_PATH + "Eczar-SemiBold", 48, False, 0],
            }
        )
        return Builder.load_string(KV)


ecopos().run()
