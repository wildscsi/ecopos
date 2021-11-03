# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 CPV.BY
#
# For suggestions and questions:
# <7664330@gmail.com>
#
# LICENSE: Commercial

import os
from kivy.uix.screenmanager import Screen
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from libs.applibs.lbmenuimport import tMenuImport
from kivymd.theming import ThemeManager
#from kivy.uix.relativelayout import RelativeLayout
#from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Line, Rectangle
from libs.base.lbcontrol import Button_, Label_
from libs.baseclass.buttonlib import PButton_, TButton
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton, MDRectangleFlatIconButton, MDRoundFlatButton, MDRoundFlatIconButton, MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from libs.base.lbcontrol import TextInput_
from kivymd.app import MDApp


class RelativeLayout_(MDRelativeLayout):
    cvalue = None
    id=''

# кнопка отображения перечня бдюда
class PButton(MDRectangleFlatIconButton):
    ogruppa = []
    line_color=(0, 0, 0, 0)

    def on_press(self):
        return self.parent.parent.parent.parent.parent.parent.loadtovar(ocnt=self, ogruppa=self.ogruppa)

# чек-бокс активности группы
class gMDCheckbox(MDCheckbox):
    id=''
    app = None
    ogruppa = []

    def on_press(self):
        lf =0
        if self.active: lf = 1
        if not self.app.osql.update('gruppa',{'lf':lf},'igruppa='+str(self.ogruppa['igruppa'])):
            if self.active: self.active = False
            else: self.active = True
        self.app.osql.commit()
        return True

# чек-бокс активности блюда
class tMDCheckbox(MDCheckbox):
    app = None
    otovar = []
    def on_press(self):
        lf =0
        if self.active: lf = 1
        if not self.app.osql.update('tovar',{'lf':lf},'itovar='+str(self.otovar['itovar'])):
            if self.active: self.active = False
            else: self.active = True
        self.app.osql.commit()
        return True


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ImpexpScreen(Screen):
    app = None
    # работа с файлами
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    listgruppa = []                     # перечень групп
    listtovar = []                      # перечень блюд
    select_group = ''                   # выбранная группа

    theme_cls = ThemeManager()
    VARIABLE = ""
    menu_labels = [
        {"viewclass": "MDMenuItem",
         "text": "Label1"},
        {"viewclass": "MDMenuItem",
         "text": "Label2"},
    ]

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.loadgrid()

    # поиск облюда по названию
    def search_tovar(self):
        csearch = self.ids['esearch'].text
        if not self.app.osql.select('tovar',''): return False
        self.listtovar = []
        listtovar = self.app.osql.getresult()
        for item in listtovar:
            if csearch.upper() in (item['tname']).upper():
                self.listtovar.append(item)
        self.ids['esearch'].text = ''

        # разотметка групп
        for item in self.ids['box_gruppa'].children:
            for item2 in item.children:
                if item2.id[:4] == 'but_':
                    item2.md_bg_color = [0,0,0,0]
                    item2.text_color = [0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1]
        # показываем выборку
        self.create_tovar()


    # загрузка данных в гриды
    def loadgrid(self):
        if not self.app.osql.select('gruppa',''): return False
        self.listgruppa = self.app.osql.getresult()
        self.ids['box_gruppa'].children = []            # очищаем грид

        # формируем экран c группами
        self.create_gruppa(self.ids.box_gruppa)

        # выбираем первую группу и отображаем по ней блюда
        if len(self.listgruppa) > 0: self.loadtovar('',self.listgruppa[0])

    # заполняем группы  ---------------------------
    def create_gruppa(self, box_gruppa):
        self.ids['box_gruppa'].rows = len(self.listgruppa)
        # рассчитываем высоту контейнера с группами
        def update_size(instance, value):
            for item in instance.children:
                item.size = instance.size[0],instance.size[0]/4

        box_gruppa.bind(pos=update_size, size=update_size)
        for gitem in self.listgruppa:
            # основной контейнер c группами
            aa = 6
            #main_cont = RelativeLayout_(id='gr_'+str(gitem['igruppa']),size_hint_y= None, size=[300, box_gruppa.parent.size[1]])
            main_cont = RelativeLayout_(size_hint_y= None, size=[300, box_gruppa.parent.size[1]])
            main_cont.id = 'gr_'+str(gitem['igruppa'])
            box_gruppa.add_widget(main_cont)

            # фон контейнера
            with main_cont.canvas.before:
                Color(self.app.main_background)
                main_cont.rect = Rectangle(size=self.size,pos=main_cont.pos)
            def update_rect(instance, value):
                instance.rect.size = instance.size
            main_cont.bind(pos=update_rect, size=update_rect)

            # название группы
            lgruppa = Label_(pos_hint={"center_x": .43, "center_y": .8}, size_hint=[0.8,0.3],
                                  text=gitem['gname'],color=self.app.color_black, halign='center')
            lgruppa.id = 'gname_'+str(gitem['igruppa'])
            lgruppa.bind(pos=lgruppa.on_texture_size, size=lgruppa.on_texture_size)
            main_cont.add_widget(lgruppa)

            # код группы
            lcode = Label_(pos_hint={"center_x": .43, "center_y": .27}, size_hint=[0.5,0.3],
                                  text='code: '+ gitem['code'],color=self.app.color_gray, halign='center')
            lcode.id = 'idcode'+gitem['code']
            lcode.bind(pos=lcode.on_texture_size, size=lcode.on_texture_size)
            main_cont.add_widget(lcode)

            # активность группы
            chlf = gMDCheckbox(pos_hint={"center_x": .1, "center_y": .3}, size_hint=[0.1,0.1], active=gitem['lf'])
            chlf.id = 'idch'+str(gitem['igruppa'])
            chlf.ogruppa = gitem
            chlf.app = self.app
            #chlf.md_bg_color = self.app.color_green
            main_cont.add_widget(chlf)

            # отображение товаров
            but_tovar = PButton()
            but_tovar.id = 'but_'+str(gitem['igruppa'])
            but_tovar.ogruppa = gitem
            but_tovar.pos_hint={"center_x": .97, "center_y": 0.5}
            #but_tovar.size_hint_y=0.8
            #but_tovar.md_bg_color = self.app.color_black
            #but_tovar.size_hint_x=0.1
            but_tovar.icon = 'arrow-right-bold'
            main_cont.add_widget(but_tovar)



    # заполнение грида с блюдами
    def loadtovar(self, ocnt, ogruppa):

        if not self.app.osql.select('tovar','code="'+ogruppa['code']+'"'): return False
        self.listtovar = self.app.osql.getresult()

        if ogruppa != '':
            # разотметка и отметка выбранной группы
            for item in self.ids['box_gruppa'].children:
                for item2 in item.children:
                    if item2.id[:4] == 'but_':
                        item2.md_bg_color = [0,0,0,0]
                        item2.text_color = [0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1]
            if ocnt == '':
                for item in self.ids['box_gruppa'].children:
                    for item2 in item.children:
                        if item2.id == 'but_'+str(ogruppa['igruppa']):
                            item2.md_bg_color = [0,0,1,1]
                            item2.text_color = [1, 1, 0, 1]
                            break
            else:
                ocnt.md_bg_color = [0,0,1,1]
                ocnt.text_color = [1, 1, 0, 1]
        self.create_tovar()

    def create_tovar(self):
        # заполнение грида с блюдами
        self.ids['box_tovar'].children = []
        self.ids['box_tovar'].rows = len(self.listtovar)
        box_tovar = self.ids['box_tovar']

        # рассчитываем высоту контейнера с группами
        def update_size(instance, value):
            for item in instance.children:
                item.size = instance.size[0],instance.size[0]/8

        box_tovar.bind(pos=update_size, size=update_size)
        for gitem in self.listtovar:
            # основной контейнер c группами
            main_cont = RelativeLayout_(size_hint_y= None, size=[300, box_tovar.parent.size[1]])
            main_cont.id = 'gr_'+str(gitem['itovar'])
            box_tovar.add_widget(main_cont)

            # фон контейнера
            with main_cont.canvas.before:
                Color(self.app.main_background)
                main_cont.rect = Rectangle(size=self.size,pos=main_cont.pos)
            def update_rect(instance, value):
                instance.rect.size = instance.size
            main_cont.bind(pos=update_rect, size=update_rect)

            # название блюда
            ltname = Label_(pos_hint={"center_x": .4, "center_y": .8}, size_hint=[0.8,0.3],
                                  text=gitem['tname'],color=self.app.color_black, halign='center')
            ltname.id ='tovar_'+str(gitem['itovar'])
            ltname.bind(pos=ltname.on_texture_size, size=ltname.on_texture_size)
            main_cont.add_widget(ltname)

            # активность блюда
            chlf = tMDCheckbox(pos_hint={"center_x": .04, "center_y": .3}, size_hint=[0.1,0.1], active=gitem['lf'])
            chlf.id = 'idch'+str(gitem['itovar'])
            chlf.otovar = gitem
            chlf.app = self.app
            main_cont.add_widget(chlf)

            # баркод
            lbarcode = Label_(pos_hint={"center_x": .2, "center_y": .3}, size_hint=[0.5,0.25],
                                  text=self.app.translation._('баркод') +' : '+ gitem['barcode'],color=self.app.color_gray, halign='center')
            lbarcode.id = 'barcode_'+gitem['barcode']
            lbarcode.bind(pos=lbarcode.on_texture_size, size=lbarcode.on_texture_size)
            main_cont.add_widget(lbarcode)

            # eд.изм.
            lei = Label_(pos_hint={"center_x": .4, "center_y": .3}, size_hint=[0.5,0.25],
                                  text=self.app.translation._('ед.изм.') +' : '+ gitem['ei'],color=self.app.color_gray, halign='center')
            lei.id = 'ei_'+gitem['barcode']
            lei.bind(pos=lei.on_texture_size, size=lei.on_texture_size)
            main_cont.add_widget(lei)

            # кухня.
            likitchen = Label_(pos_hint={"center_x": .6, "center_y": .3}, size_hint=[0.5,0.25],
                                  text=self.app.translation._('кухня') +' : '+ str(gitem['ikitchen']),color=self.app.color_gray, halign='center')
            likitchen.id='ikitchen_'+gitem['barcode']
            likitchen.bind(pos=likitchen.on_texture_size, size=likitchen.on_texture_size)
            main_cont.add_widget(likitchen)

            # цена
            lprice = Label_(pos_hint={"center_x": .9, "center_y": .8}, size_hint=[0.5,0.25],
                                  text=self.app.translation._('цена'),color=self.app.color_green, halign='center')
            lprice.id='lprice_'+gitem['barcode']
            lprice.bind(pos=lprice.on_texture_size, size=lprice.on_texture_size)
            main_cont.add_widget(lprice)

            eprice = Label_(pos_hint={"center_x": .9, "center_y": .4}, size_hint=[0.5,0.5],
                                  text=str(gitem['price1']),color=self.app.color_green, halign='center')
            eprice.id='eprice_'+gitem['barcode']
            eprice.bind(pos=eprice.on_texture_size, size=eprice.on_texture_size)
            main_cont.add_widget(eprice)

            # отображение товаров
            #but_tovar = PButton()
            #but_tovar.id = 'but_'+str(gitem['igruppa'])
            #but_tovar.ogruppa = gitem
            #but_tovar.pos_hint={"center_x": .925, "center_y": 0.5}
            #but_tovar.size_hint=[0.15,1]
            #but_tovar.text = '>'
            #but_tovar.source = './data/images/left_arrow_group.png'
            #main_cont.add_widget(but_tovar)


    # диалог выбора файла импорта
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


    # убираем диалог импорта
    def dismiss_popup(self):
        self._popup.dismiss()

    # загрузка файла
    def load(self, path, filename):
        #self.app = self.manager.parent.app
        try:
            f= open(filename[0],"r")
        except:
            pop = self.show_popup(self.app.translation._('Ошибка файла импорта'))
            return

        #ifiletype - 1-DBF, 2-CSV
        ifiletype = 0
        if (filename[0][-3:]).upper() == 'CSV': ifiletype = 3
        elif (filename[0][-3:]).upper != 'ZIP': ifiletype = 4
        else:
            f.close()
            pop = self.show_popup(self.app.translation._('Тип Файла должен быть CSV или DBF'))
            self._popup.dismiss()
            return
        f.close()
        self.fileimport(ifiletype=ifiletype,cpathfile=path,filename=filename)
        self._popup.dismiss()
        self.loadgrid()

    # импорт файла
    def fileimport(self, ifiletype, cpathfile, filename):
        #self.app = self.manager.parent.app
        oimport = tMenuImport()
        oimport.app = self.app
        oimport.ifilefrom = 4
        oimport.ifiletype = ifiletype
        oimport.cpathfile = cpathfile
        if not oimport.start():
            pop = self.show_popup(self.app.translation._(oimport.cerr))


    # диалог записи файла экспорта
    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    # запись файла
    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)
        self.dismiss_popup()

    def show_popup(self, cmsg):
        popup = Popup(title='Test popup',
            content=Label(text=cmsg),
            size_hint=(None, None), size=(300, 300))
        popup.open()