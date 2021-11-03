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
from kivymd.uix.button import MDRectangleFlatIconButton, MDRaisedButton, MDRectangleFlatButton, MDFlatButton,  MDTextButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.banner import MDBanner
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
import json
from kivy.clock import Clock
from datetime import datetime

color_green = get_color_from_hex('85ba6f')
color_blue = get_color_from_hex('2196f3')
color_white = get_color_from_hex('ffffff')
color_red = get_color_from_hex('ff0000')
color_dgreen = get_color_from_hex('288023')

gcolor =    get_color_from_hex('007d00')   # цвет ед.изм (зеленый)
bcolor =    get_color_from_hex('000000')   # цвет названия (зеленый)
blcolor =   get_color_from_hex('2196f3')   # цвет ПП (синий)
grcolor =   get_color_from_hex('939393')   # цвет серый
wcolor =    get_color_from_hex('ffffff')    # цвет белый
bcolor3 =   get_color_from_hex('3f6f9c')


class Content(BoxLayout):
    pass


# кнопка с иконкой
class IconTextButton_(MDRectangleFlatIconButton):
    cid = 'iconboot'
    pass

# кнопка с фоном
class _MDRaisedButton(MDRaisedButton):
    text_color = get_color_from_hex('ffffff')
    md_bg_color = get_color_from_hex('85ba6f')



# класс MODAL диалог ввода кол-ва или удалени позиции

class TPosDialog_(ModalView):
    cid = 'id'
    text='Error Name Item'  # основной текст на кнопке
    atext = []              # массив строк
    obutton = []            # объект товар
    inp = None              # поле ввода
    ctext=''
    app = None

    # инит
    def __init__(self, **kwargs):
        if kwargs.get('obutton'): self.obutton = kwargs.pop('obutton')
        if kwargs.get('ctext'): self.ctext = kwargs.pop('ctext')
        if kwargs.get('oform'): self.oform = kwargs.pop('oform')
        self.app = MDApp.get_running_app()
        self.setvalue()
        super(TPosDialog_, self).__init__()
        self.addbut()

    # установки контрола
    def setvalue(self):
        self.size_hint =(0.6, 0.7)
        self.auto_dismiss=True
        #self.background='./images/noimage.png'
        self.background = './data/images/back.png'
        #self.add_widget(self.buttons)

    # добавление контролов на модальное окно редактирования позиции
    def addbut(self):


        # основной контейнер
        superBox = BoxLayout(orientation ='vertical')

        # заголовок
        HBC = BoxLayout(orientation='vertical', size_hint_y=0.2)
        caption = Label_(text = self.app.translation._('Внесение количества, удаление позиции'), color= self.app.bcolor3, size_hint=[0.92, 0.2],pos_hint= {'center_x': 0.5, 'center_y': .9})
        caption.bind(pos=caption.on_texture_size, size=caption.on_texture_size)
        HBC.add_widget(caption)
        superBox.add_widget(HBC)

        # , OK
        HBD = BoxLayout(orientation='horizontal', size_hint_y=0.3)
        # поле ввода  значение кол-ва
        self.inp = Label_(text=self.ctext, color=self.app.color_red, size_hint =[0.8, 0.8],pos_hint= {'center_x': 0.5, 'center_y': .5})
        id='q'
        self.inp.bind(pos=self.inp.on_texture_size, size=self.inp.on_texture_size)

        # + и -
        PLMIN = BoxLayout(spacing=15)
        bmin= MDRaisedButton(text='-', pos_hint= {'center_x': 0.25, 'center_y': .5})
        bmin.md_bg_color = self.app.color_green
        bmin.text_color = self.app.color_igray
        bmin.on_press= lambda :self.dinput('-')
        bmax= MDRaisedButton(text='+', pos_hint= {'center_x': 0.75, 'center_y': .5})
        bmax.md_bg_color = self.app.color_green
        bmax.text_color = self.app.color_igray
        bmax.on_press= lambda :self.dinput('+')
        PLMIN.add_widget(bmin)
        PLMIN.add_widget(bmax)



        # кнопка OK
        cntOk = RelativeLayout()
        cmdOk= MDRaisedButton(text='OK', pos_hint= {'center_x': 0.5, 'center_y': .5})
        cmdOk.on_press=lambda :self.dinput('OK')
        cmdOk.color_text=self.app.color_white
        cmdOk.md_bg_color = self.app.color_hdarkblue
        cmdOk.text_color =  self.app.color_igray
        cntOk.add_widget(cmdOk)

        HBD.add_widget(self.inp)
        HBD.add_widget(PLMIN)
        HBD.add_widget(cntOk)



        # цифровая клава


        HBE = BoxLayout(orientation='horizontal')

        ldig = GridLayout(cols=3, rows=4, padding=5, spacing=2,size_hint =(1, 1))
        obut1= MDRaisedButton()
        obut1.text='1'
        obut1.on_press=lambda :self.dinput('1')
        ldig.add_widget(obut1)

        obut2= MDRaisedButton()
        obut2.text='2'
        obut2.on_press=lambda :self.dinput('2')
        ldig.add_widget(obut2)

        obut3= MDRaisedButton()
        obut3.text='3'
        obut3.on_press=lambda :self.dinput('3')
        ldig.add_widget(obut3)

        obut4= MDRaisedButton()
        obut4.text='4'
        obut4.on_press=lambda :self.dinput('4')
        ldig.add_widget(obut4)

        obut5= MDRaisedButton()
        obut5.text='5'
        obut5.on_press=lambda :self.dinput('5')
        ldig.add_widget(obut5)

        obut6= MDRaisedButton()
        obut6.text='6'
        obut6.on_press=lambda :self.dinput('6')
        ldig.add_widget(obut6)

        obut7= MDRaisedButton()
        obut7.text='7'
        obut7.on_press=lambda :self.dinput('7')
        ldig.add_widget(obut7)

        obut8= MDRaisedButton()
        obut8.text='8'
        obut8.on_press=lambda :self.dinput('8')
        ldig.add_widget(obut8)

        obut9= MDRaisedButton()
        obut9.text='9'
        obut9.on_press=lambda :self.dinput('9')
        ldig.add_widget(obut9)

        obutc= MDRaisedButton()
        obutc.text='C'
        obutc.md_bg_color= get_color_from_hex("ff0000")
        obutc.on_press=lambda :self.dinput('C')
        ldig.add_widget(obutc)

        obut0= MDRaisedButton()
        obut0.text='0'
        obut0.on_press=lambda :self.dinput('0')
        ldig.add_widget(obut0)

        obutt= MDRaisedButton()
        obutt.text='.'
        obutt.on_press=lambda :self.dinput('.')
        ldig.add_widget(obutt)

        HBE.add_widget(ldig)


        # кнопки удалить и отмена
        lbut = GridLayout(cols=1, rows=2, padding=5, spacing=25, size_hint =(0.5, .5), pos_hint= {'center_x': 0.5, 'center_y': 0.5})

        obutdel= MDRaisedButton()
        obutdel.text='DELETE'
        obutdel.on_press=lambda :self.dinput('D')
        #obutdel.padding = 20
        obutdel.text_color = color_red
        lbut.add_widget(obutdel)

        obutcancel= MDRaisedButton()
        obutcancel.text='CANCEL'
        obutcancel.on_press=lambda :self.dinput('CL')
        #obutcancel.padding = 30
        lbut.add_widget(obutcancel)
        HBE.add_widget(lbut)



        superBox.add_widget(HBD)
        superBox.add_widget(HBE)
        self.add_widget(superBox)
        return




        # контейнер слево: для кол-ва, цифровых кнопок, справа управляющие
        HB = BoxLayout(orientation ='horizontal')
        # левый
        HBL = BoxLayout(orientation ='horizontal',size_hint =(0.6, 1))

        # контейнер с названием и кнопками +-
        HBL0 = RelativeLayout(size_hint=[1, 0.3], pos_hint= {'center_x': 0.5, 'center_y': 0.5})

        #поле ввода
        self.inp = Label_(text=self.ctext, color=self.app.color_red, size_hint =[0.3, 1],pos_hint= {'center_x': 0.15, 'center_y': .5})
        id='q'
        self.inp.bind(pos=self.inp.on_texture_size, size=self.inp.on_texture_size)
        HBL0.add_widget(self.inp)



        # кнопки с цифрами
        HBL1 = BoxLayout(orientation ='vertical', size_hint=[1, 0.85], pos_hint= {'center_x': 0.5, 'center_y': .5})
        ldig = GridLayout(cols=3, rows=4, padding=45, spacing=2,size_hint =(0.5, 1))
        obut1= MDRaisedButton()
        obut1.text='1'
        obut1.on_press=lambda :self.dinput('1')
        ldig.add_widget(obut1)

        obut2= MDRaisedButton()
        obut2.text='2'
        obut2.on_press=lambda :self.dinput('2')
        ldig.add_widget(obut2)

        obut3= MDRaisedButton()
        obut3.text='3'
        obut3.on_press=lambda :self.dinput('3')
        ldig.add_widget(obut3)

        obut4= MDRaisedButton()
        obut4.text='4'
        obut4.on_press=lambda :self.dinput('4')
        ldig.add_widget(obut4)

        obut5= MDRaisedButton()
        obut5.text='5'
        obut5.on_press=lambda :self.dinput('5')
        ldig.add_widget(obut5)

        obut6= MDRaisedButton()
        obut6.text='6'
        obut6.on_press=lambda :self.dinput('6')
        ldig.add_widget(obut6)

        obut7= MDRaisedButton()
        obut7.text='7'
        obut7.on_press=lambda :self.dinput('7')
        ldig.add_widget(obut7)

        obut8= MDRaisedButton()
        obut8.text='8'
        obut8.on_press=lambda :self.dinput('8')
        ldig.add_widget(obut8)

        obut9= MDRaisedButton()
        obut9.text='9'
        obut9.on_press=lambda :self.dinput('9')
        ldig.add_widget(obut9)

        obutc= MDRaisedButton()
        obutc.text='C'
        obutc.md_bg_color= get_color_from_hex("ff0000")
        obutc.on_press=lambda :self.dinput('C')
        ldig.add_widget(obutc)

        obut0= MDRaisedButton()
        obut0.text='0'
        obut0.on_press=lambda :self.dinput('0')
        ldig.add_widget(obut0)

        obutt= MDRaisedButton()
        obutt.text='.'
        obutt.on_press=lambda :self.dinput('.')
        ldig.add_widget(obutt)

        HBL1.add_widget(ldig)
        HBL.add_widget(HBL1)
        HBL.add_widget(HBL0)

        #управляющие кнопки - удаление, отмена, OK
        HBR = BoxLayout(orientation ='vertical',size_hint =(0.3, 1), spacing = 20, padding=[20, 0, 0, 45])
        HB.add_widget(HBL)
        HB.add_widget(HBR)
          # -+
        HBR0 = BoxLayout(orientation ='horizontal',spacing=4, padding = [0,0,52,0])
        butminus = MDRectangleFlatIconButton()
        butminus.icon = "minus"
        butminus.on_press=lambda :self.dinput('-')
        butminus.size_hint= [0.1, 0.7]
        butminus.pos_hint= {'center_x': 0.2, 'center_y': .5}
        butminus.md_bg_color = color_blue
        butminus.text_color = color_white
        HBR0.add_widget(butminus)

        butplus = MDRectangleFlatIconButton()
        butplus.icon = "plus"
        butplus.on_press=lambda :self.dinput('+')
        butplus.size_hint= [0.1, 0.7]
        butplus.pos_hint= {'center_x': 0.6, 'center_y': .5}
        butplus.md_bg_color = color_blue
        butplus.text_color = color_white
        HBR0.add_widget(butplus)
        HBR.add_widget(HBR0)

        obutdel= MDRaisedButton()
        obutdel.text='DELETE'
        obutdel.on_press=lambda :self.dinput('D')
        obutdel.padding = 20
        obutdel.text_color = color_red
        HBR.add_widget(obutdel)

        obutcancel= MDRaisedButton()
        obutcancel.text='CANCEL'
        obutcancel.on_press=lambda :self.dinput('CL')
        obutcancel.padding = 30
        HBR.add_widget(obutcancel)

        obutok= MDRaisedButton()
        obutok.text='OK'
        obutok.md_bg_color=color_dgreen
        obutok.on_press=lambda :self.dinput('OK')
        obutok.padding = 40
        HBR.add_widget(obutok)

        superBox.add_widget(HB)
        self.add_widget(superBox)


    # ввод данных c контролов
    def dinput(self, ctext):
        # проверка
        if ctext == 'D':
            self.oform.delete_pos(self.obutton)
            self.dismiss()
            return
        if ctext == 'OK':
            try:
                q = float(self.inp.text)
            except:
                q = 1
            self.oform.ch_pos(self.obutton, q)
            self.dismiss()
            return
        if ctext == 'CL':
            self.dismiss()
            return
        if ctext == 'C':
            self.inp.text='0.0'
            return
        if len(self.inp.text)>8: return
        if ctext == '.':
            if self.inp.text.count('.')>0:return
        if ctext == '-':
            istr = float(self.inp.text) -1
            if istr<0:
                self.inp.text ='0.0'
                return
            self.inp.text = str(istr)
            return
        if ctext == '+':
            self.inp.text = str(float(self.inp.text) +1)
            return
        if self.inp.text == '0.0':
            self.inp.text = ctext
        elif ctext == '0.0.': self.inp.text += ctext
        else: self.inp.text += ctext

# класс кнопки с картинкой
class PButton_(MDRectangleFlatIconButton):
    ccolor = 'black'
    def __init__(self, **kwargs):
        super(PButton_, self).__init__(**kwargs)
        self.id = "leftgroup"
        opposite_colors = True
        theme_text_color = "Custom"
        text_color = [1, 0, 0, 1]
        self.icon = 'sd'
        #self.theme_text_color = "Custom"
        self.user_font_size = '20sp'
        #self.md_bg_color = get_color_from_hex('#00ff00')
        self.text_color = get_color_from_hex('ebebeb')




        #self.md_bg_color=get_color_from_hex('ffffff')
        #self.source = 'atlas://data/images/defaulttheme/checkbox_off'
        #self.source = 'atlas://Data/atlas/myatlas/info'
        #self.source = 'atlas://images/myatlas/logo200'
        #self.source = 'atlas://images/butatlas/dnup'

        # перерасчёт расзмеров шрифта
        #self.bind(pos=self.setting_function, size=self.setting_function)

    # размеры шрифта и выравнивание
    def setting_function(self, instance, value):
        aa = 123

        #instance.font_size = instance.height /2
            #instance.padding = [5, (instance.height - instance.line_height ) / 2]


# класс свойства настройки оборудования
class PMDCard(MDCard):
    dialog = None
    cid = 'id'
    pos_hint= {"center_x": .5, "center_y": .5}
    orientation     = 'horizontal'
    ripple_behavior = True
    size_hint       = (1, 20)
    ctext           = ''                        # название свойства
    cprim           = ''                        # описание свойства
    cvalue          = ''                        # значение свойства
    oform           = ''
    ecard1label3    = ''                        # контрол со значением свойства .text

    def __init__(self, ctext=None, cprim=None, cvalue=None, oform=None, **kwargs):
        self.app = MDApp.get_running_app()
        self.ctext   = ''
        self.cprim   = ''
        self.cvalue  = ''
        self.oform   = ''
        if oform: self.oform=oform
        if ctext:
            self.ctext  = ctext
            self.cid    = self.ctext
        if cprim: self.cprim = cprim
        if cvalue: self.cvalue = cvalue
        super(PMDCard, self).__init__(**kwargs)
        self.addcontrol()

    # добавляем контролы
    def addcontrol(self):
        # описание
        ecard1cnt1 = RelativeLayout(pos_hint= {'center_x': 0.35, 'center_y': 0.5},size_hint = [0.4, 1] )
        #ecard1cnt1.on_press=lambda :self.open_properties('ecard_'+str(i))
        ecard1cnt3 = MDBoxLayout(adaptive_height=True, padding= ["2dp", "2dp", "2dp", "2dp"],orientation= "vertical")
        ecard1label1 = MDLabel(text=self.ctext,font_style='Caption', adaptive_height=True, theme_text_color= "Secondary", pos_hint= {"center_y": .5})
        ecard1label2 = MDLabel(text=self.cprim,font_style='Caption', adaptive_height=True, theme_text_color= "Secondary", pos_hint= {"center_y": .5})
        ecard1separator = MDSeparator(height= "1dp")
        ecard1cnt3.add_widget(ecard1label1); ecard1cnt3.add_widget(ecard1separator); ecard1cnt3.add_widget(ecard1label2)
        ecard1cnt1.add_widget(ecard1cnt3)
        self.add_widget(ecard1cnt1)

        # значение
        ecard1cnt2 = MDRelativeLayout(pos_hint= {'center_x': 0.92, 'center_y': 0.5},size_hint = [0.6, 1] )
        self.ecard1label3 = MDLabel(text=self.cvalue,font_style='H2', adaptive_height=True, theme_text_color= "Secondary", pos_hint= {"center_y": .5}, halign='center')
        ecard1cnt2.add_widget(self.ecard1label3)
        self.add_widget(ecard1cnt2)

        # действие
        self.on_press = lambda *args: self.action()

    # действие - Pop-UP
    def action(self):
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                md_bg_color=self.app.bcolor3,
                title= self.cprim,
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialog_close),
                    _MDRaisedButton(text=self.app.translation._('ИЗМЕНИТЬ'),font_style="Button", on_release=self.dialog_edit),
                ],
            )
        self.dialog.content_cls.ids['esearch'].text = self.cvalue
        self.dialog.open()

    # закрываем диалог
    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)


    # изменение данных, перерасчёт основной формы и закрываем диалог
    def dialog_edit(self, *args):
        self.cvalue = self.dialog.content_cls.ids['esearch'].text
        self.app.config.set('KSA', self.ctext, self.cvalue)
        self.app.config.write()
        self.ecard1label3.text=self.cvalue
        # обновление строки подключения
        self.oform.setting_update()
        self.dialog.dismiss(force=True)


# общий класс кнопки для блюд-групп
class TPButton_(RelativeLayout):
    cid = 'id'
    text='Error Name Item'  # основной текст на кнопке
    atext = []              # массив строк
    obutton = []            # объект товар
    oself = None
    lwp = True          # выравнивание текста
    irow = 3            # количество строк в названии
    iword = 13          # количество букв в строке
    bcolor = get_color_from_hex('ffffff')   # цвет фона
    tcolor = get_color_from_hex('000000')   # цвет названия

    def __init__(self, **kwargs):
        if kwargs.get('obutton'): self.obutton = kwargs.pop('obutton')
        if kwargs.get('bcolor'): self.bcolor = kwargs.pop('bcolor')
        if kwargs.get('tcolor'): self.tcolor = kwargs.pop('tcolor')
        if kwargs.get('text'): self.text = kwargs.pop('text')
        if kwargs.get('oself'): self.oself = kwargs.pop('oself')
        if kwargs.get('cid'): self.cid = kwargs.pop('cid')
        super(TPButton_, self).__init__(**kwargs)
        self.setdefault()
        self.setvalue()

    def setvalue(self):
        pass

    def setdefault(self):
        self.addbut()
        self.addtext()

    # распределение текста
    def wordwrap(self):
        self.atext = []
        if len(self.text) < self.iword:
            self.atext.append(self.text)
            return
        atname = self.text.split(' ')
        self.atext = []
        tname = ''
        i = 0
        for itname in atname:
            # если в слове букв больше чем задано
            if len(itname) >= self.iword:
                self.atext.append(itname)
                tname=''; i+=1
                continue
            # последняя запись
            try:
                inext = atname[i+1]
            except:
                self.atext.append(tname + itname)
                continue
            if len(tname + ' ' + itname + ' ' + inext ) < self.iword:
                tname = tname + ' '+ itname
            else:
                self.atext.append(tname + ' ' + itname)
                tname=''
            i+=1

        # формируем tname
        self.text = ''
        j=0
        for item in self.atext:
            if j >=self.irow: continue
            self.text = self.text + item + '\n'
            j +=1

    # добавление наименования
    def addtext(self):
        if self.lwp: self.wordwrap()
        y = .88; i=0
        for item in self.atext:
            if i == self.irow:continue
            ctext = Label_(pos_hint={"center_x": .5, "center_y": y}, size_hint=[1,0.25],
                                  text=item, halign='left', color=self.tcolor, font_size=16)
            ctext.bind(pos=ctext.on_texture_size, size=ctext.on_texture_size)
            self.add_widget(ctext)
            y-= 0.23; i +=1

    # добавляем кнопку
    def addbut(self):
        but_ = MDRaisedButton()
        but_.pos_hint={"center_x": 0.5, "center_y": 0.5}
        but_.size_hint=[1,1]
        but_.font_size = 16
        but_.background_normal= ' '
        but_.background_color =  self.bcolor
        but_.md_bg_color = self.bcolor
        but_.on_press = lambda :self.oself.buttonclick(self)
        self.add_widget(but_)

# кнопка с группой
class GPButton(TPButton_):
    irow = 4            # количество строк в названии
    iword = 13          # количество букв в строке
    def __init__(self, **kwargs):
        if kwargs.get('obutton'): self.obutton = kwargs.pop('obutton')
        if len(self.obutton) > 0:
            try:
                self.text = self.obutton['gname']
            except: pass
        super(GPButton, self).__init__(**kwargs)
        #self.setdefault()


    # добавление наименования
    def addtname(self):
        if self.lwp: self.wordwrap()
        y = .88; i=0
        for ilabel in self.result_tname:
            if i == self.irow:continue
            tname1 = Label_(pos_hint={"center_x": .5, "center_y": y}, size_hint=[1,0.25],
                                  text=ilabel,halign='left',color=self.tcolor, font_size=16)
            tname1.bind(pos=tname1.on_texture_size, size=tname1.on_texture_size)
            self.add_widget(tname1)
            y-= 0.23; i +=1




# кнопка блюда с ценой и названием
class TPButton(TPButton_):
    price = 0
    edizm = ''
    pcolor = get_color_from_hex('000000')   # цвет цены
    ecolor = get_color_from_hex('000000')   # цвет ед.изм
    rcolor = get_color_from_hex('ff0000')   # цвет ед.изм (красный)
    #gcolor = get_color_from_hex('007d00')   # цвет ед.изм (зеленый)

    def __init__(self, **kwargs):
        if kwargs.get('obutton'): self.obutton = kwargs.pop('obutton')
        if len(self.obutton) > 0:
            try:
                self.text = self.obutton['tname']
                self.price = self.obutton['price1']
                self.edizm = self.obutton['ei']
            except: pass
        if kwargs.get('pcolor'): self.pcolor = kwargs.pop('pcolor')
        if kwargs.get('ecolor'): self.ecolor = kwargs.pop('ecolor')
        super(TPButton, self).__init__(**kwargs)

    # установки
    def setvalue(self):
        #self.addbut()       # кнопка
        self.addedizm()     # добавление единицы измерения
        self.addprice()     # цена

    # Primary, Secondary, Hint, Error and Custom
    # добавление цены
    def addprice(self):
        lprice = Label_(pos_hint={"center_x": .15, "center_y": 0.15}, size_hint=[0.45,0.25],
                                  text=str(self.price),halign='left',color=self.rcolor, font_size=16)
        lprice.bind(pos=lprice.on_texture_size, size=lprice.on_texture_size)
        self.add_widget(lprice)

    # добавление ед.изм
    def addedizm(self):
        ledimz = Label_(pos_hint={"center_x": .75, "center_y": 0.15}, size_hint=[0.45,0.25],
                                  text=self.edizm,halign='right',color=gcolor, font_size=10)
        ledimz.bind(pos=ledimz.on_texture_size, size=ledimz.on_texture_size)
        self.add_widget(ledimz)

# кнопка строки чека
class TickButton(TPButton_):
    cid = 'ticpos'
    text = ''
    price = 0
    q = 0
    cr=0
    sr =0
    edizm = ''
    nn=''
    barcode = ''
    pcolor = get_color_from_hex('000000')   # цвет цены
    ecolor = get_color_from_hex('000000')   # цвет ед.изм

    def __init__(self, **kwargs):
        if kwargs.get('obutton'): self.obutton = kwargs.pop('obutton')
        if len(self.obutton) > 0:
            try:
                self.tname = self.obutton['tname']
                self.cr = self.obutton['cr']
                self.q = self.obutton['q']
                self.sr = self.obutton['sr']
                self.barcode = self.obutton['barcode']
                self.edizm = self.obutton['ei']

            except: pass
        if kwargs.get('pcolor'): self.pcolor = kwargs.pop('pcolor')
        if kwargs.get('ecolor'): self.ecolor = kwargs.pop('ecolor')
        if kwargs.get('nn'): self.nn = kwargs.pop('nn')

        super(TickButton, self).__init__(**kwargs)

    # установки
    def setvalue(self):
        #self.addbut()       # кнопка
        aa = 132
        self.addn()         # ПП
        self.addq()         # кол-во
        self.addtname()     # наименование блюда
        self.addbarcode()   # бвр-код
        self.addedizm()     # добавление количества
        self.addedizm()     # добавление единицы измерения
        self.addcr()        # цена
        self.addsr()        # сумма


    # Primary, Secondary, Hint, Error and Custom
    # добавление цены

        # добавление порядкового номера
    def addn(self):
        ln = Label_(pos_hint={"center_x": .025, "center_y": 0.27}, size_hint=[0.45,0.3],
                              text=self.nn+'.', halign='left',color=blcolor)
        ln.scale_factor = 1.2
        ln.bind(pos=ln.on_texture_size, size=ln.on_texture_size)
        self.add_widget(ln)

    def addcr(self):
        lcr = Label_(pos_hint={"center_x": .77, "center_y": .7}, size_hint=[0.15,0.30],
                                  text=str(self.cr),halign='center',color= bcolor,font_size=16)
        lcr.scale_factor = 1.2
        lcr.bind(pos=lcr.on_texture_size, size=lcr.on_texture_size)
        self.add_widget(lcr)

    # добавление суммы
    def addsr(self):
        lsr = Label_(pos_hint={"center_x": .91, "center_y": .7}, size_hint=[0.17,0.30],
                                  text=str(self.sr),halign='center',color= bcolor,font_size=16)
        lsr.scale_factor = 1.2
        lsr.bind(pos=lsr.on_texture_size, size=lsr.on_texture_size)
        self.add_widget(lsr)

        #lsr = MDLabel(pos_hint={"center_x": .86, "center_y": .7}, size_hint=[0.2,0.15],
        #                          text=str(self.sr),halign='center',color= self.ecolor, font_style= 'Overline')
        #self.add_widget(lsr)

    # добавление кол-ва
    def addq(self):
        lq = Label_(pos_hint={"center_x": .67, "center_y": .7}, size_hint=[0.15,0.3],
                                  text=str(self.q),halign='center',color= bcolor)
        lq.scale_factor = 1.2
        lq.bind(pos=lq.on_texture_size, size=lq.on_texture_size)
        self.add_widget(lq)

    # добавление ед.зм
    def addedizm(self):
        ledimz = Label_(pos_hint={"center_x": .67, "center_y": .27}, size_hint=[0.2,0.3],
                                  text=self.edizm,halign='center',color= gcolor)
        ledimz.bind(pos=ledimz.on_texture_size, size=ledimz.on_texture_size)
        self.add_widget(ledimz)

    # добавление наименования
    def addtname(self):
        tname1 = Label_(pos_hint={"center_x": .30, "center_y": 0.7}, size_hint=[0.50,0.3],
                              text=self.tname.strip(),halign='left',color=bcolor)
        tname1.scale_factor = 1.2
        #tname1.bind(size=tname1.setter('text_size'))
        tname1.bind(pos=tname1.on_texture_size, size=tname1.on_texture_size)

        self.add_widget(tname1)

    # добавление кода блюда
    def addbarcode(self):
        lbarcode = Label_(pos_hint={"center_x": .125, "center_y": 0.27}, size_hint=[0.25,0.3],
                              text=self.barcode,halign='left',color=gcolor)
        lbarcode.bind(pos=lbarcode.on_texture_size, size=lbarcode.on_texture_size)
        self.add_widget(lbarcode)

    def bun(self):
        aa = 111
        oban = self.oself.ids['banner']
        #oban.type = "one-line"
        oban.show()
        #self.ban = MDBanner()
        #self.ban.type = "one-line"
        #self.ban.text = "One line string text example without actions."

        #self.ban.over_widget = self.parent
        #self.ban.type = "one-line"
        #self.ban.left_action = ["CANCEL", lambda x: None]
        #self.ban.right_action = ["CLOSE", lambda x: self.ban.hide()]

        #self.ban.show()
        #banner.type = "three-line"
        #            banner.text = \
        #            [\
        #            "Three line string text example with two actions.", \
        #            "This is the second line of the banner message,", \
        #            "and this is the third line of the banner message.",
        #            ]
        #            banner.left_action = ["CANCEL", lambda x: None]
        #            banner.right_action = ["CLOSE", lambda x: banner.hide()]
        #            banner.show()

# Кнопка заказа
class TButton(Button_):
    acompany=[]
    oform = None
    rootcnt =None
    color_main = [0.45, 0.65, 0, 1]
    color_black = [0,0,0,1]
    color_search = get_color_from_hex('ffee00')
    def on_press(self, *args):
        if len(self.acompany)==0: return
        # вызываем страницу заказа
        return self.popupalert()


    # вызов сообщения о ошибке
    def popupalert(self):
        # данные
        phonetext = ''; opertext = ''
        try:
            opertext=self.acompany['name']
            for iphones in self.acompany['phones']:
                if len(phonetext) > 0: phonetext += '\n'
                phonetext += iphones['phone']
        except:
            pass

        # основной контейнер
        main_box = RelativeLayout()

        # название фирмы
        loper=Label_(text=opertext, color=self.color_main,size_hint= [.9, .1],
                     pos_hint= {"center_x": .5, "center_y": .95},size=self.size)
        loper.bind(pos=loper.on_texture_size, size=loper.on_texture_size)
        main_box.add_widget(loper)

        # телефоны перевозчика
        lphone=Label_(text=phonetext, color=self.color_black,size_hint= [.9, .45],
                      pos_hint= {"center_x": .5, "center_y": .65},size=self.size)
        lphone.bind(pos=lphone.on_texture_size, size=lphone.on_texture_size)
        main_box.add_widget(lphone)

        # дополнительный текст
        ctext= 'Вы можете уточнить наличие мест\n'
        ctext+='и забронировать билеты через перевозчика.\n'
        ctext+='Просто позвоните по любому из указанных телефонов.\n\n'
        ctext+='Расписание берется из открытых источников\n'
        ctext+='и может содержать неточности.'
        text_label = Label_(text=ctext, color=self.color_black,
                            size_hint= [1, .3],pos_hint= {"center_x": .5, "center_y": .3},
                            size = self.size,
                            )
        #text_label.bind(pos=text_label.on_texture_size, size=text_label.on_texture_size)
        main_box.add_widget(text_label)


        # кнопка закрытия формы
        but_exit = PButton_(text=u'Закрыть')
        but_exit.id = 'but_exit'
        but_exit.color = [0,0,0,1]
        but_exit.pos_hint= {"center_x": .5, "center_y": .06}
        but_exit.size_hint = [1,0.12]
        but_exit.font_size = 24
        but_exit.background_normal= ''
        but_exit.background_color = self.color_search
        but_exit.on_press = lambda *args: self.popup.dismiss()
        main_box.add_widget(but_exit)

        self.popup = Popup(id = 'popup_exit', title='Информация о перевозчике',title_color=[0,0,0,1],
                      pos_hint= {"center_x": .5, "center_y": .5}, content=main_box, size_hint=(0.8, 0.8),
                      background = "Data/Images/background_white.png")
        self.popup.open()


# Кнопка отзыва и паклёпа
class OButton(Button_):
    itype = 1       #1 - отзыв, 2 - паклёп
    acompany=[]
    oform = None
    rootcnt =None
    color_main = [0.45, 0.65, 0, 1]
    color_black = [0,0,0,1]
    color_search = get_color_from_hex('ffee00')
    color_red = get_color_from_hex('ff0000')

    def on_press(self, *args):
        if len(self.acompany)==0: return
        # вызываем страницу заказа
        return self.popupalert()


    # вызов сообщения о ошибке
    def popupalert(self):
        # основной контейнер
        main_box = RelativeLayout()

        # имя
        lbname=Label_(text=u'Имя', color=self.color_main,size_hint= [.9, .05],
                     pos_hint= {"center_x": 0.5, "center_y": .95},size=self.size)
        lbname.bind(pos=lbname.on_texture_size, size=lbname.on_texture_size)
        main_box.add_widget(lbname)
        if self.itype == 2: lbname.text = u'Имя (не обязательно)'

        self.ename = TextInput_(id='ename',size_hint= [.9, .07], pos_hint= {"center_x": 0.5, "center_y": .88})
        self.ename.sethinttext(u'Ваше имя ?')
        main_box.add_widget(self.ename)

        # телефон
        lbphone=Label_(text=u'Номер телефона', color=self.color_main,size_hint= [.9, .05],
                     pos_hint= {"center_x": 0.5, "center_y": .80},size=self.size)
        lbphone.bind(pos=lbphone.on_texture_size, size=lbphone.on_texture_size)
        main_box.add_widget(lbphone)
        if self.itype == 2: lbphone.text = u'Номер телефона (не обязательно)'

        self.ephone = TextInput_(id='ephone',size_hint= [.9, .07], pos_hint= {"center_x": 0.5, "center_y": .73})
        self.ephone.sethinttext(u'Ваш номер телефона ?')
        main_box.add_widget(self.ephone)

        # оценка
        if self.itype == 1:
            lbocenca=Label_(text=u'Оценка', color=self.color_main,size_hint= [.9, .05],
                         pos_hint= {"center_x": 0.5, "center_y": .65},size=self.size)
            lbocenca.bind(pos=lbocenca.on_texture_size, size=lbocenca.on_texture_size)
            main_box.add_widget(lbocenca)

            def setvalue(self, value):
                lbocenca1.text=str(int(value))

            self.estar = Slider(id='estar',size_hint= [.8, .07], pos_hint= {"center_x": 0.4, "center_y": .58},
                             min=0, max=5, value=1, step=1, orientation= "horizontal")
            self.estar.bind(value = setvalue)
            main_box.add_widget(self.estar)


            lbocenca1=Label_(text=str(self.estar.value), color=self.color_red,size_hint= [.1, .05],
                         pos_hint= {"center_x": 0.9, "center_y": .58},size=self.size)
            lbocenca1.bind(pos=lbocenca1.on_texture_size, size=lbocenca1.on_texture_size)
            main_box.add_widget(lbocenca1)

        # текст отзыва
        lbotzyv=Label_(text=u'Ваш отзыв', color=self.color_main,size_hint= [.9, .05],
                     pos_hint= {"center_x": 0.5, "center_y": .50},size=self.size)
        lbotzyv.bind(pos=lbotzyv.on_texture_size, size=lbotzyv.on_texture_size)
        if self.itype == 2:
            lbotzyv.text = u'Сообщение'
            lbotzyv.size_hint= [.9, .05]
            lbotzyv.pos_hint= {"center_x": 0.5, "center_y": .65}
        main_box.add_widget(lbotzyv)

        self.etext = TextInput_(id='etext',size_hint= [.9, .31], pos_hint= {"center_x": 0.5, "center_y": .30})
        self.etext.multiline = True
        self.etext.sethinttext('')
        if self.itype == 2:
            self.etext.size_hint= [.9, .46]
            self.etext.pos_hint= {"center_x": 0.5, "center_y": .38}
        #eotzyv._lines = 5
        main_box.add_widget(self.etext)

        # кнопка закрытия формы
        but_exit = Button_(text=u'Отправить')
        but_exit.id = 'but_exit'
        but_exit.color = [0,0,0,1]
        but_exit.pos_hint= {"center_x": .5, "center_y": .06}
        but_exit.size_hint = [1,0.12]
        but_exit.font_size = 24
        but_exit.background_normal= ''
        but_exit.background_color = self.color_search
        but_exit.on_press = lambda *args: self.chechvalue()
        main_box.add_widget(but_exit)

        self.popup = Popup(id = 'popup_exit', title=u'Ваш отзыв о компании "'+ self.acompany['name']+'"',title_color=[0,0,0,1],
                      pos_hint= {"center_x": .5, "center_y": .5}, content=main_box, size_hint=(0.8, 0.8),
                      background = "Data/Images/background_white.png")
        self.popup.open()

    # проверки на заполненные поля
    def chechvalue(self):
        ob = sendtoweb()
        lret = True
        if self.itype == 1:
            # отзыв
            if len(self.ename.text) == 0:
                self.ename.hint_text_color = self.color_red
                self.ename.sethinttext(u'Заполните Имя')
                lret = False
            if len(self.ephone.text) == 0:
                self.ephone.hint_text_color = self.color_red
                self.ephone.sethinttext(u'Заполните номер телефона')
                lret = False
            if len(self.etext.text) == 0:
                self.etext.hint_text_color = self.color_red
                self.etext.sethinttext(u'Напишите отзыв')
                lret = False
            if not lret: return
            ob.estar    = str(int(self.estar.value))

        elif self.itype == 2:
            # паклёп
            if len(self.etext.text) == 0:
                self.etext.hint_text_color = self.color_red
                self.etext.sethinttext(u'Напишите сообщение')
                return

        ob.ename    = self.ename.text
        ob.ephone   = self.ephone.text
        ob.etext    = self.etext.text
        ob.company  = self.acompany['pk']
        #Clock.schedule_once(ob.sendotvet, 0.1)
        if self.itype == 1: ob.sendotvet()
        elif self.itype == 2: ob.sendpakleb()
        self.popup.dismiss()

class ScrollButton(Button_):
    id = 'popupscroll'
    auto_dismiss =  False
    acompany=[]
    oform = None
    rootcnt =None
    color_main = [0.45, 0.65, 0, 1]
    color_black = [0,0,0,1]
    color_search = get_color_from_hex('ffee00')
    color_red = get_color_from_hex('ff0000')
    lprogress = False

    def runprogress(self,*args):
        while not self.lprogress :
            if self.lprogress:
                for item in [10,20,30,40,50,60,70,80,90,100]:
                    try:
                        value = item
                    except:
                        pass
                    print(str(value)+' her')
                    self.oform.ids['progress'].value = value   # прогресс на форме
                    if not self.lprogress:
                        self.oform.ids['progress'].value = 0
                        break
                    time.sleep(0.3)
                self.oform.ids['progress'].value = 0

    def on_press(self, *args):
        if len(self.acompany)==0: return
        # вызываем страницу заказа
        self.lprogress = True

        return  Clock.schedule_once(self.popupalert, 0.1)
        #Clock.schedule_once(self.self.popupalert)
        #return self.popupalert()

    def popupalert(self,*args):
        #Clock.schedule_once(self.runprogress, 0.1)
        main_box = BoxLayout(id='contentbox')
        main_box.orientation = "vertical"
        boxscroll = ScrollView()

        olabel = Label(id="content_text")
        olabel.size_hint_y = None
        #ob = sendtoweb()
        #ob.companyname  = self.acompany['slug']
        #ob.getotvet()


        # обработка результатов отзывов
        olabel.text = ''
        if len(ob.result) == 0:
            olabel.text = u'Отзывы отсутствуют'
        else:
            if len(ob.result['object']['reviews']) == 0:
                olabel.text = u'Отзывы отсутствуют'
            else:
                # отзывы есть - парсируем
                try:
                    for item in ob.result['object']['reviews']:
                        olabel.text = item['body']+ '\n'
                        ctime = datetime.strptime(item['date'],"%Y-%m-%dT%H:%M:%S")
                        olabel.text += item['name']+'   '+ datetime.strftime(ctime, "%d.%m.%Y %H:%M") + '\n'

                        olabel.text += '\n'
                        #olabel.text += u': '+str(item['mark']) + '\n\n'
                except:
                    olabel.text = u'Отзывы отсутствуют'

        #olabel.text = u"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus odio nisi, pellentesque molestie adipiscing vitae, aliquam at tellus. Fusce quis est ornare erat pulvinar elementum ut sed felis. Donec vel neque mauris. In sit amet nunc sit amet diam dapibus lacinia. In sodales placerat mauris, ut euismod augue laoreet at. Integer in neque non odio fermentum volutpat nec nec nulla. Donec et risus non mi viverra posuere. Phasellus cursus augue purus, eget volutpat leo. Phasellus sed dui vitae ipsum mattis facilisis vehicula eu justo.\n\n Quisque neque dolor, egestas sed venenatis eget, porta id ipsum. Ut faucibus, massa vitae imperdiet rutrum, sem dolor rhoncus magna, non lacinia nulla risus non dui. Nulla sit amet risus orci. Nunc libero justo, interdum eu pulvinar vel, pulvinar et lectus. Phasellus sed luctus diam. Pellentesque non feugiat dolor. Cras at dolor velit, gravida congue velit. Aliquam erat volutpat. Nullam eu nunc dui, quis sagittis dolor. Ut nec dui eget odio pulvinar placerat. Pellentesque mi metus, tristique et placerat ac, pulvinar vel quam. Nam blandit magna a urna imperdiet molestie. Nullam ut nisi eget enim laoreet sodales sit amet a felis.\n"
        olabel.text_size = (olabel.width-20), None
        olabel.line_height = 1.5
        olabel.color = [0,0,0,1]
        olabel.valign = "top"
        olabel.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        olabel.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        boxscroll.add_widget(olabel)

        main_box.add_widget(boxscroll)
        # кнопка закрытия формы
        but_exit = Button_(text=u'Закрыть')
        but_exit.id = 'but_exit'
        but_exit.color = [0,0,0,1]
        but_exit.pos_hint= {"center_x": .5, "center_y": .06}
        but_exit.size_hint = [1,0.12]
        but_exit.font_size = 24
        but_exit.background_normal= ''
        but_exit.background_color = self.color_search
        but_exit.on_press = lambda *args: self.popupclose()
        main_box.add_widget(but_exit)

        #self.lprogress = False

        self.popup = Popup(id = 'popup_exit', title=u'Отзывы о компании "'+ self.acompany['name']+'"',title_color=[0,0,0,1],
                      pos_hint= {"center_x": .5, "center_y": .5}, content=main_box, size_hint=(0.8, 0.8),
                      background = "Data/Images/background_white.png")
        self.popup.open()

    # закрываем popup
    def popupclose(self):
        self.popup.dismiss()


class TPIconButton_(MDRectangleFlatIconButton):
    cid = 'id'
    atext = []              # массив строк
    obutton = []            # объект товар

    bcolor = get_color_from_hex('ffffff')   # цвет фона
    tcolor = get_color_from_hex('000000')   # цвет названия



    def __init__(self, **kwargs):
        #if kwargs.get('obutton'): self.obutton = kwargs.pop('obutton')
        #if kwargs.get('bcolor'): self.bcolor = kwargs.pop('bcolor')
        #if kwargs.get('tcolor'): self.tcolor = kwargs.pop('tcolor')
        #if kwargs.get('text'): self.text = kwargs.pop('text')
        #if kwargs.get('oself'): self.oself = kwargs.pop('oself')
        #if kwargs.get('cid'): self.cid = kwargs.pop('cid')
        super(TPIconButton_, self).__init__(**kwargs)
        self.setdefault()
        #self.setvalue()
        #self.size_hint_x= None
        #self.width = 150

    def setvalue(self):
        self.markup = False

    def setdefault(self):
        pass
        #self.addbut()
        self.addtext()

    # добавление наименования
    def addtext(self):
        pass
        cbox = BoxLayout(spacing= '10dp')

        ic = MDIcon(icon='printer')
        ctext = MDLabel(text='I', font_size=20, can_capitalize= self.can_capitalize, shorten= True, text_color=[1,0,1,1])
        #ctext.bind(pos=ctext.on_texture_size, size=ctext.on_texture_size)
        #ctext = Label_(text='Helllo',halign='left',font_size=16)
        aa = 3432
        cbox.add_widget(ctext)
        cbox.add_widget(ic)
        self.add_widget(cbox)





class ExitPopup(MDDialog):
    dialog = None
    def __init__(self, **kwargs):
        super(ExitPopup, self).__init__(**kwargs)
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Are you sure?",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        aa = 465
        self.dialog = MDDialog(title="Close Application",

                               size_hint=(.3, None),
                               height=dp(200))

        self.dialog.add_action_button("Close me!",
                                      action=lambda *x: self.dismiss_callback())
        self.dialog.open()

    def dismiss_callback(self):
        self.dialog.dismiss()
