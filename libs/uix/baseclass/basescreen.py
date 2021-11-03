# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 CPV.BY
#
# For suggestions and questions:
# <7664330@gmail.com>
#
# LICENSE: Commercial

from kivy.uix.screenmanager import Screen, ScreenManager
from ctypes import *                                        # для DLL
from kivy.uix.relativelayout import RelativeLayout
from libs.base.lbcontrol import Button_
from libs.uix.baseclass.buttonlib import TPButton, GPButton
from copy import deepcopy
from kivy.clock import Clock
from kivymd.material_resources import DEVICE_TYPE
from kivy.app import App



class BaseScreen(Screen):
    oApp = None


    def on_enter(self, *args):
        # вызов через 1 сек кассу

        aa = 123
        #self.manager.get_screen('about')
        #запускаем кассу
        Clock.schedule_once(lambda dt: App._running_app.show_license(), 1)




    def start(self):
        pass





    # первый метод DLL
    def opendll1(self):
        self.oApp = self.manager.parent.oApp
        print("Открываем DLL. Метод 1")
        cpath = self.oApp.dllpath
        if self.oApp.platform == 'Linux':
            libc = cdll.LoadLibrary("./so64/libsehio.so")
            print("1")
            self.ids['opendll'].text = 'dll open'
            result = libc.execsql(12)
            print(result)
            self.ids['emsg'].text += '. DLL вернула :'+str(result)
            print("3")
        elif self.oApp.platform == 'Windows':
            pass
        else:
            libc = cdll.LoadLibrary("./soarm/libsehio.so")
            print("1")
            self.ids['opendll'].text = 'dll open'
            result = libc.execsql(12)
            print(result)
            self.ids['emsg'].text += '. DLL вернула :'+str(result)
            print("3")


