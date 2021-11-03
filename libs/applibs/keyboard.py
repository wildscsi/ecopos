__author__ = 'BM'
# -*- coding: utf-8 -*-

# класс виртуальной клавиатуры

from kivy.uix.vkeyboard import VKeyboard
from copy import deepcopy
from kivymd.app import MDApp

class ekeyboard(VKeyboard):
    layout_path = './data/keyboard'     # путь для языков
    layout = 'ru_RU'                    # выбранная клавиатура
    text = ''                           # возвращаемый текст
    app = None                          # объект приложения
    lclose = False
    rlang = 'en_US'

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        self.chlang()
        super().__init__(**kwargs)

    # замена языка
    def chlang(self):
        if self.app.lang == 'de':   self.layout = 'de_CH'
        elif self.app.lang == 'ru': self.layout = 'ru_RU'
        elif self.app.lang == 'es': self.layout = 'es_ES'
        else:                       self.layout = 'en_US'

    # замена языка по кругу
    def rotatelang(self):
        print('aa')
        lang = deepcopy(self.layout)
        self.layout = deepcopy(self.rlang)
        self.rlang = lang
        self.refresh()

    # обработка нажатия клавишей
    def updkeykode(self, keyboard, keycode, text, modifiers):
        print(keyboard, keycode, text, modifiers)
        # удаление
        if keycode == 'backspace':
            self.text = self.text[0:len(self.text)-1]
            return
        # не обрабатываются
        if keycode in ['tab','capslock','shift','layout','special']: return
        # убрать клаву, записать данные
        if keycode in ['escape','enter']:
            self.lclose = True
            return
        # смена языка
        if keycode == 'lang':
            return self.rotatelang()
        self.text = self.text + text

