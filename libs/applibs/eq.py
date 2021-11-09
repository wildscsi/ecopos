__author__ = 'BM'
# -*- coding: utf-8 -*-
# работа с оборудованием

import sys
import glob
import platform
import serial
from copy import deepcopy
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton, MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.textinput import TextInput
from libs.applibs.keyboard import ekeyboard
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.card import MDCard, MDSeparator
from kivy.metrics import dp
from libs.baseclass.buttonlib import PMDCard            # контейней дополнительных свойств КСА

# контейнер для кнопок со свойствами
class RelativeLayout_(RelativeLayout):
    cvalue = None


class eq():
    listksa = {}        # перечень оборудования ФР, Кассы
    listprn = {}        # перечень оборудования принтеров чеков
    ofr = {}            # объект оборудования - Касса, ФР, принтер
    eqcnt = None        # контейнер с настройками оборудования
    oform = None        # форма на которой строятся контролы
    oButton = None      # контейнер ITEM для размещения контейнера с контролами редактирования
    eprop = None        # контрол редактирования свойст КСА
    lcodepage= {'1079':'spain win','1071':'germany','cp866':'russian DOS','1251':'russian win','1':'usa'}
    lpayname = ''       # типы оплат в зависимости от языка
    footer = ''
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        comcheck = {'descr': self.app.translation._('Чековый COM (TTY) принтер поддерживающий команды ESC/POS'),'name':'ESC/POS PRINTER','options':{'file':'ticket file name','bits':'Bit length: 7,8','parity':'N, odd, even','stop':'stop bits: 0, 1','soft':'software-controlled','hard':'1-on,0-off','upper':'capital letters','tapewidth':'width of belts','tags':'1-on,0-off','scode':'start code','ecode':'end code'}}
        titana = {}
        titana.update({'descr': self.app.translation._('Кассовый аппарат Титан-А, Титан-Плюс'),'name':'KSA TITAN-A','options':{'file':'ticket file name','tapewidth':'width of belts','cashier':'titan admin name', 'pwd':'titan admin passwoed', 'timeout':'titan timeout','delimiter':'delimiter', 'cnonce':'cnonce key'}})
        self.listksa.update({'comcheck':comcheck,'titana':titana })
        self.lpayname = self.app.translation._('наличные, карта 1, карта 2, банкет, депозит')
        super().__init__(**kwargs)

    # -----------------------------  восстановление конфигурации из файла настроек  -----------------------------------
    def getini(self):
        # проверка на наличие секции KSA
        lret = False
        for itemGr in self.app.config._sections:
            if itemGr == 'KSA':
                lret = True
                break
        if not lret: self.app.config.adddefaultsection('KSA')

        # добавляем листики ветки
        try: self.app.config._sections['KSA']['model'];
        except: self.app.config.setdefault('KSA', 'model', 'comcheck')

        try: self.app.config._sections['KSA']['port']
        except: self.app.config.setdefault('KSA', 'port', '/dev/ttyUSB0')

        try: self.app.config._sections['KSA']['tapewidth']
        except: self.app.config.setdefault('KSA', 'tapewidth', '40')

        try: self.app.config._sections['KSA']['codepage']
        except: self.app.config.setdefault('KSA', 'codepage', 'CP866')

        try: self.app.config._sections['KSA']['scode']
        except: self.app.config.setdefault('KSA', 'scode', '[27,64,27,116,7]')

        try: self.app.config._sections['KSA']['ecode']
        except: self.app.config.setdefault('KSA', 'ecode', '[27,100,4,29,86,49]')

        try: self.app.config._sections['KSA']['baud']
        except: self.app.config.setdefault('KSA', 'baud', '19200')

        try: self.app.config._sections['KSA']['upper']
        except: self.app.config.setdefault('KSA', 'upper', '1')

        try: self.app.config._sections['KSA']['tags']
        except: self.app.config.setdefault('KSA', 'tags', '1')

        try: self.app.config._sections['KSA']['host']
        except: self.app.config.setdefault('KSA', 'host', '192.168.8.2')

        try: self.app.config._sections['KSA']['footer']
        except: self.app.config.setdefault('KSA', 'footer', 'Thanks !')

        try: self.app.config._sections['KSA']['hard']
        except: self.app.config.setdefault('KSA', 'hard', '0')

        try: self.app.config._sections['KSA']['soft']
        except: self.app.config.setdefault('KSA', 'soft', '0')

        try: self.app.config._sections['KSA']['bits']
        except: self.app.config.setdefault('KSA', 'bits', '8')

        try: self.app.config._sections['KSA']['parity']
        except: self.app.config.setdefault('KSA', 'parity', 'N')

        try: self.app.config._sections['KSA']['stop']
        except: self.app.config.setdefault('KSA', 'stop', '0')

        try: self.app.config._sections['KSA']['file']
        except: self.app.config.setdefault('KSA', 'file', 'ticket.txt')

        try: self.app.config._sections['KSA']['payname']
        except: self.app.config.setdefault('KSA', 'payname', '["Cash","Card"]')

        try: self.app.config._sections['KSA']['cashier']
        except: self.app.config.setdefault('KSA', 'cashier', 'admin')

        try: self.app.config._sections['KSA']['pwd']
        except: self.app.config.setdefault('KSA', 'pwd', '555555')

        try: self.app.config._sections['KSA']['timeout']
        except: self.app.config.setdefault('KSA', 'timeout', '[1,5,90]')

        try: self.app.config._sections['KSA']['delimiter']
        except: self.app.config.setdefault('KSA', 'delimiter', '-')

        try: self.app.config._sections['KSA']['cnonce']
        except: self.app.config.setdefault('KSA', 'cnonce', '669bcf2a9b1c9deb')

        self.app.config.write()
        self.setting_update()
        return True


    # ----------------------------------------- читаем настройки оборудования -----------------------------------------
    # ----------------------------------------- формирование строки соединения с оборудованием ------------------------
    def setting_update(self):
        self.ofr.update({'model':self.app.config.get('KSA', 'model')})
        self.app.oeq.footer = self.app.config.get('KSA', 'footer')
        config={}
        if self.app.config.get('KSA', 'model') == 'comcheck':
            # ESC/POS чековый принтер
            self.ofr.update({'file':self.app.config.get('KSA', 'file')})
            if len(self.app.config.get('KSA', 'tapewidth')) == 0:
                self.ofr.update({'tapewidth':40})
            else:
                self.ofr.update({'tapewidth':int(self.app.config.get('KSA', 'tapewidth'))})
            self.ofr.update({'codepage':self.app.config.get('KSA', 'codepage')})
            self.ofr.update({'upper':int(self.app.config.get('KSA', 'upper'))})
            self.ofr.update({'tags':int(self.app.config.get('KSA', 'tags'))})
            self.ofr.update({'scode':eval(self.app.config.get('KSA', 'scode'))})
            self.ofr.update({'ecode':eval(self.app.config.get('KSA', 'ecode'))})

            if len(self.app.config.get('KSA', 'baud')) == 0:
                baud = 115200
            else:
                baud = int(self.app.config.get('KSA', 'baud'))
            config.update({'port':self.app.config.get('KSA', 'port'),'baud': baud ,'bits':int(self.app.config.get('KSA', 'bits')),'parity':self.app.config.get('KSA', 'parity'),'stop':int(self.app.config.get('KSA', 'stop')),'soft':int(self.app.config.get('KSA', 'soft')),'hard':int(self.app.config.get('KSA', 'hard'))})

        elif self.app.config.get('KSA', 'model') == 'titana':
            # КСА Титан-А
            # Касса Титан-А
                # пример
                #c1 = {'model':'titana','file':'ticket.txt','tapewidth':40,
                #        'config':{'host':'192.168.8.2','cnonce':'669bcf2a9b1c9deb',
                #                  'cashier':'admin','pwd':'555555','timeout':[1,5,90],'delimiter':'-'}}


            self.ofr.update({'file':self.app.config.get('KSA', 'file')})
            if len(self.app.config.get('KSA', 'tapewidth')) == 0:
                self.ofr.update({'tapewidth':40})
            else:
                self.ofr.update({'tapewidth':int(self.app.config.get('KSA', 'tapewidth'))})
            config.update({'host':self.app.config.get('KSA', 'host'),'cnonce':self.app.config.get('KSA', 'cnonce'), 'cashier':self.app.config.get('KSA', 'cashier') ,'pwd':self.app.config.get('KSA', 'pwd'),'timeout':self.app.config.get('KSA', 'timeout'),'delimiter':self.app.config.get('KSA', 'delimiter')})

        else: self.ofr = {}
        self.ofr.update({'config':config})
        print(self.ofr)
        return True

    # ------------------------------------- возвращаем перечень портов в системе --------------------------------------
    def getserial_port(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


    # -------------------------------------------  форма настройки КСА ------------------------------------------------
    def getform(self, oform, oButton):

        # контейнер для контролов, убиваем при закрытии формы
        self.oform = oform
        self.oButton = oButton

        # добавление общих контролов
        self.addcontrols_shared()

        # добавляем контролы ESC/POS принтеру
        if self.app.oeq.ofr['model'] == 'comcheck': self.addcontrols_comcheck()

        # форма отображения настроек Титан-А
        elif self.app.oeq.ofr['model'] == 'titana': self.addcontrols_titana()



    # добавление общих контролов
    def addcontrols_shared(self):
        self.eqcnt = RelativeLayout(size=self.oButton.size, pos=self.oButton.pos)
        self.eqcnt.id = 'cnt'

        # кнопка выхода
        cmdExit =  MDIconButton(icon = "close-circle-outline", pos_hint = {"center_x": .05, 'center_y': .85})
        cmdExit.id = 'cmdexit'
        cmdExit.on_press=lambda :self.oform.close_frsetting(self.oButton)
        self.eqcnt.add_widget(cmdExit)

        # выбор типа КСА model
        lmodelcnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.12, 'center_y': .92})
        lmodel = MDLabel(text=self.app.translation._('тип КСА'), color=self.app.color_gray, font_style='H7', halign='right', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
        lmodelcnt.add_widget(lmodel)
        emodelcnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.4, 'center_y': .92})
        emodelcnt.id='emodelcnt'
        emodel = MDFlatButton(text=self.app.oeq.listksa[self.app.oeq.ofr['model']]['name'],font_style="H2", pos_hint={'center_x': 0.5, 'center_y': .5},size_hint_y=None, on_release= self.getmodel)
        #emodel = MDLabel(text='ESC/POS', color=self.app.color_white, font_style='H6', halign='left', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
        emodelcnt.add_widget(emodel)

        # выбор типа оплат
        lpaynamecnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.12, 'center_y': .44})
        lpayname = MDLabel(text=self.app.translation._('виды оплат'), color=self.app.color_gray, font_style='H7', halign='right', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
        lpaynamecnt.add_widget(lpayname)
        epaynamecnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.4, 'center_y': .44})
        epaynamecnt.id = 'epaynamecnt'
        epayname = MDFlatButton(text=(' '.join([str(elem) for elem in eval(self.app.config.get('KSA','payname'))])[0:20] if len(' '.join([str(elem) for elem in eval(self.app.config.get('KSA','payname'))]))<20 else ' '.join([str(elem) for elem in eval(self.app.config.get('KSA','payname'))])[0:20]+' ...'),font_style="H2", pos_hint={'center_x': 0.5, 'center_y': .5}, size_hint_y=None, on_release= self.editpayname)
        epaynamecnt.add_widget(epayname)

        # нижний колонтитул
        lfootercnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.12, 'center_y': .32})
        lfooter = MDLabel(text=self.app.translation._('нижний колонтитул'), color=self.app.color_gray, font_style='H7', halign='right', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
        lfootercnt.add_widget(lfooter)
        efootercnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.4, 'center_y': .32})
        efootercnt.id = 'efootercnt'
        efooter = MDFlatButton(text=(self.app.oeq.footer[0:20] if len(self.app.oeq.footer)<20 else self.app.oeq.footer[0:20]+' ...'),font_style="H2", pos_hint={'center_x': 0.5, 'center_y': .5}, size_hint_y=None, on_release= self.editfooter)
        efootercnt.add_widget(efooter)


        # дополнительные свойства
        # подпись контейнера со свойствами
        lpropcnt =  RelativeLayout(size_hint = [0.4, 0.15], pos_hint={'center_x': 0.80, 'center_y': .92})
        lprop = MDLabel(text=self.app.translation._('дополнительные свойства (дв.клик)'), color=self.app.color_gray, font_style='H7', halign='left', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
        lpropcnt.add_widget(lprop)
        self.eqcnt.add_widget(lpropcnt)

        # формирование скрола со свойствами
        # ширина скрола - высота контейнера\6* кол=во свойств
        ih=round(self.eqcnt.height/6* len(self.listksa[self.app.config.get('KSA','model')]['options']),0)
        ecrollprop = ScrollView(pos_hint={'center_x': 0.77, 'center_y': .6}, size_hint = [0.35, 0.57],cols=1, bar_width = 10, scroll_timeout= 250, scroll_distance=20)
        egrid = BoxLayout(orientation = 'vertical', padding= 3, spacing=3, height= ih, size_hint_y= None)

        for itemprop in self.listksa[self.app.config.get('KSA','model')]['options']:
            # контейнер конкретного свойства
            ecard = PMDCard(oform=self, ctext=itemprop, cprim=self.listksa[self.app.config.get('KSA','model')]['options'][itemprop], cvalue=self.app.config.get('KSA', itemprop),text_color = self.app.color_white,  md_bg_color  = self.app.color_hdarkblue)
            ecard = PMDCard(oform=self, ctext=itemprop, cprim=self.listksa[self.app.config.get('KSA','model')]['options'][itemprop], cvalue=self.app.config.get('KSA', itemprop),text_color = self.app.color_white,  md_bg_color  = self.app.color_hdarkblue)
            egrid.add_widget(ecard)

        ecrollprop.add_widget(egrid)
        self.eqcnt.add_widget(ecrollprop)

        self.eqcnt.add_widget(lmodelcnt);self.eqcnt.add_widget(emodelcnt)
        self.eqcnt.add_widget(lpaynamecnt);self.eqcnt.add_widget(epaynamecnt)
        self.eqcnt.add_widget(lfootercnt);self.eqcnt.add_widget(efootercnt)
        self.oButton.add_widget(self.eqcnt)







    # редактирование футера
    def editfooter(self, *args):
        self.efooteredit = TextInput(text=self.app.oeq.footer, hint_text=self.app.translation._('Футер чека'),pos_hint = {"center_x": .51, "center_y": .24}, size_hint=(0.55,0.17))
        self.eqcnt.add_widget(self.efooteredit)
        # добавляем клавиатуру в WIN и Linux
        if platform.system() in ["Windows","Linux"]:
            if self.oform.kbd == None:
                self.oform.kbd = ekeyboard()
                self.oform.kbd.bind(on_key_up = self._on_keyboard_up_footer)
                self.oform.kbd.text = self.app.oeq.footer
                self.oform.kbd.lclose = False
                self.oform.add_widget(self.oform.kbd)



    # добавляем контролы ESC/POS принтеру
    def addcontrols_comcheck(self):
            # кнопка выбора COM порта
            lcomcnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.12, 'center_y': .80})
            lcom = MDLabel(text=self.app.translation._('COM порт'), color=self.app.color_gray, font_style='H7', halign='right', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
            lcomcnt.add_widget(lcom)
            ecomcnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.4, 'center_y': .80})
            ecomcnt.id = 'ecomcnt'
            ecom = MDFlatButton(text=self.app.oeq.ofr['config']['port'],font_style="H2", pos_hint={'centr_x': 0.5, 'center_y': .5}, size_hint_y=None, on_release= self.getport)
            ecomcnt.add_widget(ecom)

            # скорость порта
            lbaudcnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.12, 'center_y': .68})
            lbaud = MDLabel(text=self.app.translation._('скорость порта'), color=self.app.color_gray, font_style='H7', halign='right', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
            lbaudcnt.add_widget(lbaud)
            ebaudcnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.4, 'center_y': .68})
            ebaudcnt.id = 'ebaudcnt'
            ebaud = MDFlatButton(text=str(self.app.oeq.ofr['config']['baud']),font_style="H2", pos_hint={'center_x': 0.5, 'center_y': .5}, size_hint_y=None, on_release= self.getboud)
            ebaudcnt.add_widget(ebaud)


            # кодировка codepage
            lcodepagecnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.12, 'center_y': .56})
            lcodepage = MDLabel(text=self.app.translation._('кодовая страница'), color=self.app.color_gray, font_style='H7', halign='right', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
            lcodepagecnt.add_widget(lcodepage)
            ecodepagecnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.40, 'center_y': .56})
            ecodepagecnt.id = 'ecodepagecnt'
            try:
                ccodepage = str(self.app.oeq.ofr['codepage']) + ' (' + self.app.oeq.lcodepage[str(self.app.oeq.ofr['codepage'])] +')'
            except:
                ccodepage = 'Empty'
            ecodepage = MDFlatButton(text=ccodepage,font_style="H2", pos_hint={'center_x': 0.5, 'center_y': .5}, size_hint_y=None, on_release= self.getcodepage)
            ecodepage.id = 'ecodepage'
            ecodepagecnt.add_widget(ecodepage)

            # кнопки
            cmdtest = MDRaisedButton(text=self.app.translation._('ТЕСТ'),font_style="Button",  pos_hint={'center_x': 0.4, 'center_y': .10}, size_hint = [0.09, 0.12], md_bg_color= self.app.color_green, text_color=self.app.color_igray, on_release= self.testksa)
            cmdtest.id = 'cmdtest'

            # добавляем контейнеры с контролами
            self.eqcnt.add_widget(lcomcnt);  self.eqcnt.add_widget(ecomcnt)
            self.eqcnt.add_widget(lbaudcnt); self.eqcnt.add_widget(ebaudcnt)
            self.eqcnt.add_widget(lcodepagecnt); self.eqcnt.add_widget(ecodepagecnt)
            self.eqcnt.add_widget(cmdtest)
            #;  self.eqcnt.add_widget(cmdsave);  self.eqcnt.add_widget(cmdcancel)

     # --------------------------------------  добавление контролов КСА Титан ----------------------------------------
    def addcontrols_titana(self):
        # настройка IP адреса
        items = []
        self.eqcnt.dialogip = MDDialog(
        title=self.app.translation._("IP"),
        type="confirmation",
        md_bg_color=self.app.bcolor3,
        items = items,
            buttons=[
                MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogip_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.save_port),
                ],
            )
        # IP адрес
        lipcnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.12, 'center_y': .69})
        lip = MDLabel(text=self.app.translation._('IP адрес'), color=self.app.color_gray, font_style='H7', halign='right', pos_hint={"center_x": .5, "center_y": .5}, size_hint_y=None)
        lipcnt.add_widget(lip)
        eipcnt =  RelativeLayout(size_hint = [0.2, 0.15], pos_hint={'center_x': 0.4, 'center_y': .69})
        eipcnt.id = 'eipcnt'
        eip = MDFlatButton(text=self.app.oeq.ofr['config']['host'],font_style="H6", pos_hint={'center_x': 0.5, 'center_y': .5}, size_hint_y=None, on_release= self.eqcnt.dialogip.open)
        eip.id = 'eip'
        eipcnt.add_widget(eip)
        self.eqcnt.add_widget(lipcnt); self.eqcnt.add_widget(eipcnt)

    # --------------------------------------  обработка нажатий кнопок FOOTER  ---------------------------------------
    def _on_keyboard_up_footer(self, keyboard, keycode, text, modifiers):
        self.oform.kbd.updkeykode(keyboard, keycode, text, modifiers)
        if self.oform.kbd.lclose:
            self.oform.remove_widget(self.oform.kbd)
            self.eqcnt.remove_widget(self.efooteredit)
            self.oform.kbd = None
        else:
            self.efooteredit.text = self.oform.kbd.text
            self.app.config.set('KSA', 'footer', self.oform.kbd.text)
            self.app.config.write()
            # установка значения
            for item in self.eqcnt.children:
                try:
                    # поиск значения
                    if item.id == 'efootercnt':
                        item.children[0].text =self.oform.kbd.text
                except: pass
            # пеергрузка контролов
            self.setting_update()

    # --------------------------------------  обработка нажатий кнопок редактирования свойств  ---------------------------------------
    def _on_keyboard_up_properties(self, keyboard, keycode, text, modifiers):
        self.oform.kbd.updkeykode(keyboard, keycode, text, modifiers)
        if self.oform.kbd.lclose:
            self.oform.remove_widget(self.oform.kbd)
            self.eqcnt.remove_widget(self.eprop)
            self.oform.kbd = None
        else:
            self.eprop.text = self.oform.kbd.text
            self.app.config.set('KSA', 'footer', self.oform.kbd.text)
            self.app.config.write()
            # установка значения
            for item in self.eqcnt.children:
                try:
                    # поиск значения
                    if item.id == 'efootercnt':
                        item.children[0].text =self.oform.kbd.text
                except: pass
            # пеергрузка контролов
            self.setting_update()


    # POP-UP форма выбора COM порта, вешаем на контейнер с настройкуами
    def getport(self, *args):
        items = []; i=0
        for itemcom in self.getserial_port():
            items.append(ItemConfirm(text=itemcom))
            # отметка выбранной позиции
            if self.app.oeq.ofr['config']['port'] == itemcom:
                items[i].ids.check.active = True
            else:
                items[i].ids.check.active = False
            i+=1
        self.eqcnt.dialogport = MDDialog(
        title=self.app.translation._("Выбор порта"),
        type="confirmation",
        md_bg_color=self.app.bcolor3,
        items = items,
        buttons=[MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogport_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.save_port),],)
        self.eqcnt.dialogport.open()

    # POP-UP форма выбора типов оплат
    def editpayname(self, *args):
        items = []; i=0
        for item in [c.strip() for c in self.lpayname.split(',') if not c.isspace()] :
            items.append(ItemMultyConfirm(text=item))
            # отметка выбранных позиций
            lret = False
            for itemselect in eval(self.app.config.get('KSA', 'payname')):
                if item == itemselect:
                    items[i].ids.check.active = True
                    lret = True
                    break
            if not lret:
                # наличные всегда активны
                if item in ['наличные','cash']:
                    items[i].ids.check.active = True
                else:
                    items[i].ids.check.active = False
            i+=1
        self.eqcnt.dialogpayname = MDDialog(
        title=self.app.translation._("Выбор типа оплат"),
        type="confirmation",
        md_bg_color=self.app.bcolor3,
        items = items,
        buttons=[MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogpayname_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.save_payname),],)
        self.eqcnt.dialogpayname.open()



    # POP-UP форма выбора кодовой страницы
    def getcodepage(self, *args):
        items = []; i=0
        # 866 - winrus esp ger eng
        for itemcode in self.app.oeq.lcodepage:
            items.append(ItemConfirm(text=itemcode + ' (' + self.app.oeq.lcodepage[itemcode] + ')'))
            # отметка выбранной позиции
            if self.app.oeq.ofr['codepage'] == itemcode:
                items[i].ids.check.active = True
            else:
                items[i].ids.check.active = False
            i+=1
        self.eqcnt.dialogcodepage = MDDialog(
        title=self.app.translation._("Кодовая страница"),
        type="confirmation",
        md_bg_color=self.app.bcolor3,
        items = items,
        buttons=[MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogcodepage_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.save_codepage),],)
        self.eqcnt.dialogcodepage.open()

    # POP-UP форма выбора скорости COM-порта
    def getboud(self, *args):
        items = []; i=0
        for itembaud in ['9600','19200','38400','57600','115200']:
            items.append(ItemConfirm(text=itembaud))
            # отметка выбранной позиции
            if str(self.app.oeq.ofr['config']['baud']) == itembaud:
                items[i].ids.check.active = True
            else:
                items[i].ids.check.active = False
            i+=1
        self.eqcnt.dialogbaud = MDDialog(
        title=self.app.translation._("Скорость COM порта"),
        type="confirmation",
        md_bg_color=self.app.bcolor3,
        items = items,
        buttons=[MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogbaud_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.save_baud),],)
        self.eqcnt.dialogbaud.open()

    # POP-UP форма выбора ширины ленты
    def gettapewidth(self, *args):
        items = []; i=0
        for itemtape in ['40','44','57','76','80']:
            items.append(ItemConfirm(text=itemtape))
            # отметка выбранной позиции
            if str(self.app.oeq.ofr['tapewidth']) == itemtape:
                items[i].ids.check.active = True
            else:
                items[i].ids.check.active = False
            i+=1
        self.eqcnt.dialogtape = MDDialog(
        title=self.app.translation._("Ширина ленты"),
        type="confirmation",
        md_bg_color=self.app.bcolor3,
        items = items,
        buttons=[
                MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogtape_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.save_tape),
                ],
            )
        self.eqcnt.dialogtape.open()

    # POP-UP форма выбора модели принтера, вешаем на контейнер с настройкуами, как и все остальные свойства:
    def getmodel(self, *args):
        items = []; i=0
        for itemksa in self.app.oeq.listksa:
            items.append(ItemConfirm(text=self.app.oeq.listksa.get(itemksa)['name']))
            # отметка выбранной позиции
            if self.app.oeq.listksa[self.app.oeq.ofr['model']]['name'] == self.app.oeq.listksa.get(itemksa)['name']:
                items[i].ids.check.active = True
            else:
                items[i].ids.check.active = False
            i+=1
        self.eqcnt.dialogmodel = MDDialog(
        title=self.app.translation._("Выбор модели кассы, ФР, принтера"),
        type="confirmation",
        md_bg_color=self.app.bcolor3,
        items = items,
        buttons=[
                MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialogmodel_close),
                MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.save_model),
                ],
            )
        self.eqcnt.dialogmodel.open()


    # закрытие окна с выбором типа кассы
    def dialogmodel_close(self, *args):
        self.eqcnt.dialogmodel.dismiss(force=True)

    # закрытие окна с выбором типов оплат
    def dialogpayname_close(self, *args):
        self.eqcnt.dialogpayname.dismiss(force=True)

    def dialogport_close(self, *args):
        self.eqcnt.dialogport.dismiss(force=True)

    def dialogtape_close(self, *args):
        self.eqcnt.dialogtape.dismiss(force=True)

    def dialogbaud_close(self, *args):
        self.eqcnt.dialogbaud.dismiss(force=True)

    def dialogcodepage_close(self, *args):
        self.eqcnt.dialogcodepage.dismiss(force=True)

    def dialogip_close(self, *args):
        self.eqcnt.dialogip.dismiss(force=True)

    # установка настроек с выбором кассы, смотрим на контейнере настройки и сохраняем.
    def save_model(self, *args):
        ctext = ''
        for item in self.eqcnt.children:
            try:
                if item.id == 'emodelcnt':
                    # поиск значения
                    for itemmoodel in self.eqcnt.dialogmodel.items:
                        if itemmoodel.ids.check.active: ctext = itemmoodel.text
                    item.children[0].text =ctext
            except: pass
        # сохнаняем настройки оборудования, перечитываем конфиг, убираем POP-UP
        for item in self.listksa:
            if self.listksa[item]['name'] == ctext:
                self.app.config.set('KSA', 'model', item)
                self.app.config.write()
                self.setting_update()
                cprinter = item
        self.eqcnt.dialogmodel.dismiss(force=True)

        # меняем контролы при переходе с одного КСА на другой
        self.oButton.remove_widget(self.eqcnt)
        self.addcontrols_shared()
        eval('self.addcontrols_'+cprinter+'()')

    # выбор номера порта
    def save_port(self, *args):
        ctext = ''
        # установка значения
        for item in self.eqcnt.children:
            try:
                # поиск значения
                if item.id == 'ecomcnt':
                    for itemcom in self.eqcnt.dialogport.items:
                        if itemcom.ids.check.active: ctext = itemcom.text
                    item.children[0].text =ctext
            except: pass
        self.app.config.set('KSA', 'port', ctext)
        self.app.config.write()
        self.setting_update()
        self.eqcnt.dialogport.dismiss(force=True)

    # установка настроек КСА с выбором ширины ленты
    def save_tape(self, *args):
        ctext = ''
        for item in self.eqcnt.children:
            try:
                if item.id == 'etapecnt':
                    # поиск значения
                    for itemtape in self.eqcnt.dialogtape.items:
                        if itemtape.ids.check.active: ctext = itemtape.text
                    item.children[0].text =ctext
            except: pass
        self.app.config.set('KSA', 'tapewidth', ctext)
        self.app.config.write()
        self.setting_update()
        self.eqcnt.dialogtape.dismiss(force=True)

    # установка настроек КСА выбор скорости COM - порта
    def save_baud(self, *args):
        ctext = ''
        for item in self.eqcnt.children:
            try:
                if item.id == 'ebaudcnt':
                    # поиск значения
                    for itembaud in self.eqcnt.dialogbaud.items:
                        if itembaud.ids.check.active: ctext = itembaud.text
                    item.children[0].text =ctext
            except: pass
        self.app.config.set('KSA', 'baud', ctext)
        self.app.config.write()
        self.setting_update()
        self.eqcnt.dialogbaud.dismiss(force=True)

    # выбор кодовой странцы
    def save_codepage(self, *args):
        ctext = ''
        for item in self.eqcnt.children:
            try:
                if item.id == 'ecodepagecnt':
                    # поиск значения
                    for itemcode in self.eqcnt.dialogcodepage.items:
                        if itemcode.ids.check.active: ctext = itemcode.text
                    item.children[0].text = ctext
            except: pass
        # сохнаняем настройки оборудования, перечитываем конфиг, убираем POP-UP
        self.app.config.set('KSA', 'codepage', ctext.split(' ')[0])
        self.app.config.write()
        self.setting_update()
        self.eqcnt.dialogcodepage.dismiss(force=True)

    # выбор кодовой странцы
    def save_payname(self, *args):
        ltext = []
        for item in self.eqcnt.children:
            try:
                if item.id == 'epaynamecnt':
                    # поиск значения
                    for itemcode in self.eqcnt.dialogpayname.items:
                        if itemcode.ids.check.active: ltext.append(itemcode.text)
                    # переписываем значение кнопки
                    item.children[0].text = (' '.join([str(elem) for elem in ltext]))[0:20]
                    break
            except: pass
        # сохнаняем настройки оборудования, перечитываем конфиг, убираем POP-UP
        self.app.config.set('KSA', 'payname', str(ltext))
        self.app.config.write()
        self.setting_update()
        self.eqcnt.dialogpayname.dismiss(force=True)


    # тестирование КСА
    def testksa(self, *args):
        print('test')


# отметка чек-бокса при нажатии на название
class ItemConfirm(OneLineAvatarIconListItem):
    divider = None
    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

# отметка чек-бокса при нажатии на название
class ItemMultyConfirm(OneLineAvatarIconListItem):
    divider = None
    def set_icon(self, instance_check):
        # запрет на unchck наличных
        print('check')
        if instance_check.active:
            instance_check.active = False
        else:
            instance_check.active = True
