import pymysql

# db = pymysql.connect(host='47.102.37.250', user='yzx', password='123456', database='mysql')
# cursor = db.cursor()
#
# cursor.execute("select version()")
#
# data = cursor.fetchone()
#
# print("data version: %s" % data)
#
# db.close()

class FaceSQl:
    def __init__(self):
        self.conn = pymysql.connect(  # 连接数据库
            host='47.102.37.250',
            user="yzx",
            password="123456",
            db="dyzhao",
            charset="utf8"
        )
        
    def processFaceData(self, sqlstr, args=()):  # 处理含参数的sql语句
        cursor = self.conn.cursor()
        try:
            cursor.execute(sqlstr, args)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
        finally:
            cursor.close()
        
    def saveFaceData(self, name, encoding_str):
        self.processFaceData("insert into face(name, encoding) values(%s,%s)", (name, encoding_str))
        
    def updateFaceData(self, name, encoding_str):
        self.processFaceData("update face set encoding = %s where name = %s", (encoding_str, name))
    
    def execute_float_sqlstr(self, sqlstr):  # 处理sql语句
        cursor = self.conn.cursor()
        results = []
        try:
            cursor.execute(sqlstr)
            results = cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            print(e)
        finally:
            cursor.close()
        return results
    
    def searchFaceData(self, name):  # 根据名字搜索数据
        return self.execute_float_sqlstr("select * from face where name="+name)
    
    def allFaceData(self):  # 遍历face表中所有数据
        return self.execute_float_sqlstr("select * from face ")
    