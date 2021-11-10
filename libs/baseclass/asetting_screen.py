# -*- coding: utf-8 -*-

from kivy.properties import BooleanProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem
from libs.translation import Translation
from libs.baseclass.buttonlib import _MDRaisedButton
import os, platform
from kivy.uix.textinput import TextInput
from copy import deepcopy
from libs.applibs.keyboard import ekeyboard
import libs.applibs.equaction as equ


class AsettingScreen(MDScreen):
    list_created = BooleanProperty(False)
    dialogcval      = None
    dialogiround    = None
    efirm           = ''        # контрол ввода назваия организации
    eaddressfirm    = ''        # контрол с внесением адреса фирмы
    kbd = None                  # клавиатура

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)


    # -------------------------------------------------- Название фирмы -------------------------------------------------

    # редактирование названия фирмы: выводим название и кнопку записи
    def show_firm_dialog(self):
        if self.kbd !=None: return
        # уменьшаем контрол с Label названием
        self.ids['lfirm'].font_style = 'Overline'
        # добавляем поле ввода
        self.efirm = TextInput(text=self.app.firm, hint_text=self.app.translation._('Название организации'),pos_hint = {"center_x": .8, "center_y": .5}, size_hint=(0.35,0.7))
        self.ids['listlfirm'].add_widget(self.efirm)
        self.efirm.focus = True

        # подключаем клаву
        if platform.system() in ["Windows","Linux"]:
            self.kbd = ekeyboard()
            self.kbd.bind(on_key_up = self._on_keyboard_up)
            self.kbd.text = self.efirm.text
            self.kbd.lclose = False
            self.add_widget(self.kbd)


    # обработка нажатий кнопок названия фирмы
    def _on_keyboard_up(self, keyboard, keycode, text, modifiers):
        self.kbd.updkeykode(keyboard, keycode, text, modifiers)
        if self.kbd.lclose:
            if len(self.efirm.text) > len(self.kbd.text):
                result = self.efirm.text
            else:
                result = deepcopy(self.kbd.text)
            self.ids['listlfirm'].remove_widget(self.efirm)
            self.efirm = None
            self.ids['lfirm'].font_style = 'H6'
            self.ids['lfirm'].text= result
            self.remove_widget(self.kbd)
            self.kbd = None

            self.app.firm = result
            self.app.config.set('General', 'firm', self.app.firm)
            self.app.config.write()
        else:
            self.efirm.text = self.kbd.text


    # -------------------------------------------------- Адрес фирмы -------------------------------------------------

    # редактирование названия фирмы: выводим название и кнопку записи
    def show_addressfirm_dialog(self):
        if self.kbd !=None: return
        # уменьшаем контрол с Label названием
        self.ids['laddressfirm'].font_style = 'Overline'
        # добавляем поле ввода
        self.eaddressfirm = TextInput(text=self.app.addressfirm, hint_text=self.app.translation._('Адрес организации'),pos_hint = {"center_x": .8, "center_y": .5}, size_hint=(0.35,0.7))
        self.ids['listaddressfirm'].add_widget(self.eaddressfirm)
        self.eaddressfirm.focus = True
        #self.eaddressfirm.show_keyboard()
        if platform.system() in ["Windows","Linux"]:
            self.kbd = ekeyboard()
            self.kbd.bind(on_key_up = self._on_keyboard_up_addressfirm)
            self.kbd.text = self.eaddressfirm.text
            self.kbd.lclose = False
            self.add_widget(self.kbd)




    # обработка нажатий кнопок названия фирмы
    def _on_keyboard_up_addressfirm(self, keyboard, keycode, text, modifiers):
        self.kbd.updkeykode(keyboard, keycode, text, modifiers)
        if self.kbd.lclose:
            if len(self.eaddressfirm.text) > len(self.kbd.text):
                result = self.eaddressfirm.text
            else:
                result = deepcopy(self.kbd.text)
            self.ids['listaddressfirm'].remove_widget(self.eaddressfirm)
            self.eaddressfirm = None
            self.ids['laddressfirm'].font_style = 'H6'
            self.ids['laddressfirm'].text= result
            self.remove_widget(self.kbd)
            self.kbd = None
            self.app.addressfirm = result
            self.app.config.set('General', 'addressfirm', self.app.addressfirm)
            self.app.config.write()
        else:
            self.eaddressfirm.text = self.kbd.text

    # -------------------------------------------------- ИНН - УНН-------------------------------------------------

    # редактирование инн: выводим название и кнопку записи
    def show_inn_dialog(self):
        if self.kbd !=None: return
        # уменьшаем контрол с Label названием
        self.ids['linn'].font_style = 'Overline'
        # добавляем поле ввода
        self.einn = TextInput(text=self.app.inn, hint_text=self.app.translation._('ИНН'),pos_hint = {"center_x": .8, "center_y": .5}, size_hint=(0.35,0.7))
        self.ids['listinn'].add_widget(self.einn)
        self.einn.focus = True
        if platform.system() in ["Windows","Linux"]:
            self.kbd = ekeyboard()
            self.kbd.bind(on_key_up = self._on_keyboard_up_inn)
            self.kbd.text = self.einn.text
            self.kbd.lclose = False
            self.add_widget(self.kbd)


    # обработка нажатий кнопок инн
    def _on_keyboard_up_inn(self, keyboard, keycode, text, modifiers):
        self.kbd.updkeykode(keyboard, keycode, text, modifiers)
        if self.kbd.lclose:
            if len(self.einn.text) > len(self.kbd.text):
                result = self.einn.text
            else:
                result = deepcopy(self.kbd.text)
            self.ids['listinn'].remove_widget(self.einn)
            self.einn = None
            self.ids['linn'].font_style = 'H6'
            self.ids['linn'].text= result
            self.remove_widget(self.kbd)
            self.kbd = None
            self.app.inn = result
            self.app.config.set('General', 'inn', self.app.inn)
            self.app.config.write()
        else:
            self.einn.text = self.kbd.text



    # -------------------------------------------------- Валюта -------------------------------------------------

    # диалог выбора валюты
    def show_val_dialog(self):
        def select_locale(name_locale):
            for locale in self.app.dict_language.keys():
                if name_locale == self.app.dict_language[locale]:
                    self.app.cval = locale
                    self.app.config.set('General', 'currency', self.app.cval)
                    self.app.config.write()

        items = []; i=0
        for ival in self.app.dict_cval.keys():

            items.append(ItemConfirm(text=ival.upper() +' ('+ self.app.dict_cval[ival] +')'))
            # отметка выбранной валюты
            if self.app.cval == ival:
                items[i].ids.check.active = True
            else:
                items[i].ids.check.active = False
            i+=1
        self.dialogcval = MDDialog(
            title=self.app.translation._("Выбор валюты"),
            type="confirmation",
            md_bg_color=self.app.bcolor3,
            items = items,
            buttons=[
                MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogcval_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.chcval),
            ],
        )
        self.dialogcval.open()

    # кнопка закрытия диалога выбора валюты
    def dialogcval_close(self, *args):
        self.dialogcval.dismiss(force=True)

    # подтверждение выбора валюты
    def chcval(self, *args):
        self.dialogcval_close()
        for item in self.dialogcval.items:
            if item.ids.check.active:
                # сохраняем значение на приложении и в настройках
                self.app.config.set('General', 'currency', item.text[0:1])
                self.app.config.write()
                self.app.cval = item.text[0:1]
                self.ids['cval'].text = item.text[0:1]
                break

    # --------------------------------- Округление ------------------------------------
    # диалог выбора округления
    def show_iround_dialog(self):
        def select_locale(name_locale):
            for locale in self.app.dict_iround.keys():
                if name_locale == self.app.dict_iround[locale]:
                    self.app.iround = locale
                    self.app.config.set('General', 'rounding', self.app.iround)
                    self.app.config.write()

        items = []; i=0
        for iround in self.app.dict_iround.keys():
            items.append(ItemConfirm(text=iround +' ('+ self.app.dict_iround[iround] +')'))
            # отметка выбранной валюты
            if str(self.app.iround) == iround:
                items[i].ids.check.active = True
            else:
                items[i].ids.check.active = False
            i+=1
        self.dialogiround = MDDialog(
            title=self.app.translation._("Выбор округления"),
            type="confirmation",
            md_bg_color=self.app.bcolor3,
            items = items,
            buttons=[
                MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogiround_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.chiround),
            ],
        )
        self.dialogiround.open()

    # кнопка закрытия диалога выбора валюты
    def dialogiround_close(self, *args):
        self.dialogiround.dismiss(force=True)

    # подтверждение выбора округления
    def chiround(self, *args):
        self.dialogiround_close()
        for item in self.dialogiround.items:
            if item.ids.check.active:
                # сохраняем значение на приложении и в настройках
                self.app.config.set('General', 'rounding', item.text[0:2].strip())
                self.app.config.write()
                self.app.iround =  item.text[0:2].strip()
                self.ids['iround'].text = self.app.iround
                break


    # -------------------------------------------------- Общая скидка -------------------------------------------------

    def alldscch(self, *arg):
        self.app.alldsc = int(arg[0].value)
        self.app.config.set('General', 'alldsc', str(self.app.alldsc))
        self.app.config.write()
        self.ids['alldsc'].text = str(self.app.alldsc) + " %"
        #print(int(arg[0].value))



# отметка чек-бокса при нажатии на название
class ItemConfirm(OneLineAvatarIconListItem):
    divider = None
    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False