# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 CPV.BY
#
# For suggestions and questions:
# <7664330@gmail.com>
#
# LICENSE: Commercial
# kassa.py
# интерфейс кассы

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from libs.base.lbcontrol import Button_
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from libs.uix.baseclass.buttonlib import TPButton, GPButton, TickButton, TPosDialog_, ExitPopup
from copy import deepcopy
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDFlatButton

#from kivymd.uix.dialog import MDDialog
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivy.uix.modalview import ModalView
from kivymd.uix.bottomsheet import (
    MDCustomBottomSheet,
    MDGridBottomSheet,
    MDListBottomSheet,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from libs.base.lbfunc import mround

class Content(BoxLayout):
    pass

class KassaScreen(Widget):
    pass

Factory.register('KassaScreen', KassaScreen)


# контейнер для кнопок с группами
class RelativeLayout_(RelativeLayout):
    cvalue = None


class Kassa(Screen):
    oApp = None
    listgruppa = []     # перечень отображаемых групп
    listtovar = []      # перечень отображаемых товаров
    obutton = {}        # объект клика
    treemenu = []       # дерево меню
    itree = 0           # местонахождение по дереву
    dialog = None
    ikol = 0
    def on_pre_enter(self, *args):
        self.oApp = self.manager.oapp
        self.loadgrid()

    # выборка данных для групп и товаров
    def loadgrid(self, **kwargs):
        # очищаем грид. очистка канваса, тени остаются
        aa = 4
        self.ids['box_gruppa'].children = []
        self.ids['box_gruppa'].canvas.children = []
        self.listgruppa = []; self.listtovar = []
        self.obutton = {}

        if kwargs.get('obutton'):
            # клик с кнопки, ищем группы, и блюда
            self.obutton = kwargs.get('obutton')

            # находим группы (подменю)
            if not self.oApp.osql.select('gruppa','idnt="'+self.obutton['code']+'"'): return False
            listgruppa = self.oApp.osql.getresult()
            self.listgruppa=sorted(listgruppa,key= lambda d: d['gname'])

            # находим перечень блюд
            if not self.oApp.osql.select('tovar','code="'+self.obutton['code']+'"'): return False
            listtovar = self.oApp.osql.getresult()
            self.listtovar= sorted(listtovar,key= lambda d: d['tname'])

        else:
            # первый вызов, запрашиваем все группы
            self.oApp = self.manager.parent.oApp
            if not self.oApp.osql.select('gruppa','lf=1 and idnt=""'): return False
            self.listgruppa = self.oApp.osql.getresult()

            if len(self.treemenu) == 0:
                self.treemenu=[]
                self.treemenu.append({'gname':''})

        # размеры и свойства контейнера
        aa = 576
        self.setgrid(self.ids.box_gruppa)

        # формируем экран c группами
        if len(self.listgruppa)>0: self.create_gruppa(self.ids.box_gruppa)

        # выбираем первую группу и отображаем по ней блюда
        if len(self.listtovar)>0: self.loadtovar(self.ids.box_gruppa)

    # размеры и свойства контейнера
    def setgrid(self, box_gruppa):
        aa = 567
        # высота контейнера
        # количество строчек с кнопками групп
        self.ids['box_gruppa'].rows = 0

        # рассчитываем высоту контейнера с группами (три строчки)
        def update_size(instance, value):
            for item in instance.children:
                item.size = box_gruppa.parent.size[0],(box_gruppa.parent.size[1]/6)*0.9
        box_gruppa.bind(pos=update_size, size=update_size)

    # заполняем товары  ---------------------------
    def loadtovar(self, box_gruppa):
        # количество строчек с кнопками групп
        irow = abs(len(self.listtovar)/4)
        if len(self.listtovar)/4 > irow: irow += 1
        if len(self.listtovar)/4<1: irow=1
        self.ids['box_gruppa'].rows += int(irow)
        # добавляем кнопки с товарами
        ibutton = 0     # Кнопка, с которой начинается контейнер
        for gitem in range(int(irow)):
            # основной контейнер c товарами
            main_cont = RelativeLayout_(id='irow_'+str(irow),size_hint_y= None, size=[200, box_gruppa.parent.size[1]])
            box_gruppa.add_widget(main_cont)
            ib=0.125
            for item_but in range(ibutton,ibutton+4):
                if item_but+1> len(self.listtovar): continue

                obutton = self.listtovar[item_but]
                # отображение товаров
                but_tovar = TPButton(cid ='tovar', obutton = self.listtovar[item_but], bcolor=self.oApp.color_white, tcolor=self.oApp.color_black, pcolor=self.oApp.color_red, ecolor=self.oApp.color_green, oself=self)
                #but_tovar.id = 'but_'+str(obutton['itovar'])
                but_tovar.pos_hint={"center_x": ib, "center_y": 0.5}
                but_tovar.size_hint=[0.24,1]
                main_cont.add_widget(but_tovar)
                ib+=0.25
            ibutton += 4

    # заполняем группы  ---------------------------
    def create_gruppa(self, box_gruppa):
        # легенда с группами
        # количество строчек с кнопками групп
        irow = int(len(self.listgruppa)/4)
        if len(self.listgruppa)/4 > irow: irow += 1
        self.ids['box_gruppa'].rows += int(irow)
        if irow == 0: irow = 1
        ibutton = 0     # Кнопка, с которой начинается контейнер
        for gitem in range(int(irow)):

            # основной контейнер c группами
            main_cont = RelativeLayout_(id='irow_'+str(irow),size_hint_y= None, size=[200, box_gruppa.parent.size[1]])
            box_gruppa.add_widget(main_cont)

            # добавляем кнопки с группами
            ib=0.125
            for item_but in range(ibutton,ibutton+4):
                if item_but+1> len(self.listgruppa): continue
                ogruppa = self.listgruppa[item_but]
                # отображение групп
                but_gruppa = GPButton(cid = 'gruppa', obutton = self.listgruppa[item_but], bcolor=self.oApp.color_lblue, tcolor=self.oApp.color_black, oself=self)
                but_gruppa.pos_hint={"center_x": ib, "center_y": 0.5}
                but_gruppa.size_hint=[0.24,1]
                main_cont.add_widget(but_gruppa)
                ib+=0.25
            ibutton += 4

    # нажатие на кнопки панели
    def buttonclick(self, obutton):
        aa = 12121
        if obutton.cid == 'tovar':
            self.oApp.aticket.append(deepcopy(obutton.obutton))
            self.treload()

        elif obutton.cid == 'gruppa':
            if len(self.treemenu)-1>self.itree:
                treecopy = deepcopy(self.treemenu)
                self.treemenu = []
                for item in range(0,self.itree+1):
                    self.treemenu.append(treecopy[item])
            self.treemenu.append(obutton.obutton)
            self.itree += 1
            self.loadgrid(obutton=obutton.obutton)
        elif obutton.cid == 'leftgroup':
            self.itree -= 1
            if self.itree < 0: self.itree = 0
            if self.itree == 0: self.loadgrid()
            else: self.loadgrid(obutton=self.treemenu[self.itree])
        elif obutton.cid == 'homegroup':
            self.itree = 0
            self.loadgrid()
        elif obutton.cid == 'rightgroup':
            if len(self.treemenu)==0: return
            if len(self.treemenu)>self.itree+1:
                self.itree += 1
                self.loadgrid(obutton=self.treemenu[self.itree])
        # изменение кол-ва и удаление позиции
        elif obutton.cid == 'ticpos':
            return self.show_modal_pos(obutton=obutton.obutton)


        elif obutton.cid == 'ticketdel':
            aa = 576
            return self.show_alert_dialog()


            #self.show_alert_dialog()
            self.oApp.aticket=[]
            self.treload()
            self.show_alert_dialog()

        elif obutton.cid == 'action_search':
            print('serch')


        else:
            print('hello')

        self.ids['lpath'].text = ''; i = 0
        for item in self.treemenu:
            if i> self.itree : break
            self.ids['lpath'].text = self.ids['lpath'].text + item['gname'] + ' / '
            i+=1
    # перерисовка чека
    def treload(self):
        # очистка строк чека
        self.ids['box_ticket'].children = []

        # общий контейнер
        box_ticket = self.ids['box_ticket']
        box_ticket.rows = len (self.oApp.aticket)

        # заполняем строки
        nn=0
        for item in self.oApp.aticket:
            # расчёты
            nn+=1
            try:
                item['sr'] = mround(item['price1']*item['q'],self.oApp.iround)
                item['cr'] = item['price1']
                item['nn'] = deepcopy(nn)
            except:
                item.update({'q':1.00, 'sr':item['price1'], 'cr':item['price1'],'nn':deepcopy(nn)})
            #контейнер строки
            main_cont = RelativeLayout_(id='irow_'+str(item['itovar']),size_hint_y= None, size=[200, box_ticket.parent.size[1]/6])
            box_ticket.add_widget(main_cont)
            but_pos = TickButton(nn=str(nn),obutton = item, bcolor=self.oApp.color_white, tcolor=self.oApp.color_black, pcolor=self.oApp.color_red, ecolor=self.oApp.color_green, oself=self)
            main_cont.add_widget(but_pos)

        aa = 432434
        # перерасчёт сумм и данных по чеку
        self.oApp.ocalc.calc()
        self.ids['ekol'].text = str(self.oApp.ocalc.irow)
        self.ids['esall'].text = self.oApp.cval + ' ' + str(self.oApp.ocalc.sall)

    # удаление чека
    def show_alert_dialog(self):
        popupWindow = MDDialog(
            title='',
            #text =self.oApp.translation._('Удалить чек?'),
            text ='Hello',
            size_hint_x = 0.8,
            size_hint_y = 0.8,
            text_button_cancel = StringProperty("ca")
            #size_hint =(0.4, 0.3),

        )


        # open popup window
        popupWindow.open()

    # редактирование позиции чека
    def ticketpos_edit(self, obutton):
        aa = 343
        popupWindow = TPosDialog_(obutton=obutton)
        # open popup window
        popupWindow.open()

    # редактирование количества и удаление
    def show_modal_pos(self, obutton):

        # ссылку на количество
        # удаление
        dd = 67
        mview =TPosDialog_(ctext=str(obutton['q']),oform=self, obutton=obutton)
        mview.open()
        aa = 576
        return
        mview = ModalView(id='mviewid', ctesize_hint=(0.4, 0.3), auto_dismiss=True, background='./images/noimage.png')
        mblt = BoxLayout(orientation='vertical', padding=(24))
        minp = TextInput(id='inptxt', text='', hint_text='Start typing text with markup here', size_hint=(1,0.5),multiline=True)
        #minp.bind(text=self.on_inptext)

        mtxt = Label(id='txtresult',text='displays formatted text', color=(0.3,0.3,0.3), size_hint=(1,0.5),markup=True)
        mcnf = Button(text='OK', size=(144,48), size_hint=(None,None))
        mcnf.bind(on_press=mview.dismiss)

        mblt.add_widget(minp)
        mblt.add_widget(mtxt)
        mblt.add_widget(mcnf)
        mview.add_widget(mblt)
        #mview.bind(on_dismiss=self.print_text)
        # binding between TextInput text and Label text
        minp.bind(text=lambda instance, value: setattr(mtxt, 'text',value))

        mview.open()

    # удаление блюда, вызывается из модального окна
    def delete_pos(self,obutton):
        aa = 567
        newticket = deepcopy(self.oApp.aticket)
        self.oApp.aticket = []
        for item in newticket:
            if item['nn'] != obutton['nn']:
                self.oApp.aticket.append(item)
        self.treload()

    # изменение кол-ва, вызывается из модального окна
    def ch_pos(self, obutton, ikol):
        for item in self.oApp.aticket:
            aa = 12
            if item['nn'] == obutton['nn']:
                item.update({'q':ikol})
                break
        self.treload()
