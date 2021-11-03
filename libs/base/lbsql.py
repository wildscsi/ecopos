__author__ = 'BM'
import psycopg2
import psycopg2.extensions
import sqlite3
import platform
import os as os

# Класс для работы Postgre SQL
class psql:
    def __init__(self):
        self.conn   = None
        self.cur    = None
        self.hsql   = False
        self.sqlstrconnect = ''
        self.errmsg = ''
        # Конвертируем Numeric(Decimal) в тип Float
        DEC2FLOAT = psycopg2.extensions.new_type( psycopg2.extensions.DECIMAL.values, \
        'DEC2FLOAT', lambda value, curs: float(value) if value is not None else None)
        psycopg2.extensions.register_type(DEC2FLOAT)

    # Переоткрытие соединения с SQL
    def reopen(self):
        self.close()
        return self.open(self.sqlstrconnect)

    # Открываем соединение с SQL
    def open(self,sqlstrconnect=''):
        self.errmsg = ''
        if len(sqlstrconnect) > 0:
            self.sqlstrconnect = sqlstrconnect
        if len(self.sqlstrconnect) == 0:
            self.errmsg = 'PSQL: Не определена строка подключения к SQL'
            return False
        try:
            if not self.hsql:
                self.conn = psycopg2.connect(self.sqlstrconnect)
                self.hsql = True
        except psycopg2.Error as e:
            self.errmsg = 'PSQL: Ошибка установки соединения\n' + '%s' %e
            self.hsql = False
        if self.hsql: self.conn.autocommit = True
        return self.hsql

    # Выполнение произвольного набора SQL команд
    def execute(self,sqlscript,lcommit=False,lcursorclose=False,cmsg='команд'):
        lret = True
        self.errmsg = ''
        if not self.hsql:
            if len(self.sqlstrconnect) == 0:
                self.errmsg = 'PSQL: Соединение не установлено.\nПараметры соединения не определены'; return False
            if not self.open(self.sqlstrconnect): return False
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sqlscript)
            # if lcommit: self.conn.commit()
            if lcursorclose: self.cur.close()
        except psycopg2.Error as e:
            self.errmsg = 'PSQL: Ошибка выполнения SQL ' + cmsg + '\n' + e.args[0] + ' Выражение: ' + sqlscript
            lret = False
        if not lret: self.close()
        return lret

    def execparam(self,sqlscript,param=None,cmsg='команд'):
        lret = True
        self.errmsg = ''
        if not self.hsql:
            if len(self.sqlstrconnect) == 0:
                self.errmsg = 'PSQL: Соединение не установлено.\nПараметры соединения не определены'; return False
            if not self.open(self.sqlstrconnect): return False
        try:
            self.cur = self.conn.cursor()
            if param is None:
                self.cur.execute(sqlscript)
            else:
                self.cur.execute(sqlscript,param)
        except psycopg2.Error as e:
            self.errmsg = 'PSQL: Ошибка выполнения SQL ' + cmsg + '\n' + e.args[0] + ' Выражение: ' + sqlscript
            lret = False
        if not lret: self.close()
        return lret

    def getresult(self):
        if self.cur is None: return []
        return dictfetchall(self.cur)

    # Предполагается выполнение команды Select
    def select(self,sqlscript,lcommit=False,lcursorclose=False):
        return self.execute(sqlscript,lcommit,lcursorclose,'команды SELECT')

    # Предполагается выполнение команды Insert
    def insert(self,sqlscript,lcommit=True,lcursorclose=True):
        return self.execute(sqlscript,lcommit,lcursorclose,'команды INSERT')

    # Предполагается выполнение команды Update
    def update(self,sqlscript,lcommit=True,lcursorclose=True):
        return self.execute(sqlscript,lcommit,lcursorclose,'команды UPDATE')

    # Предполагается выполнение команды Delete
    def delete(self,sqlscript,lcommit=True,lcursorclose=True):
        return self.execute(sqlscript,lcommit,lcursorclose,'команды DELETE')

    # Закрытие соединения
    def close(self):
        if not self.hsql: return True
        lret = True
        self.hsql = False
        try:
            if not self.cur is None: self.cur.close()
        except psycopg2.Error as e:
            if len(self.errmsg) > 0: self.errmsg += '\n'
            self.errmsg += 'PSQL: Ошибка команды CLOSE Cursor ' + '\n' + e.args[0]
            lret = False
        try:
            self.conn.close()
        except psycopg2.Error as e:
            if len(self.errmsg) > 0: self.errmsg += '\n'
            self.errmsg += 'PSQL: Ошибка команды CLOSE Connection ' + '\n' + e.args[0]
        if lret: self.hsql = False
        return lret

    def __del__(self):
        self.close()

# Класс для работы с SQLite
class qsql:
    def __init__(self):
        self.conn           = None
        self.cur            = None
        self.hsql           = False
        self.sqlstrconnect  = ''
        self.noclose        = False
        self.errmsg         = ''
        self.result         = None

    # Открываем класс для работы.
    # Метод может быть выполнен автоматически при выполнении execute
    def open(self,sqlstrconnect=''):
        self.errmsg = ''
        if len(sqlstrconnect) > 0:
            self.sqlstrconnect = sqlstrconnect
        if len(self.sqlstrconnect) == 0:
            self.errmsg = 'QSQL: Не определена строка подключения к SQL'
            return False
        try:
            if not self.hsql:
                self.conn = sqlite3.connect(self.sqlstrconnect,check_same_thread=False)
                self.hsql = True
        except sqlite3.Error as e:
            self.errmsg = 'QSQL: Ошибка установки соединения\n' + e.args[0]
            self.hsql = False
        # if self.hsql:
        #     self.execute('PRAGMA journal_mode=WAL;')
        return self.hsql

    #  Открывает работу с таблицами в памяти
    def openm(self):
        self.noclose = True
        try:
            if not self.hsql:
                self.conn = sqlite3.connect(":memory:", check_same_thread=False)
                self.hsql = True
        except sqlite3.Error as e:
            self.errmsg = 'QSQL: Ошибка открытия Memory\n' + e.args[0]
            self.hsql = False
        return self.hsql

    # Метод выполняет SQL команды
    # Если метод open не вызывался, то он будет вызван автоматически
    def execute(self,sqlscript,param=None,atr='RECORD'):
        self.errmsg = ''
        lret = True
        if not self.hsql:
            if len(self.sqlstrconnect) == 0:
                self.errmsg = 'QSQL: Соединение не установлено.\nПараметры соединения не определены'; return False
            if not self.open(self.sqlstrconnect): return False
        try:
            self.cur = self.conn.cursor()
            if param is None: self.cur.execute(sqlscript)
            else:
                atr = atr.upper()
                if atr == 'CURSOR': self.cur.executemany(sqlscript,param)
                else: self.cur.execute(sqlscript,param)
        except sqlite3.Error as e:
            self.errmsg = 'QSQL: Ошибка выполнения SQL команды.\n' + e.args[0] + '\nВыражение: ' + sqlscript
            lret = False
        if not lret:
            if not self.noclose: self.close(); print('CLOSE')
        return lret

    def getresult(self):
        if self.cur is None: return []
        return dictfetchall(self.cur)

    # Помещает словарь имен таблиц, входящих в открытую БД в свойство result
    def dbtables(self):
        self.result = []
        if not self.hsql: self.errmsg = 'БД не открыта'; return False
        ctxt = "SELECT " + "name AS tname FROM sqlite_master WHERE type='table';"
        if not self.execute(ctxt): return False
        self.result = self.getresult()
        return True

    # Проверка наличия таблицы
    def tblcheck(self,ctable=''):
        self.errmsg = ''
        ctable = ctable.strip(' ').lower()
        ctxt = "SELECT " + "name FROM sqlite_master WHERE type='table' AND name='" + ctable + "';"
        if not self.execute(ctxt): return -1
        allrec = self.getresult()
        if len(allrec) > 0: return 1
        return 0


    # Запись словаря на SQL
    def saverec(self,ctable,orec):
        cval = ''; cfld = ''; allrec = []
        for c1 in orec:
            allrec.append(orec[c1]); cval +=',?'; cfld += ',' + c1
        cval = cval[1:len(cval)]; cfld = cfld[1:len(cfld)]
        cscript = 'INSERT ' + 'INTO ' + ctable +' (' + cfld + ') VALUES (' + cval + ')'
        lret = self.execute(cscript,allrec,'RECORD')
        return lret

    # Применение сделанных изменений к БД
    # по умолчанию изменения не применяются сразу, так как при больших объемах
    # данных это значительно увеличивает продолжительность выполнения команд
    def commit(self):
        self.errmsg = ''
        lret = True
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            self.errmsg = 'QSQL: Ошибка выполнения команды COMMIT.\n' + e.args[0]
            lret = False
        return lret

    # Закрытие курсоров и соединений
    def close(self):
        if not self.hsql: return
        self.hsql = False
        try:
            if not self.cur is None: self.cur.close()
        except sqlite3.Error as e:
            pass
        try:
            self.conn.close()
        except sqlite3.Error as e:
            pass

    def __del__(self):
       self.close()

# Класс для работы с курсорами, размещаемыми в памяти, SQLite
class TQLTCursor:
    omem   = None
    errmsg = ''
    # Создание БД в памяти
    def open(self):
        self.close()
        self.omem = qsql()
        if not self.omem.openm():
            self.errmsg = self.omem.errmsg
            return False
        return True

    # Выполнение SQL команды
    def execute(self,sqlscript,param=None,atr='RECORD'):
        self.errmsg = ''
        if not self.omem.execute(sqlscript,param,atr):
            self.errmsg = self.omem.errmsg
            return False
        return True

    def getresult(self):
        if self.omem.cur is None: return []
        return dictfetchall(self.omem.cur)

    # Создание таблицы
    def tablecreate(self,ctable='',cstruct=''):
        ctable = ctable.strip(' ').lower()
        cstruct = cstruct.strip(' ')
        cscript = 'CREATE ' + 'TABLE ' + ctable + ' (' + cstruct + ')'
        self.errmsg = ''
        if not self.omem.execute(cscript):
            self.errmsg = self.omem.errmsg
            return False
        return True

    # Получить список всех временных таблиц
    def tablelist(self) -> dict:
        allrec = None
        self.errmsg = ''
        if self.omem.execute("SELECT " + "name FROM sqlite_master WHERE type='table'"):
            allrec = dictfetchall(self.omem.cur)
        else:
            self.errmsg = self.omem.errmsg
        return allrec

    # Очистка всех ранее созданных таблиц от данных
    def tableclear(self):
        self.errmsg = ''
        allrec = self.tablelist()
        if allrec is None: return False
        if len(allrec) == 0: return True
        lret = True
        for table in allrec:
            if not self.omem.execute('DELETE ' + 'FROM ' + table['name']):
                self.errmsg = self.omem.errmsg
                lret = False
                break
        return lret

    # Запись словаря на SQL
    def saverec(self,ctable,orec):
        self.errmsg = ''
        if not self.omem.saverec(ctable,orec):
            self.errmsg = self.omem.errmsg
            return False
        return True

    # Закрытие БД
    def close(self):
        if not self.omem is None:
            self.omem.close()

    # Деструктор класса
    def __del__(self):
        self.close()
        self.omem = None

# Определение класса
# для работы со структурами БД Postgre SQL
class dbpsql:
    port            = '5432'
    host            = ''
    password        = ''
    dbuser          = 'postgres'
    dbmaster        = 'postgres'
    dbname          = ''
    allrec          = None
    cfld            = ''
    osql            = None
    errmsg          = ''
    ctable          = ''
    cmethod         = ''

    # Открытие класса для работы
    def open(self):
        self.osql = psql()
        self.setsqlstrconnect()
        return True

    # Запись ошибок. Возвращает всегда False или vret
    def errbox(self,cmsg,vret=None):
        self.errmsg = cmsg
        if vret is None: vret = False
        return vret

    # Формирование новой строки подключений
    def setsqlstrconnect(self,ckey=''):
        self.ctable = ''; self.cmethod= ''
        if not self.osql.close():
            return self.errbox(self.osql.errmsg)
        self.password = self.password.strip(' ')
        self.host     = self.host.strip(' ')
        self.port     = self.port.strip(' ')
        self.dbuser   = self.dbuser.strip(' ')
        self.dbname   = self.dbname.strip(' ').lower()
        self.dbmaster = self.dbmaster.strip(' ').lower()
        if len(self.password) == 0: return self.errbox('DBSQL: Свойство PASSWORD не определено')
        if len(self.host) == 0:     return self.errbox('DBSQL: Свойство HOST не определено')
        if len(self.port) == 0:     return self.errbox('DBSQL: Свойство PORT не определено')
        if len(self.dbuser) == 0:   return self.errbox('DBSQL: Свойство DBUSER не определено')
        if len(self.dbname) == 0:   return self.errbox('DBSQL: Свойство DBNAME не определено')
        if len(self.dbmaster) == 0: return self.errbox('DBSQL: Свойство DBMASTER не определено')
        if ckey == 'M':
            ctxt  = 'port=' + self.port + ' dbname=' + self.dbmaster + ' '
            ctxt += 'user=' + self.dbuser + ' password=' + self.password + ' host=' + self.host
        else:
            ctxt  = 'port=' + self.port + ' dbname=' + self.dbname + ' '
            ctxt += 'user=' + self.dbuser + ' password=' + self.password + ' host=' + self.host
        self.osql.sqlstrconnect = ctxt
        return True

    # Закрывает работу и соединение с SQL
    def close(self):
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        if not self.osql is None:
            if not self.osql.close(): return self.errbox(self.osql.errmsg)

    def dbcheck(self):
        self.errmsg = ''
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        if not self.setsqlstrconnect('M'): return -1
        cscript = "SELECT " + "datname AS dname FROM pg_catalog.pg_database WHERE datname = '" + self.dbname + "';"
        if not self.osql.select(cscript): return self.errbox(self.osql.errmsg,-1)
        self.cfld = 'dname'
        self.allrec = dictfetchall(self.osql.cur)
        if not self.setsqlstrconnect(): return -1
        return len(self.allrec)

    def dbcreate(self,encoding='',lc_collate='',lc_type=''):
        if len(encoding) == 0: encoding = 'UTF8'
        if len(lc_collate) == 0:
            if platform.system() == "Windows": lc_collate = 'Russian, Russia'
            else: lc_collate = 'ru_RU.UTF-8'
        if len(lc_type) == 0:
            if platform.system() == "Windows": lc_type = 'Russian, Russia'
            else: lc_type = 'ru_RU.UTF-8'
        self.errmsg = ''
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        if not self.setsqlstrconnect('M'): return False
        iret = self.dbcheck()
        if iret > 0: return True
        if len(encoding)    == 0: encoding   = 'UTF8'
        if len(lc_collate)  == 0: lc_collate = 'Russian, Russia'
        if len(lc_type)     == 0: lc_type    = 'Russian, Russia'
        cscript  = "CREATE DATABASE " + self.dbname + " WITH OWNER = " + self.dbuser.strip(' ')
        cscript += " ENCODING = '" + encoding + "'"
        cscript += " TABLESPACE = pg_default LC_COLLATE = '" + lc_collate + "'"
        cscript += " LC_CTYPE = '" + lc_type + "'"
        cscript += " CONNECTION LIMIT = -1;"
        if not self.setsqlstrconnect('M'): return False
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        if not self.setsqlstrconnect(): return False
        return True

    def dbdelete(self):
        self.errmsg = ''
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        if not self.setsqlstrconnect('M'): return False
        iret = self.dbcheck()
        if   iret == -1: self.setsqlstrconnect(); self.osql.close(); return False
        elif iret ==  0: self.setsqlstrconnect(); self.osql.close(); return True
        cscript = "DROP DATABASE " + self.dbname
        if not self.setsqlstrconnect('M'): return False
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        if not self.setsqlstrconnect(): return False
        return True

    def dbtables(self):
        self.errmsg = ''
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        cscript  = "SELECT " + "relname AS tname FROM pg_catalog.pg_statio_user_tables"
        if not self.osql.execute(cscript):
            return self.errbox(self.osql.errmsg)
        self.cfld = 'tname'
        self.allrec = dictfetchall(self.osql.cur)
        return True

    def tblcheck(self,ctable=''):
        self.errmsg = ''
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        ctable = ctable.strip(' ').lower()
        if len(ctable) == 0: return self.errbox('Имя таблицы не определено',-1)
        cscript  = "SELECT " + "relname AS tname FROM pg_catalog.pg_statio_user_tables "
        cscript += "WHERE relname='" + ctable + "';"
        if not self.osql.execute(cscript):
            return self.errbox(self.osql.errmsg,-1)
        self.cfld = 'tname'
        self.allrec = dictfetchall(self.osql.cur)
        return len(self.allrec)

    def tblcreate(self,ctable='',ctext=''):
        self.errmsg = ''
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        ctable = ctable.strip(' ').lower()
        ctext  = ctext.strip(' ')
        if len(ctable) == 0: return self.errbox('Имя таблицы не определено')
        if len(ctext)  == 0: return self.errbox('Скрипт для создания таблицы не определен')
        iret = self.tblcheck(ctable)
        if   iret == -1: return False
        elif iret ==  1: return True
        cscript = "CREATE " + "TABLE " + ctable + " (" + ctext + ");"
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        return True

    def tbldelete(self,ctable=''):
        self.errmsg = ''
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        ctable = ctable.strip(' ').lower()
        if len(ctable) == 0: return self.errbox('Имя таблицы не определено')
        iret = self.tblcheck(ctable)
        if   iret == -1: return False
        elif iret ==  0: return True
        cscript = "DROP " + "TABLE " + ctable
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        return True

    def tblfields(self,ctable='',ldrop=False):
        self.errmsg = ''
        self.ctable = ''
        ctable = ctable.strip(' ').lower()
        if len(ctable) == 0: return self.errbox('Имя таблицы не определено')
        iret = self.tblcheck(ctable)
        if   iret == -1: return False
        elif iret ==  0: return self.errbox('Таблица ' + ctable.upper() + ' не существует')
        cscript = self.tblscrfields(ctable,ldrop)
        if not self.osql.execute(cscript):
            return self.errbox(self.osql.errmsg)
        self.cfld   = 'fname,ftype,attnotnull,atthasdef,attnum,fdefault'
        self.allrec = dictfetchall(self.osql.cur)
        self.ctable  = ctable
        self.cmethod = 'tblfields'
        return True

    def tblscrfields(self,ctable='',ldrop=False):
        self.errmsg = ''
        ctable = ctable.strip(' ').lower()
        # Если из скрипта убрать left(b.attname,4)<>'....', то можно получить плюс поля,
        # которые были удалены из таблицы
        cscript  = "SELECT a.oid,b.attrelid,b.attname AS fname,format_type(b.atttypid, b.atttypmod) AS ftype,"
        cscript += "b.attnotnull, b.atthasdef, b.attnum,COALESCE(c.adsrc,'') AS fdefault "
        cscript += "FROM pg_class a,pg_attribute b "
        cscript += "LEFT JOIN pg_attrdef c ON (b.attrelid = c.adrelid AND b.attnum = c.adnum) "
        cscript += "WHERE a.relname ='" + ctable + "' AND b.attnum > 0 AND b.attrelid = a.oid "
        if not ldrop: cscript += "AND left(b.attname,4)<>'....' "
        cscript += "ORDER BY b.attnum;"
        return cscript


    def chkfield(self,ctable='',cname=''):
        self.errmsg = ''; iret = 0
        ctable = ctable.strip(' ').lower()
        cname = cname.strip(' ').lower()
        if len(ctable) == 0: return self.errbox('Имя таблицы не определено',-1)
        if len(cname)  == 0: return self.errbox('Имя поля не определено',-1)
        if not ctable == self.ctable and self.cmethod == 'tblfields':
            if not self.tblfields(ctable): return -1
        if not type(self.allrec) is dict:
            if not self.tblfields(ctable): return -1
        for rec in self.allrec:
            ctxt = rec['fname'].strip(' ').lower()
            if ctxt == cname: iret = 1; break
        return iret

    def newfield(self,ctable='',ctext=''):
        self.errmsg = ''
        ctable = ctable.strip(' ').lower()
        ctext  = ctext.strip(' ')
        if len(ctable) == 0: return self.errbox('Имя таблицы не определено')
        if len(ctext)  == 0: return self.errbox('Скрипт создания поля не определен')
        pos = ctext.find(' ',0)
        cname = ctext[0:pos]
        iret = self.chkfield(ctable,cname)
        if   iret == -1: return False
        elif iret ==  1: return True
        cscript = "ALTER " + "TABLE " + ctable + " ADD " + ctext + ";"
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        return True

    def delfield(self,ctable='',cname=''):
        ctable = ctable.strip(' ').lower()
        cname = cname.strip(' ').lower()
        if len(ctable) == 0: return self.errbox('Имя таблицы не определено')
        if len(cname)  == 0: return self.errbox('Имя поля не определено')
        iret = self.chkfield(ctable,cname)
        if   iret == -1: return False
        elif iret ==  0: return True
        cscript = "ALTER " + "TABLE " + ctable + " DROP COLUMN " + cname
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        return True

    def chgfield(self,ctable='',cname='',cp1='',cp2='',cp3=''):
        self.errmsg = ''
        ctable = ctable.strip(' ').lower()
        cname  = cname.strip(' ').lower()
        cp1 = cp1.strip(' '); cp2 = cp2.strip(' '); cp3 = cp3.strip(' ')
        if len(ctable) == 0: return self.errbox('Имя таблицы не определено')
        if len(cname)  == 0: return self.errbox('Имя поля не определено')
        if len(cp1)+len(cp2)+len(cp3) == 0: return self.errbox('Не определены скрипты для выполнения')
        iret = self.chkfield(ctable,cname)
        if   iret == -1: return False
        elif iret ==  0: return self.errbox('Поле не существует')
        cscript = "ALTER " + "TABLE " + ctable + " ALTER COLUMN " + cname + " "
        if len(cp1) > 0: cp1 = cscript + cp1 + ";"
        if len(cp2) > 0: cp2 = cscript + cp2 + ";"
        if len(cp3) > 0: cp3 = cscript + cp3 + ";"
        cscript = cp1 + cp2 + cp3
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        return True

    def tblindexes(self):
        self.errmsg = ''
        self.ctable = ''; self.cmethod= ''; self.allrec = None
        # ctable = ctable.strip(' ').lower()
        # if len(ctable) == 0: return self.errbox('Имя таблицы не определено')
        # iret = self.tblcheck(ctable)
        # if   iret == -1: return False
        # elif iret ==  0: return self.errbox('Таблица не существует')
        cscript  = "SELECT "
        cscript += "U.usename AS user,ns.nspname AS schema,"
        cscript += "idx.indrelid :: REGCLASS AS tname,i.relname AS iname,"
        cscript += "idx.indisunique AS unique,idx.indisprimary AS primary_key,am.amname AS index_type,"
        cscript += "idx.indkey,ARRAY(SELECT pg_get_indexdef(idx.indexrelid, k + 1, TRUE) "
        cscript += "FROM generate_subscripts(idx.indkey, 1) AS k ORDER BY k) AS column_name,"
        cscript += "(idx.indexprs IS NOT NULL) OR (idx.indkey::int[] @> array[0]) AS is_functional,"
        cscript += "idx.indpred IS NOT NULL AS is_partial,false AS clustered "
        cscript += "FROM pg_index AS idx JOIN pg_class AS i ON i.oid = idx.indexrelid "
        cscript += "JOIN pg_am AS am ON i.relam = am.oid JOIN pg_namespace AS NS ON i.relnamespace = NS.OID "
        cscript += "JOIN pg_user AS U ON i.relowner = U.usesysid WHERE NOT nspname LIKE 'pg%'"
        # cscript += " AND indrelid :: REGCLASS :: text = '" + ctable + "';"
        if not self.osql.execute(cscript):
            return self.errbox(self.osql.errmsg)
        self.cfld   = 'tname,iname,column_name,primary_key,unique,index_type,'
        self.cfld  += 'clustered,is_partial,is_functional,user,schema,indkey'
        self.allrec = dictfetchall(self.osql.cur)
        self.ctable  = 'index'
        self.cmethod = 'tblindexes'
        return True

    def chkindex(self,cname=''):
        self.errmsg = ''
        cname  = cname.strip(' ').lower()
        iret   = 0
        if len(cname)  == 0: return self.errbox('Имя индекса не определено')
        if not self.ctable == 'index' and self.cmethod == 'tblindexes':
            if not self.tblindexes(): return -1
        if not type(self.allrec) is dict:
            if not self.tblindexes(): return -1
        for rec in self.allrec:
            if rec['iname'] == cname: iret = 1; break
        return iret

    def newindex(self,ctable='',colname='',cname=''):
        self.errmsg = ''
        ctable = ctable.strip(' ').lower()
        colname = colname.strip(' ').lower()
        cname = cname.strip(' ').lower()
        if len(ctable)  == 0: return self.errbox('Имя таблицы не определено')
        if len(colname) == 0: return self.errbox('Не определен список колонок для индексирования')
        if len(cname)   == 0: return self.errbox('Имя индекса не определено')
        iret = self.chkindex(cname)
        if   iret == -1: return False
        elif iret ==  1: return True
        cscript = "CREATE " + "INDEX " + cname + " ON " + ctable + "(" + colname + ");"
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        return True

    def delindex(self,cname=''):
        self.errmsg = ''
        cname = cname.strip(' ').lower()
        if len(cname)   == 0: return self.errbox('Имя индекса не определено')
        iret = self.chkindex(cname)
        if   iret == -1: return False
        elif iret ==  0: return True
        cscript = "DROP " + "INDEX " + cname + ";"
        if not self.osql.execute(cscript,True,True):
            return self.errbox(self.osql.errmsg)
        return True

    def chkfunc(self,cfunc=''):
        self.errmsg = ''
        cfunc = cfunc.strip(' ').lower()
        if len(cfunc) == 0:
            return self.errbox('Имя функции не определено',-1)
        ctxt  = "SELECT "
        ctxt += "p.proname AS pname,pg_catalog.pg_get_function_identity_arguments(p.oid) AS params "
        ctxt += "FROM   pg_catalog.pg_proc p "
        ctxt += "JOIN   pg_catalog.pg_namespace n ON n.oid = p.pronamespace "
        ctxt += "WHERE  n.nspname = 'public' AND p.proname='" + cfunc + "' "
        ctxt += "ORDER  BY 1;"
        if not self.osql.execute(ctxt):
            return self.errbox(self.osql.errmsg,-1)
        self.allrec = self.osql.getresult()
        return len(self.allrec)

    def delfunc(self,cfunc=''):
        self.errmsg = ''
        cfunc = cfunc.strip(' ').lower()
        if len(cfunc) == 0:
            return self.errbox('Имя функции не определено')
        iret  = self.chkfunc(cfunc)
        if iret > 0:
            ctxt = ""
            for orec in self.allrec:
                ctxt += "DROP FUNCTION " + orec['pname'] + "(" + orec['params'] + ");"
            if not self.osql.execute(ctxt):
                return self.errbox(self.osql.errmsg)
        return True


# Класс чтения структур таблиц с диска
class ReadStrSQL:
    errmsg = ''         # Текст ошибки
    tblsrc = None       # Словарь скриптов создания таблиц и процедур
    tbllst = None       # Список таблиц в порядке их определения в файле
    kob    = 10         # Код объекта по умолчанию
    fname  = ''         # Имя файла, хранящего описание структ таблиц и процедур
    cp     = 'utf-8'    # Кодовая страница файла
    odbsql = None       # Ссылка на объект создания БД PostgreSQL
    def readstrsql(self):
        self.fname = self.fname.strip(' ')
        if len(self.fname) == 0:
            return self.errbox('Имя файла не определено')
        if not os.path.isfile(self.fname):
            return self.errbox('Файл ' + self.fname.upper() + ' не найден')
        cmsg = ''; han = ''
        try:
            han = open(self.fname,'r',encoding=self.cp)
        except Exception as e:
            cmsg = '%s' %e
        if len(cmsg) > 0:
            return self.errbox('Ошибка чтения файла ' + self.fname.upper() + '\n' + cmsg)
        ctable = ''
        cid = str(self.kob)
        self.tblsrc = dict()
        self.tbllst = list()
        for line in han:
            line = line.replace('\n','')
            line = line.replace('\t','')
            if len(line) == 0: continue
            ch = line[0:1]
            if ch in ['-','*']: continue
            if ch == '.':
            # Конец определения строк таблицы
                ctable = ""
                continue
            if ch == ':':
            # Объявление таблицы, процедуры, скрипта изменений
                ctable = line[1:].strip(' ').upper()
                self.tbllst.append(ctable)
                self.tblsrc[ctable] = ""
                continue
            if len(ctable) == 0: continue
            ipos = line.find('<')
            if ipos > -1: line = line[0:ipos] + cid + ','
            self.tblsrc[ctable] += line
        han.close()
        return True

    def dbcreate(self):
        if self.odbsql is None:
            return self.errbox('Объект ODBSQL не определен')
        if not self.readstrsql(): return False
        # Формируем скрит создания таблиц
        ctxt = ""
        for ctable in self.tbllst:
            if not len(self.tblsrc[ctable]) > 0: continue
            ctbl = ctable.replace(' ','').split('=')
            if ctbl[0][0:5] == 'TABLE':
                if not self.odbsql.tblcheck(ctbl[1]):
                    ctxt += self.tblsrc[ctable]
            elif ctbl[0][0:4] == 'PROC':
                ctxt += self.tblsrc[ctable]
        # print(self.tbllst)
        # print(ctxt)
        if len(ctxt) > 0:
            if not self.odbsql.osql.execute(ctxt):
                return self.errbox(self.odbsql.osql.errmsg)
        return True

    def errbox(self,cmsg):
        self.errmsg = "ERROR READSTRSQL: " + cmsg
        return False

# Возвращает все строки запроса в виде словаря данных
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

