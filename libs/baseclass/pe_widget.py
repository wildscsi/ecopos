#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# pe_widget.py
#
# форма редактирования количества и удаления позиции чека
#
from kivymd.app import MDApp
import time
from kivy.uix.label import Label, CoreLabel
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog
from kivy.utils import get_hex_from_color, get_color_from_hex
from libs.base.lbcontrol import Button_, Label_, TextInput_
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRectangleFlatIconButton, MDRaisedButton, MDRectangleFlatButton, MDFlatButton,  MDTextButton, MDIconButton
from kivymd.uix.card import MDCard

from kivymd.uix.label import MDLabel, MDIcon
from libs.base.lbcontrol import Button_
from kivymd.uix.dialog import MDDialog
from kivymd.uix.banner import MDBanner
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
import libs.applibs.equaction as equ
from copy import deepcopy


class pe(RelativeLayout):
    cid = 'cntpe'
    oform = None        # кассовая панель
    evalue = None       # объект с вводимыми цифрами
    obutton = None      # позиция чека

    def __init__(self, **kwargs):
        self.size_hint = [0.95, 0.75]
        self.pos_hint = {'center_x': 0.5, 'center_y': .61}
        self.oform = kwargs.pop('oform')
        self.obutton = kwargs.pop('obutton')
        self.app = MDApp.get_running_app()

        super(pe, self).__init__(**kwargs)
        self.add_input()        # контейнер с полем ввода суммы
        self.add_tovar()        # наименование товара
        self.add_kbd()          # добавляем клавиатуру
        self.add_directbut()    # добавление управляющих кнопок


    # обработка нажатий на кнопки
    def button_click(self, cdate):
        # цифры клавиатуры
        js = None
        #self.inbox.text = '0'

        # ограничение на количество символов после запятой
        if cdate in ['0','1','2','3','4','5','6','7','8','9']:
            if len(self.evalue.text.split('.')) > 1:
                if len(self.evalue.text.split('.')[1]) >1: return

        if cdate in ['0','1','2','3','4','5','6','7','8','9']:
            if len(self.evalue.text) >11: return
            if self.evalue.text == '0': self.evalue.text = ''
            self.evalue.text += cdate
        # точка
        if cdate == '.':
            if len(self.evalue.text) >11: return
            if self.evalue.text.find('.') != -1: return
            self.evalue.text += cdate


        # BACKSPACE
        if cdate == 'BACK':
            self.evalue.text = self.evalue.text[0:len(self.evalue.text)-1]
            if len(self.evalue.text) == 0: self.evalue.text = '0'

        # +1
        if cdate == '+1':
            self.evalue.text = str(float(self.evalue.text)+1)
            self.evalue.text=str(round(float(self.evalue.text),2))

        # +10
        if cdate == '+10':
            self.evalue.text = str(float(self.evalue.text)+10)
            self.evalue.text=str(round(float(self.evalue.text),2))


        # -1
        if cdate == '-1':
            cvalue = float(self.evalue.text)-1
            if cvalue >=0: self.evalue.text = str(cvalue)
            self.evalue.text=str(round(float(self.evalue.text),2))

        # Clear 1
        if cdate == 'C1': self.evalue.text = '1'

        # Clear 10
        if cdate == 'C10': self.evalue.text = '10'

        # удаление блюда
        if cdate == 'DELETE':
            newticket = deepcopy(self.app.aticket)
            self.app.aticket = []
            for item in newticket:
                if item['nn'] != self.obutton['nn']:
                    self.app.aticket.append(item)
            self.oform.buttonclick(self.oform.areturn)
            return self.oform.treload()

        # изменение кол-ва, вызывается из модального окна
        if cdate == 'QNT':
            for item in self.app.aticket:
                if item['nn'] == self.obutton['nn']:
                    item.update({'q':float(self.evalue.text)})
                    break
            self.oform.buttonclick(self.oform.areturn)
            return self.oform.treload()

        #self.evalue.text=str(round(float(self.evalue.text),2))

    #  ------------------------------- фон ------------------------
    def addrect(self):
        # фон контейнера
        with self.canvas.before:
            Color(self.app.color_red)
            self.rect = Rectangle(size=self.size,pos=self.pos)
        def update_fr(instance, value):
            instance.rect.size = instance.size
        self.bind(pos=update_fr, size=update_fr)


    # ------------------------------ наименование товара и кол-во ---------------------------
    def add_tovar(self):
        cnttovar = RelativeLayout(size_hint = [0.8, 0.10], pos_hint = {'center_x': 0.5, 'center_y': .95})
        ltovar = Label_(pos_hint={"center_x": .48, "center_y": .5}, halign='right', valign = 'middle', color=self.app.color_lgray)
        ltovar.text = self.obutton['bname'] + '   ' + str(self.obutton['q']) + '   ' + self.obutton['ei']
        ltovar.bind(size=self.evalue.setter('text_size'))
        cnttovar.add_widget(ltovar)
        self.add_widget(cnttovar)


    # -------------------------------- поле ввода ----------------------------
    def add_input(self):

        ldigit = RelativeLayout(size_hint = [0.675, 0.12], pos_hint = {'center_x': 0.5, 'center_y': .77})
        # фон контейнера
        with ldigit.canvas.before:
            Color(self.app.color_white)
            ldigit.rect = Rectangle(size=ldigit.size ,pos=ldigit.pos)
        def update_ldigit(instance, value):
            instance.rect.size = instance.size
        ldigit.bind(pos=update_ldigit, size=update_ldigit)
        self.evalue = Label_(pos_hint={"center_x": .48, "center_y": .5}, halign='right', valign = 'middle', color=self.app.color_red)
        self.evalue.id = 'evalue'
        self.evalue.text = '0'
        self.evalue.bind(size=self.evalue.setter('text_size'))
        ldigit.add_widget(self.evalue)
        self.add_widget(ldigit)

    # ------------------------------кнопки с цифами ---------------------------
    def add_kbd(self):
        ldig = GridLayout(cols=4, rows=4, padding=5, spacing=3, size_hint =(.7, .6), pos_hint={"center_x": .5, "center_y": .41})

        plus1= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_sblack)
        plus1.on_press=lambda :self.button_click('+1')
        plusbut1 = MDIconButton(color= self.app.color_white, icon = "numeric-positive-1", pos_hint = {"center_x": .5, "center_y": .5})
        plus1.add_widget(plusbut1)
        ldig.add_widget(plus1)

        obut1= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut1.on_press=lambda :self.button_click('1')
        mbut1 = MDIconButton(color= self.app.color_white, icon = "numeric-1", pos_hint = {"center_x": .5, "center_y": .5})
        obut1.add_widget(mbut1)
        ldig.add_widget(obut1)

        obut2= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut2.on_press=lambda :self.button_click('2')
        mbut2 = MDIconButton(color= self.app.color_white, icon = "numeric-2", pos_hint = {"center_x": .5, "center_y": .5})
        obut2.add_widget(mbut2)
        ldig.add_widget(obut2)

        obut3= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut3.on_press=lambda :self.button_click('3')
        mbut3 = MDIconButton(color= self.app.color_white, icon = "numeric-3", pos_hint = {"center_x": .5, "center_y": .5})
        obut3.add_widget(mbut3)
        ldig.add_widget(obut3)

        minus1= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_sblack)
        minus1.on_press=lambda :self.button_click('-1')
        minusbut1 = MDIconButton(color= self.app.color_white, icon = "numeric-negative-1", pos_hint = {"center_x": .5, "center_y": .5})
        minus1.add_widget(minusbut1)
        ldig.add_widget(minus1)

        obut4= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut4.on_press=lambda :self.button_click('4')
        mbut4 = MDIconButton(color= self.app.color_white, icon = "numeric-4", pos_hint = {"center_x": .5, "center_y": .5})
        obut4.add_widget(mbut4)
        ldig.add_widget(obut4)

        obut5= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut5.on_press=lambda :self.button_click('5')
        mbut5 = MDIconButton(color= self.app.color_white, icon = "numeric-5", pos_hint = {"center_x": .5, "center_y": .5})
        obut5.add_widget(mbut5)
        ldig.add_widget(obut5)

        obut6= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut6.on_press=lambda :self.button_click('6')
        mbut6 = MDIconButton(color= self.app.color_white, icon = "numeric-6", pos_hint = {"center_x": .5, "center_y": .5})
        obut6.add_widget(mbut6)
        ldig.add_widget(obut6)

        clear10= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_sblack)
        clear10.on_press=lambda :self.button_click('C10')
        clearbut10 = MDIconButton(color= self.app.color_white, icon = "numeric-10-box", pos_hint = {"center_x": .5, "center_y": .5})
        clear10.add_widget(clearbut10)
        ldig.add_widget(clear10)

        obut7= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut7.on_press=lambda :self.button_click('7')
        mbut7 = MDIconButton(color= self.app.color_white, icon = "numeric-7", pos_hint = {"center_x": .5, "center_y": .5})
        obut7.add_widget(mbut7)
        ldig.add_widget(obut7)

        obut8= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut8.on_press=lambda :self.button_click('8')
        mbut8 = MDIconButton(color= self.app.color_white, icon = "numeric-8", pos_hint = {"center_x": .5, "center_y": .5})
        obut8.add_widget(mbut8)
        ldig.add_widget(obut8)

        obut9= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut9.on_press=lambda :self.button_click('9')
        mbut9 = MDIconButton(color= self.app.color_white, icon = "numeric-9", pos_hint = {"center_x": .5, "center_y": .5})
        obut9.add_widget(mbut9)
        ldig.add_widget(obut9)

        clear1= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_sblack)
        clear1.on_press=lambda :self.button_click('C1')
        clearbut1 = MDIconButton(color= self.app.color_white, icon = "numeric-1-box", pos_hint = {"center_x": .5, "center_y": .5})
        clear1.add_widget(clearbut1)
        ldig.add_widget(clear1)

        obutc= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obutc.on_press=lambda :self.button_click('.')
        mbutc = MDIconButton(color= self.app.color_white, icon = "circle-small", pos_hint = {"center_x": .5, "center_y": .5})
        obutc.add_widget(mbutc)
        ldig.add_widget(obutc)

        obut0= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obut0.on_press=lambda :self.button_click('0')
        mbut0 = MDIconButton(color= self.app.color_white, icon = "numeric-0", pos_hint = {"center_x": .5, "center_y": .5})
        obut0.add_widget(mbut0)
        ldig.add_widget(obut0)

        obutd= MDCard(orientation = 'vertical', radius = [5,5], pos_hint = {"center_x": .5, 'center_y': .5}, size_hint = [1, 1], text_color = self.app.color_white, md_bg_color = self.app.color_lblack)
        obutd.on_press=lambda :self.button_click('BACK')
        mbutd = MDIconButton(color= self.app.color_white, icon = "backspace-outline", pos_hint = {"center_x": .5, "center_y": .5})
        obutd.add_widget(mbutd)
        ldig.add_widget(obutd)

        self.add_widget(ldig)

    # --------------------------- управляющие кнопки ---------------------------
    def add_directbut(self):

        # -------------------- Удаление  -----------------------------
        delbut= MDCard(orientation = 'horizontal', radius = [5,5], pos_hint = {"center_x": .29, 'center_y': .016}, size_hint = [0.25, 0.12], text_color = self.app.color_white, md_bg_color = self.app.bcolor1)
        delbut.on_release=lambda :self.button_click('DELETE')
        dellabel = Label_(pos_hint={"center_x": .5, "center_y": .5},size_hint = [0.8, 0.4], text=self.app.translation._("УДАЛИТЬ"),halign='center',color=self.app.color_red)
        dellabel.bind(size=dellabel.setter('text_size'))
        #izrepbut = MDIconButton(color= self.app.color_white, icon = "backspace-outline", pos_hint = {"center_x": .5, "center_y": .5})
        delbut.add_widget(dellabel)
        self.add_widget(delbut)

        # -------------------- Количество -----------------------------
        qbut= MDCard(orientation = 'horizontal', radius = [5,5], pos_hint = {"center_x": .71, 'center_y': .016}, size_hint = [0.25, 0.12], text_color = self.app.color_white, md_bg_color = self.app.bcolor1)
        qbut.on_release=lambda :self.button_click('QNT')
        qlabel = Label_(pos_hint={"center_x": .5, "center_y": .5},size_hint = [0.8, 0.4], text=self.app.translation._("КОЛИЧЕСТВО"),halign='center',color=self.app.color_white)
        qlabel.bind(size=qlabel.setter('text_size'))
        #izrepbut = MDIconButton(color= self.app.color_white, icon = "backspace-outline", pos_hint = {"center_x": .5, "center_y": .5})
        qbut.add_widget(qlabel)
        self.add_widget(qbut)

