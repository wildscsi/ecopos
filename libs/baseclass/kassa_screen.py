# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 CPV.BY
#
# For suggestions and questions:
# <7664330@gmail.com>
#
# LICENSE: Commercial
# kassa_screen.py
# интерфейс кассы

from kivymd.app import MDApp
import time
from kivy.uix.relativelayout import RelativeLayout
import platform

from libs.base.lbcontrol import Button_
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from libs.baseclass.buttonlib import TPButton, GPButton, TickButton, TPosDialog_, ExitPopup
from copy import deepcopy
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivy.uix.vkeyboard import VKeyboard
from libs.applibs.keyboard import ekeyboard
from kivymd.uix.dialog import MDDialog
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField, MDTextFieldRound, MDTextFieldRect
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from libs.base.lbfunc import mround
from kivymd.uix.screen import MDScreen
from libs.baseclass.buttonlib import _MDRaisedButton, Label_
from libs.baseclass.fr_widget import fr
from libs.baseclass.pe_widget import pe
import libs.applibs.equaction as equ
from kivy.utils import get_hex_from_color, get_color_from_hex


class Content(BoxLayout):
    pass

#class KassaScreen(Widget):
#    pass

#Factory.register('KassaScreen', KassaScreen)





class Content(BoxLayout):
    pass


# контейнер для кнопок с группами
class RelativeLayout_(RelativeLayout):
    cvalue = None




class KassaScreen(MDScreen):
    app = None
    listgruppa = []     # перечень отображаемых групп

    listtovar = []      # перечень отображаемых товаров
    obutton = {}        # объект клика
    treemenu = []       # дерево меню
    itree = 0           # местонахождение по дереву
    dialogdel = None    # диалог удаления позиций чека
    dialogfr = None     # модальное окно работы с ФР
    ikol = 0
    lpath = None        # объект контрола с путём блюд
    leftgroup = None    # група влево
    rightgroup = None   # група вправо
    homegroup = None    # Домой
    areturn = None      # кнопка возврата на экран с блюдами
    llegend = None      # легенда, название экрана
    search = None       # кнопка поиска
    esearch = None      # контрол поиска
    dialogsearch = None # объект диалога поиска
    dialogsave = None   # диалога с сохранением
    dialogload = None   # диалог с восстановлением
    dialogerror = None  # диалог с ошибкой
    kbd = None          # объект клавиатуры
    active_panel = None # активная левая панель

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.loadgrid()


    # выборка данных для групп и товаров
    def loadgrid(self, **kwargs):
        # очищаем грид. очистка канваса, тени остаются
        self.ids['box_gruppa'].children = []
        self.ids['box_gruppa'].canvas.children = []
        self.listgruppa = []; self.listtovar = []
        self.obutton = {}

        if kwargs.get('obutton'):
            # клик с кнопки, ищем группы, и блюда
            self.obutton = kwargs.get('obutton')

            # находим группы (подменю)
            if not self.app.osql.select('gruppa','lf=1 and idnt="'+self.obutton['code']+'"'): return False
            listgruppa = self.app.osql.getresult()
            self.listgruppa=sorted(listgruppa,key= lambda d: d['gname'])

            # находим перечень блюд
            if not self.app.osql.select('tovar','lf=1 and code="'+self.obutton['code']+'"'): return False
            listtovar = self.app.osql.getresult()
            self.listtovar= sorted(listtovar,key= lambda d: d['tname'])

        else:
            # первый вызов, запрашиваем все группы
            if not self.app.osql.select('gruppa','lf=1 and idnt=""'): return False
            self.listgruppa = self.app.osql.getresult()

            if len(self.treemenu) == 0:
                self.treemenu=[]
                self.treemenu.append({'gname':''})

        # размеры и свойства контейнера
        self.setgrid(self.ids.box_gruppa)

        # формируем экран c группами
        if len(self.listgruppa)>0: self.create_gruppa(self.ids.box_gruppa)

        # выбираем первую группу и отображаем по ней блюда
        if len(self.listtovar)>0: self.loadtovar(self.ids.box_gruppa)

        # строка с навигацией
        self.navreload()

    # размеры и свойства контейнера
    def setgrid(self, box_gruppa):
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
            main_cont = RelativeLayout_(size_hint_y= None, size=[200, box_gruppa.parent.size[1]])
            main_cont.id='irow_'+str(irow)
            box_gruppa.add_widget(main_cont)
            ib=0.125
            for item_but in range(ibutton,ibutton+4):
                if item_but+1> len(self.listtovar): continue

                obutton = self.listtovar[item_but]
                # отображение товаров
                but_tovar = TPButton(obutton = self.listtovar[item_but], bcolor=self.app.color_white, tcolor=self.app.color_black, pcolor=self.app.color_red, ecolor=self.app.color_green, oself=self)
                but_tovar.cid ='tovar'
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
            main_cont = RelativeLayout_(size_hint_y= None, size=[200, box_gruppa.parent.size[1]])
            main_cont.id='irow_'+str(irow)
            box_gruppa.add_widget(main_cont)

            # добавляем кнопки с группами
            ib=0.125
            for item_but in range(ibutton,ibutton+4):
                if item_but+1> len(self.listgruppa): continue
                ogruppa = self.listgruppa[item_but]
                # отображение групп
                but_gruppa = GPButton(obutton = self.listgruppa[item_but], bcolor=self.app.color_lblue, tcolor=self.app.color_black, oself=self)
                but_gruppa.cid = 'gruppa'
                but_gruppa.pos_hint={"center_x": ib, "center_y": 0.5}
                but_gruppa.size_hint=[0.24,1]
                main_cont.add_widget(but_gruppa)
                ib+=0.25
            ibutton += 4


    # нажатие на кнопки панели
    def buttonclick(self, obutton):

        # возврат к меню
        if obutton.cid == 'areturn':
            self.active_panel = None
            self.on_pre_leave()     # удаление лишних виджетов с экрана
            aa=11
            # перегрузка грида

            if self.itree < 0: self.itree = 0
            if self.itree == 0: self.loadgrid()
            else: self.loadgrid(obutton=self.treemenu[self.itree])


        # дважды не вызываем
        elif self.active_panel:
            if obutton.cid == self.active_panel.cid: return

        elif obutton.cid == 'tovar':
            self.app.aticket.append(deepcopy(obutton.obutton))
            self.treload()
            self.updatepath()

        elif obutton.cid == 'gruppa':
            if len(self.treemenu)-1>self.itree:
                treecopy = deepcopy(self.treemenu)
                self.treemenu = []
                for item in range(0,self.itree+1):
                    self.treemenu.append(treecopy[item])
            self.treemenu.append(obutton.obutton)
            self.itree += 1
            self.loadgrid(obutton=obutton.obutton)
            self.updatepath()

        elif obutton.cid == 'leftgroup':
            self.itree -= 1
            if self.itree < 0: self.itree = 0
            if self.itree == 0: self.loadgrid()
            else: self.loadgrid(obutton=self.treemenu[self.itree])
            self.updatepath()

        elif obutton.cid == 'homegroup':
            self.itree = 0
            self.loadgrid()
            self.updatepath()

        elif obutton.cid == 'rightgroup':
            if len(self.treemenu)==0: return
            if len(self.treemenu)>self.itree+1:
                self.itree += 1
                self.loadgrid(obutton=self.treemenu[self.itree])
            self.updatepath()

        # изменение кол-ва и удаление позиции
        elif obutton.cid == 'ticpos':
            self.edit_position(obutton=obutton.obutton)
            #return self.show_modal_pos(obutton=obutton.obutton)

        # форма удаления чека
        elif obutton.cid == 'ticketdel':
            return self.delete_dialog()

        # фильтр по блюдам, вызвов контрола с запросом наименования
        elif obutton.cid == 'search':
            self.esearch = TextInput(text='', hint_text=self.app.translation._('Поиск товаров'),pos_hint = {"center_x": .79, "center_y": .6}, size_hint=(0.3,0.9))
            self.ids['cntnavy'].add_widget(self.esearch)
            # добавляем клавиатуру в WIN и Linux
            if platform.system() in ["Windows","Linux"]:
                if self.kbd == None:
                    self.kbd = ekeyboard()
                    self.kbd.bind(on_key_up = self._on_keyboard_up_search)
                    self.kbd.text = ''
                    self.kbd.lclose = False
                    self.add_widget(self.kbd)



        # работа с фискальником
        elif obutton.cid == 'action_fr':
            # очистка формы слева и навигации

            self.ids['box_gruppa'].clear_widgets()
            self.ids['cntnavy'].clear_widgets()
            self.lpath      = None
            self.leftgroup  = None
            self.rightgroup = None
            self.homegroup  = None
            self.search     = None

            # добавляем кнопку навигации
            # контейнер навигации
            nbox = self.ids['cntnavy']

            # стрелка возврата
            if self.areturn == None:
                self.areturn =  MDIconButton(icon = "arrow-left-thick", pos_hint = {"center_x": .04, "center_y": .65})
                self.areturn.cid = 'areturn'
                self.areturn.on_press=lambda :self.buttonclick(self.areturn)
                nbox.add_widget(self.areturn)

            # Название где находимся
            if self.llegend == None:
                self.llegend =  Label_(text=self.app.translation._('ФР. ОТЧЁТЫ ПО СМЕНЕ'), halign='left', color = self.app.color_white , size_hint=[0.65, 0.6], pos_hint = {"center_x": .33, 'center_y': .65}, bold = True)
                self.llegend.id = 'llegend'
                self.llegend.bind(pos=self.llegend.on_texture_size, size=self.llegend.on_texture_size)
                nbox.add_widget(self.llegend)

            # Создаём контейнер для экрана c настройками фискальника
            self.active_panel = fr()
            self.ids['cntgruppa'].add_widget(self.active_panel)

        # чек возврата
        elif obutton.cid == 'action_refund':
            print('action_refund')
            if len(self.app.aticket) == 0: return
            type = 'return'
            row = []
            gmt = 10800
            for item in self.app.aticket:
                row.append({'tname': item['tname'],'price':item['cr'],'q':item['q'],'suma':item['sr'],'sdsa':item['dsc1']})


            js = {'class':'equ','model':'cashreg','cmd':'equprintcheck','data':{
                        'cashier':'Вася Иванов','type':type,'sdsp':0,'client':'Сергей Иванович','gmt':gmt,'row': row,
                        'pay':[self.app.ocalc.sall,0]
                        }
                  }

            # колонтитулы
            #js['data']['pay'] = [10.57,10]
            js['headers'] = [self.app.firm,self.app.addressfirm]
            js['footers'] = self.app.oeq.footer
            js['device'] = self.app.oeq.ofr
            result = equ.action(js)
            self.dialogerror = None
            if not result[4]:
                self.dialogerror = MDDialog(
                    title=self.app.translation._("Ошибка") + ": " + result[2]['message'],
                    md_bg_color=self.app.color_red,
                    buttons=[MDFlatButton(text=self.app.translation._('ЗАКРЫТЬ'),font_style="Button",on_release=self.dialogerror_close),
                        ],)
                self.dialogerror.open()
            else:
                # очистка данных чека
                self.app.aticket = []
                self.treload()
        elif obutton.cid == 'ticketpay':
            print('ticketpay')
            if len(self.app.aticket) == 0: return

            # строки чека
            # pay - массив оплат 5шт.
            # продажа sale (return)
            type = 'sale'
            row = []
            gmt = 10800
            for item in self.app.aticket:
                row.append({'tname': item['tname'],'price':item['cr'],'q':item['q'],'suma':item['sr'],'sdsa':item['dsc1']})


            js = {'class':'equ','model':'cashreg','cmd':'equprintcheck','data':{
                        'cashier':'Вася Иванов','type':type,'sdsp':0,'client':'Сергей Иванович','gmt':gmt,'row': row,
                        'pay':[self.app.ocalc.sall,0]
                        }
                  }

            # колонтитулы
            #js['data']['pay'] = [10.57,10]
            js['headers'] = [self.app.firm,self.app.addressfirm]
            js['footers'] = self.app.oeq.footer
            js['device'] = self.app.oeq.ofr


            # оборудование
            #cl = {'model':'comcheck','file':'ticket.txt','tapewidth':40,
            #            'upper':1,'tags':1,'codepage':'cp866','scode':[27,64,27,116,7],'ecode':[27,100,4,29,86,49],
            #            'config':{'port':'/dev/ttyUSB0','baud':19200,'bits':8,'parity':'N','stop':0,'soft':0,'hard':0}}


            # вызываем печать чека
            result = equ.action(js)

            self.dialogerror = None
            if not result[4]:
                self.dialogerror = MDDialog(
                    title=self.app.translation._("Ошибка") + ": " + result[2]['message'],
                    md_bg_color=self.app.color_red,
                    buttons=[MDFlatButton(text=self.app.translation._('ЗАКРЫТЬ'),font_style="Button",on_release=self.dialogerror_close),
                        ],)
                self.dialogerror.open()
            else:
                # очистка данных чека
                self.app.aticket = []
                self.treload()



        # сохранить набранный чек
        elif obutton.cid == 'action_save':
            if len(self.app.aticket) == 0:
                ctitle = self.app.translation._('Нет данных для сохранения. Чек пустой!')
            else:
                self.app.aticket_save = deepcopy(self.app.aticket)
                ctitle = self.app.translation._('ЧЕК СОХРАНЁН !')
            self.dialogsave = MDDialog(
                title=ctitle,
                type="confirmation",
                md_bg_color=self.app.bcolor3,
                buttons=[MDFlatButton(text=self.app.translation._('OK'),font_style="Button",on_release=self.dialogsave_close)]
                )
            self.dialogsave.open()


        # востановить набранный чек
        elif obutton.cid == 'action_load':
            if len(self.app.aticket_save) == 0: return

            if not self.dialogload:
                self.dialogload = MDDialog(
                    title=self.app.translation._('ВОССТАНОВИТЬ СОХРАНЁННЫЙ ЧЕК ?'),
                    type="confirmation",
                    md_bg_color=self.app.bcolor3,
                    buttons=[
                        MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogload_close),
                        _MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.dialogload_load ),
                    ],
                )
            self.dialogload.open()



        else:
            print('not understand')

    # закрытие окна с ошибкой кассы
    def dialogerror_close(self, *args):
        self.dialogerror.dismiss(force=True)

    # обновляем путь по группам
    def updatepath(self):
        # обновляем путь по группам
        self.lpath.text = ''; i = 0
        for item in self.treemenu:
            if i> self.itree : break
            cr = ''
            if len(self.lpath.text) > 0: cr = '/'
            self.lpath.text = self.lpath.text + cr + item['gname']
            i+=1

    # перерисовка контейнера с навигацией
    def navreload(self):

        # контейнер навигации
        nbox = self.ids['cntnavy']

        # очистка
        #for item in nbox.children:
        #    nbox.remove_widget(item)
        #nbox.children = []

        # кнопка влево
        if self.leftgroup == None:
            self.leftgroup =  MDIconButton(icon = "arrow-left-bold-circle", pos_hint = {"center_x": .04, "center_y": .65})
            self.leftgroup.cid = 'leftgroup'
            self.leftgroup.on_press=lambda :self.buttonclick(self.leftgroup)
            nbox.add_widget(self.leftgroup)

        # кнопка вправо
        if self.rightgroup == None:
            self.rightgroup =  MDIconButton(icon = "arrow-right-bold-circle", pos_hint = {"center_x": .20, 'center_y': .65})
            self.rightgroup.cid = 'rightgroup'
            self.rightgroup.on_press=lambda :self.buttonclick(self.rightgroup)
            nbox.add_widget(self.rightgroup)

        # кнопка навигации домой
        if self.homegroup == None:
            self.homegroup =  MDIconButton(icon = "home-circle", pos_hint = {"center_x": .12, 'center_y': .65})
            self.homegroup.cid = 'homegroup'
            self.homegroup.on_press=lambda :self.buttonclick(self.homegroup)
            nbox.add_widget(self.homegroup)

        # кнопка поиска
        if self.search == None:
            self.search =  MDIconButton(icon = "magnify", pos_hint = {"center_x": .97, 'center_y': .65})
            self.search.cid = 'search'
            self.search.on_press=lambda :self.buttonclick(self.search)
            nbox.add_widget(self.search)

        # путь (навигация) по группам
        if self.lpath == None:
            self.lpath =  Label_(text='', halign='left', color = self.app.color_white , size_hint=[0.65, 0.6], pos_hint = {"center_x": .63, 'center_y': .65}, bold = True)
            self.lpath.id = 'lpath'
            self.lpath.bind(pos=self.lpath.on_texture_size, size=self.lpath.on_texture_size)
            nbox.add_widget(self.lpath)

    # установка общей скидки на чек
    def chlalldsc(self,*args):
        if args[0].active:
            self.app.lalldsc = True
        else:
            self.app.lalldsc = False
        self.treload()


    # перерисовка чека
    def treload(self):
        # очистка строк чека
        self.ids['box_ticket'].children = []

        # общий контейнер
        box_ticket = self.ids['box_ticket']
        box_ticket.rows = len (self.app.aticket)

        # заполняем строки
        nn=0
        for item in self.app.aticket:
            # расчёты
            nn+=1
            try:
                item['sr'] = mround(item['price1']*item['q'],self.app.iround)
                item['cr'] = item['price1']
                item['nn'] = deepcopy(nn)
            except:
                item.update({'q':1.00, 'sr':item['price1'], 'cr':item['price1'],'nn':deepcopy(nn)})
            #контейнер строки
            main_cont = RelativeLayout_(size_hint_y= None, size=[200, box_ticket.parent.size[1]/6])
            main_cont.id='irow_'+str(item['itovar'])
            box_ticket.add_widget(main_cont)
            but_pos = TickButton(nn=str(nn),obutton = item, bcolor=self.app.color_white, tcolor=self.app.color_black, pcolor=self.app.color_red, ecolor=self.app.color_green, oself=self)
            main_cont.add_widget(but_pos)

        # перерасчёт сумм и данных по чеку
        self.app.ocalc.calc()
        self.ids['ekol'].text = str(self.app.ocalc.irow)                            # количество позиций
        self.ids['esall'].text = self.app.cval + ' ' + str(self.app.ocalc.sall)     # сумма к оплате
        self.ids['edsc2'].text = self.app.cval + ' ' + str(self.app.ocalc.ealldsc)  # сумма общего дисконта
        self.ids['ldscmain'].text = self.app.translation._('общий дисконт').upper() + '  ' + str(self.app.alldsc) + ' %'  # общий дисконт %


    # удаление чека
    def delete_dialog(self):
        if len(self.app.aticket) == 0: return
        if not self.dialogdel:
            self.dialogdel = MDDialog(
                title=self.app.translation._('УДАЛИТЬ ВСЕ ПОЗИЦИИ ЧЕКА ?'),
                type="confirmation",
                md_bg_color=self.app.bcolor3,
                buttons=[
                    MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogdel_close),
                    _MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.delete_all ),
                ],
            )
        self.dialogdel.open()

    # удаление всех позиция
    def delete_all(self, *args):
        self.app.aticket=[]
        self.treload()
        self.dialogdel.dismiss(force=True)

    # закрытие диалога удаление всех позиций
    def dialogdel_close(self, *args):
        self.dialogdel.dismiss(force=True)

    # закрытие диалога c сохранением чека
    def dialogsave_close(self, *args):
        self.dialogsave.dismiss(force=True)

    # закрытие диалога работы с ФР
    def dialogfr_close(self, *args):
        self.dialogfr.dismiss(force=True)

    # закрытие диалога загрузки чека
    def dialogload_close(self, *args):
        self.dialogload.dismiss(force=True)

    # загрузка сохранённого чека
    def dialogload_load(self, *args):
        self.app.aticket = deepcopy(self.app.aticket_save)
        self.app.aticket_save = []
        self.dialogload.dismiss(force=True)
        self.treload()

    # редактирование позиции чека
    def ticketpos_edit(self, obutton):
        popupWindow = TPosDialog_(obutton=obutton)
        # open popup window
        popupWindow.open()

    # форма редактирования количества и удаление
    def edit_position(self, obutton):
           # очистка формы слева и навигации
            self.ids['box_gruppa'].clear_widgets()
            self.ids['cntnavy'].clear_widgets()
            self.lpath      = None
            self.leftgroup  = None
            self.rightgroup = None
            self.homegroup  = None
            self.search     = None

            # добавляем кнопку навигации
            # контейнер навигации
            nbox = self.ids['cntnavy']

            # стрелка возврата
            if self.areturn == None:
                self.areturn =  MDIconButton(icon = "arrow-left-thick", pos_hint = {"center_x": .04, "center_y": .65})
                self.areturn.cid = 'areturn'
                self.areturn.on_press=lambda :self.buttonclick(self.areturn)
                nbox.add_widget(self.areturn)

            # Название где находимся
            if self.llegend == None:
                self.llegend =  Label_(text=self.app.translation._('ИЗМЕНЕНИЕ ПОЗИЦИИ'), halign='left', color = self.app.color_white , size_hint=[0.65, 0.6], pos_hint = {"center_x": .33, 'center_y': .65}, bold = True)
                self.llegend.id = 'llegend'
                self.llegend.bind(pos=self.llegend.on_texture_size, size=self.llegend.on_texture_size)
                nbox.add_widget(self.llegend)

            # Создаём контейнер для экрана c редактированием позиции
            self.active_panel = pe(oform=self, obutton= obutton)
            self.ids['cntgruppa'].add_widget(self.active_panel)



    # переход на другой экран
    def on_pre_leave(self):

        # Очистка экрана от лишних виджетов
        try:
            self.ids['box_gruppa'].clear_widgets()
            self.ids['cntnavy'].clear_widgets()
            self.leftgroup = None
            self.rightgroup = None
            self.homegroup = None
            self.search = None
            self.lpath = None
            # удаляем экран

            #aa = self.ids['cntgruppa'].children[0]
            for item in self.ids['cntgruppa'].children:
                if item.cid in ['cntfr','cntpe']: self.ids['cntgruppa'].remove_widget(item)

            self.areturn = None
            self.llegend = None
            self.active_panel = None

        except:
            pass

    # обработка нажатий кнопок поиска
    def _on_keyboard_up_search(self, keyboard, keycode, text, modifiers):
        self.kbd.updkeykode(keyboard, keycode, text, modifiers)
        if self.kbd.lclose:
            if len(self.esearch.text) > len(self.kbd.text):
                result = self.esearch.text
            else:
                result = deepcopy(self.kbd.text)
            self.ids['cntnavy'].remove_widget(self.esearch)
            self.esearch = None
            self.remove_widget(self.kbd)
            self.kbd = None
            self.search_tovar(result)
        else:
            self.esearch.text = self.kbd.text

    # форма поиска и отбора блюд
    def search_tovar(self, evalue):
        self.listgruppa = []; self.listtovar = []
        self.ids['box_gruppa'].children = []
        self.ids['box_gruppa'].canvas.children = []
        # выбираем все блюда
        if not self.app.osql.select('tovar','lf=1'): return False
        listtovar_temp = self.app.osql.getresult()
        if len(evalue) == 0: return
        listtovar = []
        for item in listtovar_temp:
            if evalue.upper() in (item['tname']).upper():
                listtovar.append(item)
        self.listtovar= sorted(listtovar,key= lambda d: d['tname'])
        self.lpath.text = self.app.translation._('Поиск') + ': ' + evalue
        self.loadtovar(self.ids['box_gruppa'])
