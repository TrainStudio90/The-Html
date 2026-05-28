import sqlite3

def openGDB(fpath):
    conn = sqlite3.connect(fpath)
    my_cursor = conn.cursor()
    return conn, my_cursor

def closeGDB(conn,cursor):
    cursor.close()
    conn.close()

def get_id(fpath,a,b):
    conn, my_cursor = openGDB(fpath)
    page = (a,b)
    task = '''SELECT id FROM users
                WHERE login == ?
                AND password == ?'''
    

# list
    my_cursor.execute(task,page)
    data = my_cursor.fetchone()

    closeGDB(conn,my_cursor)
    if data != None:
        return data[0]
    else:
        return data
# если не может выбрать одно значение то вот 




def clearGDB(fpath):

    
    conn, my_cursor = openGDB(fpath)
    task = '''DROP TABLE IF EXISTS users'''
    my_cursor.execute(task)
    task = '''DROP TABLE IF EXISTS writenbooks'''
    my_cursor.execute(task)
    
    
    
    conn.commit()
    closeGDB(conn,my_cursor)

def create_tables(fpath):
    conn, my_cursor = openGDB(fpath)

    task = '''PRAGMA foreign_keys = on'''
    my_cursor.execute(task)
    
    task = '''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                nickname TEXT,
                login TEXT UNIQUE,
                password TEXT,
                permissions TEXT)'''
    my_cursor.execute(task)
    conn.commit()


    task = '''CREATE TABLE IF NOT EXISTS writenbooks 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER,
                name TEXT, 
                story TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id))'''
    my_cursor.execute(task)
    conn.commit()


    task = '''CREATE TABLE IF NOT EXISTS goodbooks 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER,
                name TEXT, 
                story TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id))'''
    my_cursor.execute(task)
    conn.commit()

    
    closeGDB(conn,my_cursor)




def add_dummy(fpath):
    add_user(fpath,'CoolComposer15','None','None','Mc')
    add_book(fpath,get_id(fpath,'None','None'),'Книга','Это книга о машине, которая хотела начать писать музыку для людей.')
    # Mc ранг манекна - нет возможностей



def add_user(fpath,a,b,c,d):
    conn, my_cursor = openGDB(fpath)
# добавляем 1 манекен
    user= (a,b,c,d)
    task = '''INSERT INTO users (nickname,login,password,permissions) VALUES (?,?,?,?)'''
    
    try:
        my_cursor.execute(task,user)
        conn.commit()
        closeGDB(conn,my_cursor)
        return '+'
    except:
        return '-'

def add_book(fpath,a,b,c):
    conn, my_cursor = openGDB(fpath)
# добавляем 1 манекен
    book= (a,b,c)
    task = '''PRAGMA foreign_keys=on'''
    
    my_cursor.execute(task)
    conn.commit()
    task = '''INSERT INTO writenbooks (user_id, name, story) VALUES (?,?,?)'''
    
    my_cursor.execute(task,book)

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
        print('Ник:',box[1])
        print('Логин:',box[2])
        print('Пароль:',box[3])
        print('Ранг:',box[4])


def show_books(fpath):
    conn, my_cursor = openGDB(fpath)
    task = '''SELECT * FROM writenbooks'''
    my_cursor.execute(task)
    data = my_cursor.fetchall()

    closeGDB(conn,my_cursor)

    for box in data:
        print('🟩===================================================')
        print('ID:',box[0])
        print('ID пользователя:',box[1])
        print('Название:',box[2])
        print('Текст:',box[3])




        
def Vostok():
    if input('Очистить базу данных? (+/-): ')=='+':
        clearGDB('GDB.db')
    if input('Создать таблицы? (+/-): ')=='+':
        create_tables('GDB.db')
    if input('Создать манекен? (+/-): ')=='+':
        add_dummy('GDB.db')
    if input('🟩 Приступить к показу? (+/-): ')=='+':
        show_users('GDB.db')
        show_books('GDB.db')
    


def by_book_id(fpath,a,b):
    
    conn, my_cursor = openGDB(fpath)
    page = (b,)

    task = '''SELECT '''+a+''' FROM writenbooks
                WHERE id == ?
                '''
    
    my_cursor.execute(task,page)
    data = my_cursor.fetchone()

    closeGDB(conn,my_cursor)
    if data != None:
        return data[0]
    else:
        return data

def by_id(fpath,a,b):
    
    conn, my_cursor = openGDB(fpath)
    page = (b,)

    task = '''SELECT '''+a+''' FROM users
                WHERE id == ?
                '''
    
    my_cursor.execute(task,page)
    data = my_cursor.fetchone()

    closeGDB(conn,my_cursor)
    if data != None:
        return data[0]
    else:
        return data

# def find_books(fpath,a):
    
#     conn, my_cursor = openGDB(fpath)
#     page = (a,)

#     task = '''SELECT name FROM writenbooks
#                 WHERE user_id == ?
#                 '''
    
#     my_cursor.execute(task,page)
#     data = my_cursor.fetchall()

#     closeGDB(conn,my_cursor)

#     if data != None:
#         returnlist = list()
#         for i in data:
#             returnlist.append(i[0])
#         return returnlist
#     else:
#         return data

def find_books(fpath,a):
    
    conn, my_cursor = openGDB(fpath)
    page = (a,)

    task = '''SELECT id, name FROM writenbooks
                WHERE user_id == ?
                '''
    
    my_cursor.execute(task,page)
    data = my_cursor.fetchall()

    closeGDB(conn,my_cursor)

    return data[::-1]


def get_books_id(fpath):
    
    conn, my_cursor = openGDB(fpath)

    task = '''SELECT id FROM writenbooks'''
    
    my_cursor.execute(task)
    data = my_cursor.fetchall()

    closeGDB(conn,my_cursor)

    returnlist = list()
    for i in data:
        returnlist.append(i[0])
    return returnlist
    

def lastbook_id(fpath,a):
    
    conn, my_cursor = openGDB(fpath)

    task = '''SELECT id FROM writenbooks
                WHERE user_id == ?
                '''
    
    my_cursor.execute(task,(a,))
    data = my_cursor.fetchall()

    closeGDB(conn,my_cursor)

    
    return data[-1][0]

def pagemanager(fpath,page,mode):
    
    conn, my_cursor = openGDB(fpath)
    
    task = '''SELECT id, name FROM writenbooks
                '''
    
    my_cursor.execute(task)
    data = my_cursor.fetchall()

    closeGDB(conn,my_cursor)

    

    counting=0
    inhand=list()
    gotoscreen=list()
    data = data[::-1]
    
    for i in data:
        inhand.append(i)
        counting+=1
        if counting % 5 == 0:
            gotoscreen.append(inhand)
            inhand=list()
    if counting % 5 != 0:
            gotoscreen.append(inhand)
            inhand=list()

    
    print(gotoscreen)









    
    if mode == 'r':
        return gotoscreen[page-1]
    if mode == 'l':
        return len(gotoscreen)
    

































































































































































































































































































































































































































































































































































































































































































































































































































if __name__ == "__main__":
    Vostok()
