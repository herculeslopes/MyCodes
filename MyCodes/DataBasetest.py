import sqlite3

def ConnectToDB():
    global MyCodesDB, DB_Cursor
    MyCodesDB = sqlite3.connect('MyCodesDB.db')
    DB_Cursor = MyCodesDB.cursor()


def CloseConnection():
    MyCodesDB.commit()
    DB_Cursor.close()
    MyCodesDB.close()

ConnectToDB()

select = DB_Cursor.execute('''SELECT * FROM CodeList_2''')
Data = select.fetchall()

print(Data)

CloseConnection()