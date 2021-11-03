#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# buttonlib.py
#
# кнопки.
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

class fr(RelativeLayout):
    cid = 'cntfr'
    evalue = None      # объект с вводимыми цифрами
    vnesenie = None    # контрол внесения денег
    vyplata = None     # контрол выплаты
    inbox = None       # контрол суммы в ящике
    dialogerror = None # pop-up с ошибкой

    def __init__(self, **kwargs):
        self.size_hint = [0.95, 0.75]
        self.pos_hint = {'center_x': 0.5, 'center_y': .61}
        self.app = MDApp.get_running_app()


        super(fr, self).__init__(**kwargs)
        #self.addrect()
        self.add_lcont()        # контейнер с информационными полями
        self.add_input()        # контейнер с полем ввода суммы
        self.add_directbut()    # добавление управляющих кнопок


    # обработка нажатий на кнопки
    def button_click(self, cdate):
        # цифры клавиатуры
        js = None
        self.vnesenie.text = '0'
        self.vyplata.text = '0'
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

        # X - отчёт
        if cdate == 'X-REP':
            print('X-REP')
            js = {'class':'setvalue','name':'lang','value':self.app.lang}; equ.action(js)
            #js = {'class':'setarray','name':'payname','value':self.app.config.get('KSA','payname')};equ.action(js)
            js = {'class':'equ','model':'cashreg','cmd':'equprintreport','data':{'cashier':'Андрей Фокин','type':'xrep'}}


        # Z - отчёт
        if cdate == 'Z-REP':
            print('Z-REP')
            js = {'class':'setvalue','name':'lang','value':self.app.lang}; equ.action(js)
            #js = {'class':'setarray','name':'payname','value':self.app.config.get('KSA','payname')};equ.action(js)
            c1 = 'Возникла проблема с чеком. Кончилась бумага, но Титан сохранил чек у себя.'
            js = {'class':'equ','model':'cashreg','cmd':'equprintreport','data':{'cashier':'Лена Пинягина','type':'zrep','note':c1}}

        # Денег в ящике
        if cdate == 'INBOX':
            self.inbox.text = '0'
            js = {'class':'equ','model':'cashreg','cmd':'equgetcash'}

        # Внесение
        if cdate == 'CASHIN':
            if float(self.evalue.text) == 0: return
            self.vnesenie.text = self.evalue.text
            self.evalue.text = '0'
            js = {'class':'setvalue','name':'lang','value':self.app.lang}; equ.action(js)
            js = {'class':'equ','model':'cashreg','cmd':'equcashin','data':{'suma':float(self.evalue.text),'cashier':'Машка Иванова'}}


        # выплата
        if cdate == 'CASHOUT':
            if float(self.evalue.text) == 0: return
            self.vyplata.text = self.evalue.text
            self.evalue.text = '0'
            js = {'class':'setvalue','name':'lang','value':self.app.lang}; equ.action(js)
            js = {'class':'equ','model':'cashreg','cmd':'equcashout','data':{'suma':float(self.evalue.text)}}

        # печать документа на КСА
        if js:
            js ['device'] = self.app.oeq.ofr
            js['headers'] = [self.app.firm,self.app.addressfirm]
            result = equ.action(js)
            # подсвечиваем значение суммы в ящике
            if cdate == 'INBOX' and result[4]:
                self.inbox.text = result[2]['result']

            # обработка ошибок
            self.dialogerror = None
            if not result[4]:
                self.dialogerror = MDDialog(
                    title=self.app.translation._("Ошибка") + ": " + result[2]['message'],
                    md_bg_color=self.app.color_red,
                    buttons=[MDFlatButton(text=self.app.translation._('ЗАКРЫТЬ'),font_style="Button",on_release=self.dialogerror_close),
                        ],)
                self.dialogerror.open()

    # закрытие окна с ошибкой кассы
    def dialogerror_close(self, *args):
        self.dialogerror.dismiss(force=True)


    #  ------------------------------- фон ------------------------
    def addrect(self):
        # фон контейнера
        with self.canvas.before:
            Color(self.app.color_red)
            self.rect = Rectangle(size=self.size,pos=self.pos)
        def update_fr(instance, value):
            instance.rect.size = instance.size
        self.bind(pos=update_fr, size=update_fr)

    # -------------------------------- информационное табло с суммами ----------------------------
    def add_lcont(self):

        lcont = RelativeLayout(size_hint = [0.3, 0.7], pos_hint = {'center_x': 0.19, 'center_y': .48})
        # фон контейнера

        with lcont.canvas.before:
            Color(self.app.color_blue)
            lcont.rect = Rectangle(size=lcont.size ,pos=lcont.pos)
        def update_lcont(instance, value):
            instance.rect.size = instance.size
        lcont.bind(pos=update_lcont, size=update_lcont)

        tname_lay_1 = RelativeLayout(size_hint=[0.95,0.07], pos_hint={"center_x": .5, "center_y": 0.95})
        tname1 = Label_(pos_hint={"center_x": .5, "center_y": 0.5},text=self.app.translation._("Номер Z отчёта"),halign='left',color=self.app.color_gray)
        tname1.bind(size=tname1.setter('text_size'))
        tname_lay_1.add_widget(tname1)
        lcont.add_widget(tname_lay_1)

        tname_lay_2 = RelativeLayout(size_hint=[0.95,0.07], pos_hint={"center_x": .5, "center_y": 0.75})
        tname2 = Label_(pos_hint={"center_x": .5, "center_y": 0.5},text=self.app.translation._("Сумма наличных"),halign='left',color=self.app.color_gray)
        tname2.bind(size=tname2.setter('text_size'))
        tname_lay_2.add_widget(tname2)
        lcont.add_widget(tname_lay_2)

        tname_lay_3 = RelativeLayout(size_hint=[0.95,0.07], pos_hint={"center_x": .5, "center_y": 0.55})
        tname3 = Label_(pos_hint={"center_x": .5, "center_y": 0.5},text=self.app.translation._("Сумма внесения"),halign='left',color=self.app.color_gray)
        tname3.bind(size=tname3.setter('text_size'))
        tname_lay_3.add_widget(tname3)
        lcont.add_widget(tname_lay_3)

        tname_lay_4= RelativeLayout(size_hint=[0.95,0.07], pos_hint={"center_x": .5, "center_y": 0.35})
        tname4 = Label_(pos_hint={"center_x": .5, "center_y": 0.5},text=self.app.translation._("Сумма выплаты"),halign='left',color=self.app.color_gray)
        tname4.bind(size=tname4.setter('text_size'))
        tname_lay_4.add_widget(tname4)
        lcont.add_widget(tname_lay_4)

        ename_lay_1= RelativeLayout(size_hint=[0.85,0.12], pos_hint={"center_x": .5, "center_y": 0.85})
        ename1 = Label_(pos_hint={"center_x": .5, "center_y": 0.5}, text=self.app.translation._("0"),halign='left',color=self.app.color_black)
        ename1.bind(size=ename1.setter('text_size'))
        ename_lay_1.add_widget(ename1)
        lcont.add_widget(ename_lay_1)

        ename_lay_2= RelativeLayout(size_hint=[0.85,0.12], pos_hint={"center_x": .5, "center_y": 0.65})
        self.inbox = Label_(pos_hint={"center_x": .5, "center_y": 0.5}, text=self.app.translation._("0"),halign='left',color=self.app.color_black)
        self.inbox.bind(size=self.inbox.setter('text_size'))
        ename_lay_2.add_widget(self.inbox)
        lcont.add_widget(ename_lay_2)

        ename_lay_3= RelativeLayout(size_hint=[0.85,0.12], pos_hint={"center_x": .5, "center_y": 0.45})
        self.vnesenie = Label_(pos_hint={"center_x": .5, "center_y": 0.5}, text=self.app.translation._("0"),halign='left',color=self.app.color_black)
        self.vnesenie.bind(size=self.vnesenie.setter('text_size'))
        ename_lay_3.add_widget(self.vnesenie)
        lcont.add_widget(ename_lay_3)

        ename_lay_4= RelativeLayout(size_hint=[0.85,0.12], pos_hint={"center_x": .5, "center_y": 0.25})
        self.vyplata = Label_(pos_hint={"center_x": .5, "center_y": 0.5}, text=self.app.translation._("0"),halign='left',color=self.app.color_black)
        self.vyplata.bind(size=self.vyplata.setter('text_size'))
        ename_lay_4.add_widget(self.vyplata)
        lcont.add_widget(ename_lay_4)

        self.add_widget(lcont)

    # -------------------------------- поле ввода ----------------------------
    def add_input(self):

        ldigit = RelativeLayout(size_hint = [0.58, 0.12], pos_hint = {'center_x': 0.695, 'center_y': .77})
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
        ldig = GridLayout(cols=3, rows=4, padding=5, spacing=3, size_hint =(.6, .6), pos_hint={"center_x": .692, "center_y": .41})

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

    def add_directbut(self):
        # --------------------------- управляющие кнопки ---------------------------

        # -------------------- X отчёт -----------------------------
        zrepbut= MDCard(orientation = 'horizontal', radius = [5,5], pos_hint = {"center_x": .86, 'center_y': .94}, size_hint = [0.25, 0.12], text_color = self.app.color_white, md_bg_color = self.app.bcolor1)
        zrepbut.on_press=lambda: self.button_click('Z-REP')
        zlabel = Label_(pos_hint={"center_x": .5, "center_y": .5},size_hint = [0.8, 0.4], text=self.app.translation._("Z-ОТЧЁТ"),halign='center',color=self.app.color_white)
        zlabel.bind(size=zlabel.setter('text_size'))
        #izrepbut = MDIconButton(color= self.app.color_white, icon = "backspace-outline", pos_hint = {"center_x": .5, "center_y": .5})
        zrepbut.add_widget(zlabel)
        self.add_widget(zrepbut)

        # -------------------- Z отчёт -----------------------------
        xrepbut= MDCard(orientation = 'horizontal', radius = [5,5], pos_hint = {"center_x": .53, 'center_y': .94}, size_hint = [0.25, 0.12], text_color = self.app.color_white, md_bg_color = self.app.bcolor1)
        xrepbut.on_press=lambda :self.button_click('X-REP')
        xlabel = Label_(pos_hint={"center_x": .5, "center_y": .5},size_hint = [0.8, 0.4], text=self.app.translation._("X-ОТЧЁТ"),halign='center',color=self.app.color_white)
        xlabel.bind(size=zlabel.setter('text_size'))
        #izrepbut = MDIconButton(color= self.app.color_white, icon = "backspace-outline", pos_hint = {"center_x": .5, "center_y": .5})
        xrepbut.add_widget(xlabel)
        self.add_widget(xrepbut)

        # -------------------- В ящике -----------------------------
        xrepbut= MDCard(orientation = 'horizontal', radius = [5,5], pos_hint = {"center_x": .162, 'center_y': .016}, size_hint = [0.25, 0.12], text_color = self.app.color_white, md_bg_color = self.app.bcolor1)
        xrepbut.on_press=lambda :self.button_click('INBOX')
        xlabel = Label_(pos_hint={"center_x": .5, "center_y": .5},size_hint = [0.8, 0.4], text=self.app.translation._("В ЯЩИКЕ"),halign='center',color=self.app.color_white)
        xlabel.bind(size=zlabel.setter('text_size'))
        #izrepbut = MDIconButton(color= self.app.color_white, icon = "backspace-outline", pos_hint = {"center_x": .5, "center_y": .5})
        xrepbut.add_widget(xlabel)
        self.add_widget(xrepbut)

        # -------------------- Внесение  -----------------------------
        xrepbut= MDCard(orientation = 'horizontal', radius = [5,5], pos_hint = {"center_x": .53, 'center_y': .016}, size_hint = [0.25, 0.12], text_color = self.app.color_white, md_bg_color = self.app.bcolor1)
        xrepbut.on_press=lambda :self.button_click('CASHIN')
        xlabel = Label_(pos_hint={"center_x": .5, "center_y": .5},size_hint = [0.8, 0.4], text=self.app.translation._("ВНЕСЕНИЕ"),halign='center',color=self.app.color_white)
        xlabel.bind(size=zlabel.setter('text_size'))
        #izrepbut = MDIconButton(color= self.app.color_white, icon = "backspace-outline", pos_hint = {"center_x": .5, "center_y": .5})
        xrepbut.add_widget(xlabel)
        self.add_widget(xrepbut)

        # -------------------- Выплата -----------------------------
        xrepbut= MDCard(orientation = 'horizontal', radius = [5,5], pos_hint = {"center_x": .86, 'center_y': .016}, size_hint = [0.25, 0.12], text_color = self.app.color_white, md_bg_color = self.app.bcolor1)
        xrepbut.on_press=lambda :self.button_click('CASHOUT')
        xlabel = Label_(pos_hint={"center_x": .5, "center_y": .5},size_hint = [0.8, 0.4], text=self.app.translation._("ВЫПЛАТА"),halign='center',color=self.app.color_white)
        xlabel.bind(size=zlabel.setter('text_size'))
        #izrepbut = MDIconButton(color= self.app.color_white, icon = "backspace-outline", pos_hint = {"center_x": .5, "center_y": .5})
        xrepbut.add_widget(xlabel)
        self.add_widget(xrepbut)

