import sqlite3

def openGDB(fpath):
    conn = sqlite3.connect(fpath)
    my_cursor = conn.cursor()
    return conn, my_cursor

def closeGDB(conn,cursor):
    cursor.close()
    conn.close()

def clearGDB(fpath):

    
    conn, my_cursor = openGDB(fpath)
    task = '''DROP TABLE IF EXISTS users'''
    my_cursor.execute(task)
    task = '''DROP TABLE IF EXISTS posts'''
    my_cursor.execute(task)
    
    
    
    conn.commit()
    closeGDB(conn,my_cursor)

def create_tables(fpath):
    conn, my_cursor = openGDB(fpath)

    task = '''PRAGMA foreign_keys = on'''
    my_cursor.execute(task)
    
    task = '''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                lastname TEXT, 
                nickname TEXT,
                login TEXT,
                password TEXT,
                band TEXT, 
                permissions TEXT)'''
    my_cursor.execute(task)
                
    
    conn.commit()
    closeGDB(conn,my_cursor)

def add_user(fpath):
    conn, my_cursor = openGDB(fpath)
# добавляем 1 манекен
    dummy=  ('name','lastname','CoolComposer15','login','1234567890','band', 'Z')
    task = '''INSERT INTO users (name,lastname,nickname,login,password,band,permissions) VALUES (?,?,?,?,?,?,?)'''
    my_cursor.execute(task,dummy)



    conn.commit()



    closeGDB(conn,my_cursor)

def show_users(fpath):
    conn, my_cursor = openGDB(fpath)
    task = '''SELECT * FROM users'''
    my_cursor.execute(task)
    data = my_cursor.fetchall()

    closeGDB(conn,my_cursor)

    for box in data:
        print('🟩===================================================')
        print('ID:',box[0])
        print('Имя:',box[1])
        print('Фамилия:',box[2])
        print('Ник:',box[3])
        print('Логин:',box[4])
        print('Пароль:',box[5])
        print('Группа:',box[6])
        print('Ранг:',box[7])
        
def Vostok():
    if input('Очистить базу данных? (+/-): ')=='+':
        clearGDB('GDB.db')
    if input('Создать таблицы? (+/-): ')=='+':
        clearGDB('GDB.db')
    if input('Создать манекен? (+/-): ')=='+':
        add_user('GDB.db')
    if input('🟩 Приступить к показу? (+/-): ')=='+':
        clearGDB('GDB.db')
    

if __name__ == "__main__":
    Vostok()




    