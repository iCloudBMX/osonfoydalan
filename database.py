import sqlite3

db_name = "user.db"

class DbHelper:
    def AddUser(self, telegram_id):
        conn = sqlite3.connect(db_name, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''insert into user (telegram_id, lastmessage)values(?, ?)''',(telegram_id,""))
        conn.commit()
        conn.close()
    
    def GetUser(self, telegram_id):
        conn = sqlite3.connect(db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        items = cursor.execute("select * from user where telegram_id='"+str(telegram_id)+"'").fetchall()
        conn.close()
        return items
    
    def GetLastMessage(self, telegram_id):
        conn = sqlite3.connect(db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        items = cursor.execute("select lastmessage from user where telegram_id='"+str(telegram_id)+"'").fetchall()
        conn.close()
        if len(items) > 0:
            return items[0]['lastmessage']
        return ""

    def UpdateUser(self, telegram_id, lastmessage):
        conn = sqlite3.connect(db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("update user set lastmessage='"+lastmessage+"' where telegram_id='"+str(telegram_id)+"'")
        conn.commit()
        conn.close()

    def GetAllDatas(self):
        conn = sqlite3.connect(db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        items = cursor.execute("select * from user").fetchall()
        conn.close()
        return items

    def UpdateRequest(self, telegram_id, result):
        conn = sqlite3.connect(db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("update user set request='"+str(result)+"' where telegram_id='"+str(telegram_id)+"'")
        conn.commit()
        conn.close()