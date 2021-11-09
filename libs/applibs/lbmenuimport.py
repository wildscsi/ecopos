__author__ = 'BM'
# -*- coding: utf-8 -*-

import os
from ftplib import FTP
from libs.applibs.vfunc import unzip, DeleteFileDir
import dbf, csv, shutil
from kivymd.app import MDApp
from copy import deepcopy
from smb.SMBConnection import SMBConnection

# класс импорта меню в DBF и CSV форматах, с FTP, SAMBA, WEB
# ifiletype - 1-DBF, 2-CSV
# ifilefrom 1-FTP, 2-samba, 4-File

class tMenuImport:

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)
        # читаем настройки
        self.cpath = 'temp/'     # директорий импорта
        self.cpathfile = ''     # директорий при импорте из файлов
        self.cerr = ''          # ошибка
        self.kob = 0            # объект для которого импортируем меню
        self.listfile = ''      # перечень файлов импорта
        self.ldel = False       # удаление файлов после успешного импорта
        self.listimp = []       # перечень заданий для принятия
        self.lmanual=True       # True - ручной приём
        self.listfile=[]        # перечень файлов импорта
        self.codepage = 'UTF-8' # кодировка файла
        self.delimiter=';'      # делимитер
        self.aftertovar = []    # предыдущее меню
        self.notovar = []       # неактуальные блюда
        self.otConf = None      # объект настроек приложения
        self.ifiletype = ''     #тип импортируемых файлов
        self.ifilefrom = 4      # 1-FTP, 2-samba, 4-File
        self.app = None

    # настройки
    def setvalue(self):
        # ручной и автоматический приём
        if self.lmanual: self.ldel=False
        # проверяем, существует ли директорий импорта, создаём при отсутствии, очищаем
        if os.path.isdir(os.getcwd()+self.cpath):
            # чистим директорий
            DeleteFileDir(os.getcwd()+self.cpath)
        else:
            # создаём директорий
            os.mkdir(os.getcwd()+self.cpath)


    # основной метод
    def start(self):
        #установка настроек
        self.setvalue()
        return  self.importrec()

    # проверки и импорт
    def importrec(self):
        # массив импортируемых файлов и кодовая страница файла
        if self.ifiletype == 1:
            self.listfile = ['sqlzip.zip','sqlzip.web','sqlzip.key','sqlzip.now']
            self.codepage = 'CP1251'
        if self.ifiletype == 2 or self.ifiletype == 3:
            self.listfile = ['GOODS.CSV','PRICE.CSV']
            self.codepage = 'UTF-8'
        if self.ifiletype == 4:
            self.listfile = ['sqlzip.zip']


        # копируем файлы
        if self.ifilefrom == 1:
            # приём с FTP
            if not self.ftpimport():return False
        if self.ifilefrom == 2:
            # приём с директория SAMBA
            if not self.sambaimport(): return False
        if self.ifilefrom == 3:
            # приём с браузера, файл уже переписан
            pass
        if self.ifilefrom == 4:
            # приём из файловой системы
            if not self.fileimport(): return False


        ctxt = "SELECT " + "name FROM sqlite_master WHERE type='table' AND name='tovar';"
        if not self.app.osql.execute(ctxt): return False
        self.aftertovar = self.app.osql.getresult()
        # импортируем файлы
        lret = True
        if self.ifiletype == 1 or self.ifiletype == 4:
            # DBF
            if not self.dbfimport(): lret=False
        if self.ifiletype == 2:
            # CSV guscom
            if not self.csvimpguscom(): lret=False
        if self.ifiletype == 3:
            # CSV iiko
            if not self.csvimpiiko(): lret=False
        if not lret:
            # восстанавливаем группы и блюда
            return False

        return True

    # импорт файла с FTP
    def ftpimport(self):
        try:
            ftp = FTP(host=self.importitem['ftpserver'],user=self.importitem['ftpuser'],passwd=self.importitem['ftpimportpassword'])
        except:
            self.cerr = 'Не возможно соединиться с FTP сервером ' + self.importitem['ftpserver']; return False

        # переходим в директорий
        try:
            ftp.cwd(self.importitem['ftpdir'])
        except:
            self.cerr = 'Не существует директория '+ self.importitem['ftpimportdir'] + ' на FTP сервере ' + self.importitem['ftpserver']; return False

        # удаляем все файлы из директория загрузки
        self.clsdir()

        # получаем массив файлов
        ftpfilelist = []
        try:
            ftp.dir(ftpfilelist.append)
        except:
            self.cerr = 'Ощибка получения списка файлов директория '+ self.importitem['ftpdir'] + ' на FTP сервере ' + self.importitem['ftpserver']; return False
        for clist in ftpfilelist:
            cfile = clist.split(None, 8)
            cfile = cfile[len(cfile)-1]
            if cfile in self.listfile:
                # переписываем на WEB
                try:
                    local_filename = os.path.join(self.cpath, cfile)
                    lf = open(local_filename, "wb")
                    ftp.retrbinary("RETR " + cfile, lf.write, 8*1024)
                    lf.close()
                except:
                    self.cerr = 'Ощибка записи файла ' + cfile + ' с FTP директория '+ self.importitem['ftpdir'] + ' на FTP сервере ' + self.importitem['ftpserver']; return False
        ftp.close()
        return True

    # импорт файла из директория
    def sambaimport(self):
        self.clsdir()
        # установка соединения
        userID = self.importitem['sambauser']
        password = self.importitem['sambapassword']
        client_machine_name = 'localpcname'
        server_name = self.importitem['sambaserver']
        server_ip = self.importitem['sambaip']
        remotepath = self.importitem['sambadir']
        domain_name = ''

        try:
            conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                     is_direct_tcp=True)
            conn.connect(server_ip, 445)
        except Exception as e:
            self.cerr= "Невозможно установить соединение с удалённым директорием: " + e.strerror
            return False

        # ищем необходимые файлы
        shares = conn.listShares()      # перечень всех шар на сервере

        for share in shares:
            if share.name == remotepath:
                if not share.isSpecial and share.name not in ['NETLOGON', 'SYSVOL']:
                    sharedfiles = conn.listPath(share.name, '/')
                    ifile=0
                    for sharedfile in sharedfiles:
                        if (sharedfile.filename).upper() in self.listfile: ifile += 1
                    if ifile == 0:
                        self.cerr = 'Нет файлов импорта в удалённом директории'; return False
                    if ifile != len(self.listfile):
                        self.cerr = 'Не все файлы импорта есть в удалённом директории'; return False

        # копируем файлы в директорию
        try:
            for item in self.listfile:
                file_obj = open(self.cpath + item, 'wb')
                file_attributes, filesize = conn.retrieveFile(remotepath, item, file_obj)
                file_obj.close()
        except:
            self.cerr = 'Ошибка копирования файлов импорта из удалённого директория'; return False

        return True

    #копируем файлы в директорий приёма файла из файловой системы
    def fileimport(self):
        try:
            for item in self.listfile:
                shutil.copyfile(self.cpathfile+'/'+ item, os.getcwd()+self.cpath+item)
        except:
            self.cerr = 'Error copy filles to temp dir'
            return False
        return True

    # импорт файлов из DBF
    def dbfimport(self):
        # проверяем наличие файлов
        cfile = os.listdir(os.getcwd()+self.cpath)[0]
        if cfile not in self.listfile:
            self.cerr = 'Not find CSV file. Import canceled'; return False

        # разархивируем
        if not unzip(os.getcwd()+self.cpath, os.getcwd()+self.cpath+'sqlzip.zip'):
            self.cerr = 'Error unzip file sqlzip.zip'; return False


        # удаляем все записи меню
        if not self.app.osql.delete('gruppa','kob=' + str(self.app.kob)):
            self.cerr = 'Error delete all rows in table Gruppa. Import canceled'; return False
        if not self.app.osql.delete('tovar','kob=' + str(self.app.kob)):
            self.cerr = 'Error delete all rows in table Tovar. Import canceled'; return False

        # открываем DBF-файлы
        try:
            cgruppa = dbf.Table(os.getcwd()+self.cpath+'GRUPPA.DBF')
            ctovar = dbf.Table(os.getcwd()+self.cpath+'TOVAR.DBF')
            cgruppa.open(); ctovar.open()
        except:
            self.cerr = 'Error open import table GRUPPA И TOVAR. Import canceled'; return False

        for grec in cgruppa:
            lf = 0
            if grec.lf: lf = 1
            rec = {'kob':int(self.app.kob),
                    'gname': (grec.gname).strip(),
                    'bname': (grec.bname).strip(),
                    'idnt':   '',
                    #'idnt':  (grec.idnt).strip(),
                    'lf':    lf,
                    'code' : (grec.code).strip() }

            if not self.app.osql.insert('gruppa',rec):
                self.cerr = 'Error insert data to table Gruppa. Import canceled'; return False

            for trec in ctovar:
                if grec.igruppa == trec.igruppa:
                    xrec = dict()
                    ltop=0; lf=0; lf1=0; lf2=0; lf3=0; lf4=0
                    if trec.ltop: ltop = 1
                    if trec.lf: lf = 1
                    if trec.lf1: lf1 = 1
                    if trec.lf2: lf2 = 1
                    if trec.lf3: lf3 = 1
                    if trec.lf4: lf4 = 1
                    irec = {'kob': int(self.app.kob),
                            'tname': (trec.tname).strip(),
                            'bname': (trec.bname).strip(),
                            'cr': float(trec.cr),
                            'barcode': (trec.barcode).strip(),
                            'code': (trec.code).strip(),
                            'igruppa': int((trec.code).strip()),
                            'price1': trec.price1,
                            'price2': trec.price2,
                            'price3': trec.price3,
                            'price4': trec.price4,
                            'ikitchen': trec.ikitchen,
                            'lf': lf,
                            'lf1': lf1,
                            'lf2': lf2,
                            'lf3': lf3,
                            'lf4': lf4,
                            'dsc1': trec.dsc1,
                            'dsc2': trec.dsc2,
                            'dsc3': trec.dsc3,
                            'dsc4': trec.dsc4,
                            'ikd': trec.ikd,
                            'ei':trec.ei,
                            'department': trec.department,
                            'ltop': ltop}
                    if not self.app.osql.insert('tovar',irec):
                        self.cerr = 'Error insert data to table Tovar. Import canceled'; return False
            self.app.osql.commit()
        return True

    # импорт из CSV guscom
    def csvimpguscom(self):
        # у нас два файла импорта - обдин перзапись меню, второй только обновление цен

        # проверяем наличие файлов
        cfile = os.listdir(os.getcwd()+self.cpath)[0]
        if cfile not in self.listfile:
            self.cerr = 'Отсутствует файл CSV. Импорт отменён'; return False
        # открываем CSV-файл
        try:
            data = open(self.cpath + cfile, "r", encoding='CP1251')
            #encoding='utf-8'
        except:
            self.cerr = 'Не возможно открыть файл CSV. Импорт отменён'; return False

        # формируем из CSV - LIST
        reader = csv.reader(data, delimiter=";")
        result = []
        i = 0; shapka = None
        for row in reader:
            if i == 0:
                shapka = row; i +=1; continue
            dictrow = {}
            j = 0
            for ch in shapka:
                dictrow.update({ch:row[j]})
                j+=1
            result.append(dictrow)
            i +=1

        if len(result) == 0:
            self.cerr = 'Файл CSV с меню пуст. Импорт отменён'; return False
        # полная перезапись меню
        if cfile == 'GOODS.CSV':

            # удаляем все записи меню
            gruppa.objects.all().filter(kob=self.kob).delete()
            tovar.objects.all().filter(kob=self.kob).delete()

            # делаем list с группами, дописываем
            lgruppa = []
            for rec in result:
                if rec['TYPE'] == 'GROUP' and rec['INCLUDED_IN_MENU'] == '1' :
                    rec.update({'LIST':[]})
                    lgruppa.append(rec)

            # формируем LIST - группа(последняя) - блюда
            for trec in result:
                # ищем активное блюдо
                if trec['TYPE'] == 'DISH' and trec['INCLUDED_IN_MENU'] == '1':
                    #записываем его в парент группу
                    for grec in lgruppa:
                        if grec['NUM'] == trec['PARENT_CODE']:
                            grec['LIST'].append(trec)
                            continue

            #узнаём длину полей для округлегия gname, tname
            for cash in tovar._meta.fields:
                if cash.name == 'tname':
                    tokr = cash.max_length
            for cash in gruppa._meta.fields:
                if cash.name == 'gname':
                    gokr = cash.max_length

            #перебираем группу и пишем в SQL
            for grec in lgruppa:
                if len(grec['LIST']) != 0:
                    rec = {'kob':self.kob,
                    'gname':((grec.get('NAME')).replace("'",'"'))[0:gokr],
                    'bname':((grec.get('NAME')).replace("'",'"'))[0:gokr],
                    'idnt': (grec.get('NUM'))[0:gokr],
                    'code' : grec.get('NUM') }
                    ogruppa = gruppa.objects.create(**rec)
                    id = ogruppa.igruppa
                    for trec in grec['LIST']:
                        xrec = dict()
                        irec = {'kob':self.kob,
                            'tname': ((trec.get('NAME')).replace("'",'"'))[0:tokr],
                            'bname': ((trec.get('NAME')).replace("'",'"'))[0:tokr],
                            'cr': float(trec.get('PRICE')),
                            'barcode': trec.get('NUM'),
                            'code': trec.get('NUM'),
                            'price1': float(trec.get('PRICE')),
                            'price2': float(trec.get('PRICE')),
                            'price3': float(trec.get('PRICE')),
                            'price4': float(trec.get('PRICE')),
                            'ikitchen': self.getkitchenid(trec.get('COOKING_PLACE_TYPE')),
                            'ei':(trec.get('MEASURE_UNIT')).replace("'",'"')}
                        tovar.objects.create(igruppa_id=id, **irec)

                        # заполняем XTOVAR
                        recept = (trec.get('CONCEPTION')).replace("'",'"')
                        info = (trec.get('CONCEPTION')).replace("'",'"')
                        if len(recept): xrec.update({'recept':recept})
                        if len(info): xrec.update({'info':info})

                        # если в XTOVAR запись существует -обновляем, если нет добавляем
                        if len(xrec) >0:
                            xrec.update({'kob':self.kob,'us':3,'barcode':irec['barcode']})
                            ix = xtovar.objects.filter(kob=self.kob).filter(us=3).filter(barcode=irec['barcode'])
                            if len(ix) == 0:
                                # новая строчка
                                xtovar.objects.create(**xrec)
                            else:
                                # обновление
                                xrec.update({'kob':self.kob,'us':3,'barcode':irec['barcode']})
                                xtovar.objects.filter(kob=self.kob).filter(us=3).filter(barcode=irec['barcode']).update(**xrec)

        else:
            self.cerr = 'Файл CSV должен быть GOODS.CSV'; return False
        return True

    # импорт из CSV iiko
    def csvimpiiko(self):
        # у нас два файла импорта - один перзапись меню, второй только обновление цен
        # проверяем наличие файлов
        ldirfile = os.listdir(os.getcwd()+self.cpath)
        if self.lmanual:
            # ручной импорт меню
            lret = False
            self.listfile = []
            for idir in ldirfile:
                if idir in ['GOODS.CSV','PRICE.CSV']:
                    lret = True
                    self.listfile.append(idir)
            if not lret:
                self.cerr = 'отсутствуют файлы импорта. Импорт отменён'; return False

        else:
            # импорт из директория или FTP
            if 'GOODS.CSV' not in ldirfile:
                self.cerr = 'Отсутствует файл GOODS.CSV. Импорт отменён'; return False
            if 'PRICE.CSV' not in ldirfile:
                self.cerr = 'Отсутствует файл PRICE.CSV. Импорт отменён'; return False

        # импортируем GOODS.CSV
        if 'GOODS.CSV' in  self.listfile:
            try:
                data = open(os.getcwd()+self.cpath + 'GOODS.CSV', "r", encoding=self.codepage)
            except:
                self.cerr = 'Error open file GOODS.CSV. Import canceled'; return False
            # парсинг
            try:
                reader = csv.reader(data, delimiter=self.delimiter)
            except:
                self.cerr = 'Error parced file GOODS.CSV. Import canceled'; return False

            # формируем из CSV - LIST c группами и товарами
            lgruppa = []; ltovar = []

            try:
                for row in reader:
                    # формируем листы с группами и строками
                    if row[0] in ['Группа','GROUP']:
                        lgruppa.append({'code':row[1],'idnt':row[2],'gname':row[3][0:79],'bname':row[3][0:39],'lf':1,'kob':self.app.kob})
                    elif row[0] in ['Блюдо','DISH']:
                        if row[6] == 'Кухня': department = 2
                        else: department = 1
                        if row[7] == 'Кухня': ikitchen = 1
                        else: ikitchen = 0
                        ltovar.append({'barcode':row[1], 'code':row[2],'tname':row[3][0:79],'bname':row[3][0:39], 'ei':row[4],'status':row[5],
                                        'department':department,'ikitchen':ikitchen,'lf':1,'kob':self.app.kob})
                    else: continue
            except:
                self.cerr = 'Error format file GOODS.CSV. Import canceled'; return False


            if len(lgruppa) == 0 and len(ltovar) == 0:
                self.cerr = 'No Item in file GOODS.CSV. Import canceled'; return False

            # полная перезапись меню
            # удаляем все записи меню
            if not self.app.osql.delete('gruppa','kob=' + str(self.app.kob)):
                self.cerr = 'Error delete all rows in table Gruppa. Import canceled'; return False
            if not self.app.osql.delete('tovar','kob=' + str(self.app.kob)):
                self.cerr = 'Error delete all rows in table Tovar. Import canceled'; return False
            #self.app.osql.commit()

            #перебираем группы и пишем в SQL
            for grec in lgruppa:
                if not self.app.osql.insert('gruppa',grec):
                    self.cerr = 'Error insert data to table Gruppa. Import canceled'; return False

                for trec in ltovar:
                    if grec['code'] == trec['code']:
                        if not self.app.osql.insert('tovar',trec):
                            self.cerr = 'Error insert data to table Tovar. Import canceled'; return False

            self.app.osql.commit()

        # импортируем PrIcE.CSV - обновление цен
        if 'PRICE.CSV' in  self.listfile:
            try:
                data = open(os.getcwd()+self.cpath + 'PRICE.CSV', "r", encoding=self.codepage)
            except:
                self.cerr = 'Error open file GOODS.CSV. Import canceled'; return False
            # парсинг
            try:
                reader = csv.reader(data, delimiter=self.delimiter)
            except:
                self.cerr = 'Error parced file PRICE.CSV. Import canceled'; return False

            # формируем из CSV - LIST c товарами
            ltovar = []
            for row in reader:
                if row[0] in ['Блюдо','DISH']:
                    ltovar.append({'barcode':row[1], 'code':row[2],'tname':row[3][0:79],'bname':row[3][0:39], 'ei':row[4],'price1':float((row[5]).replace(',','.')),
                                    'price2':float((row[5]).replace(',','.')),'price3':float((row[5]).replace(',','.')),'price4':float((row[5]).replace(',','.')),'lf':int(row[6]),'kob':self.app.kob})
                else: continue

            if len(ltovar)==0:
                self.cerr = 'Empty file PRICE.CSV. Import canceled'; return False

            # обновляем цены
            for item in ltovar:
                if not self.app.osql.update('tovar',item,'kob ='+ str(self.app.kob)+' and '+'barcode="'+item['barcode']+'"'):
                    self.cerr = 'Error update data to table Tovar. Import canceled'; return False
            self.app.osql.commit()
        return True




    # проверяем наличие файлов в локальном директории для импорта
    def chfile(self):
        # приём с монтрированного диска или FTP, DBF - файлов должны быть все файлы
        locallist = os.listdir(self.cpath)
        for cfile in self.listfile:
            if cfile not in locallist:
                self.cerr = 'Отсутствует файл ' + cfile + '. Импорт отменён'; return False
        return True

    # удаляем все файлы из директория загрузки
    def clsdir(self):
        files = os.listdir(self.cpath)
        if len(files) > 1:
            for f in files:
                os.remove(self.cpath+f)


