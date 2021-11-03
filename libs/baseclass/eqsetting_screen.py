__author__ = 'smitkevich'
# -*- coding: utf-8 -*-

from kivy.properties import BooleanProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem
from libs.translation import Translation
from libs.baseclass.buttonlib import _MDRaisedButton
from kivymd.uix.label import MDLabel
import os
from copy import deepcopy
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineIconListItem, MDList, IconLeftWidget


class EqsettingScreen(MDScreen):
    list_created = BooleanProperty(False)
    ids_old = []    # предыдущий перечень контролов
    btnhight = 0    # высота котрола
    lopen = True
    kbd = None
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

    # загрузка контролов
    def on_pre_enter(self, *args):
        self.addfr()

    # выход с экрана. Закрываем вкладки
    def on_pre_leave(self, *args):
        self.lopen = True
        if self.btnhight !=0: self.ids['fr'].height = self.btnhight

    # добавление закладки с ФР
    def addfr(self):
        self.cnt_clear()
        mlabel = MDLabel(text=self.app.oeq.listksa[self.app.oeq.ofr['model']]['name'], color=self.app.color_white, font_style='H2', halign='center', pos_hint={"center_x": .8, "center_y": .5}, size_hint_y=None)
        mlabel.id='mlabel'
        self.ids['fr'].add_widget(mlabel)


        #micon = IconLeftWidget(icon= "printer-check")
        #micon.id='micon'
        #self.ids['fr'].add_widget(micon)
        #self.ids['fr'].text = self.app.translation._('Чекопечатающее устройство: ФР, КСА, принтер ')

    # -------------------------------------------   ФР КСА   ----------------------------------------
    # открытие настроек ФР
    def open_frsetting(self, oButton):
        # oButton - контрол кнопки с ФР
        if not self.lopen:
            return True

        self.lopen = False
        # останавливаем скролл основного контейнера, т.к. он мешает скролу со свойствами
        self.ids['eqscroll'].do_scroll_y = False
        self.ids['eqscroll'].do_scroll_x = False
        self.cnt_clear()
        self.btnhight = oButton.height
        oButton.height = oButton.height*6

        # форма с настройками
        self.app.oeq.getform(self, oButton)


    # удаление контролов - контейнера с настройками и название ФР
    def cnt_clear(self):
        for item in self.ids['fr'].children:
            try:
                if item.id in ['mlabel','cnt']: self.ids['fr'].remove_widget(item)
            except: pass



    # закрытие настроек с ФР
    def close_frsetting(self, oButton):
        oButton.height = self.btnhight
        for item in self.ids['fr'].children:
            try:
                if item.id in ['cnt','micon','']: self.ids['fr'].remove_widget(item)
            except: pass

        self.ids['eqscroll'].do_scroll_y = True
        self.ids['eqscroll'].do_scroll_x = True
        self.lopen = True
        aa = 123
        if self.kbd != None:
            self.remove_widget(self.kbd)
            self.kbd = None

        self.addfr()





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

    # подтверждение выбора языка
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

    # подтверждение выбора языка
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