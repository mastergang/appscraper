# -*- coding: utf-8 -*-
# coding: utf-8
import os 
os.environ["NLS_LANG"] = ".AL32UTF8"
import cx_Oracle

class DB:        
    def connect(self):
        try:
            self.db = cx_Oracle.connect('')
            print("Module Connect Success!")
        except cx_Oracle.DatabaseError as e:
            print("Module Connect fail..")
            error, = e.args
            if error.code == 1017:
                print('Please check your credentials.')
            else:
                print('Database connection error: %s'.format(e))
            raise

        self.cursor = self.db.cursor()

    def disconnect(self):
        try:
            self.cursor.close()
            self.db.close()
            print("Module close Success!")
        except cx_Oracle.DatabaseError:
            print("Module close fail..")
            pass

    def commit(self):
         self.db.commit()

    def execute(self, sql, commit=False):
        try:
            try:
                self.cursor.execute(sql)
            except:
                # db 환경 euc-kr => utf-8 변경
                os.environ["NLS_LANG"] = ".AL32UTF8"
                self.cursor.execute(sql)
                
        except cx_Oracle.DatabaseError as e:
            print("Module execute fail..")
            error, = e.args
            if error.code == 955:
                print('Table already exists')
            elif error.code == 1031:
                print("Insufficient privileges")
            print(error.code)
            print(error.message)
            print(error.context)
            raise

        if commit:
            self.db.commit()
        else:
            try:
                result = self.cursor.fetchall()
                return result
            except:
                self.cursor.execute(sql)
                self.db.commit()


