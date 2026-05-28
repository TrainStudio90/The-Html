from flask import Flask, redirect, url_for, session, request, render_template
import os
from GDB_commands import add_user, add_dummy,get_id,by_id,find_books,add_book, get_books_id,lastbook_id,by_book_id,pagemanager












def postbook():
    add_book('GDB.db',session['gid'],session['curname'],session['curstory'])
    session['curname']= None
    session['curstory']= None



    book_id = lastbook_id('GDB.db',session['gid'])
    


    return redirect(url_for('account'))

    
def backfrombook():

    return redirect(url_for('vlibrary'))

def openbook(book_id):
    nm = by_book_id('GDB.db','name',book_id)
    st = by_book_id('GDB.db','story',book_id)
    return render_template('OpenBook.html',Gname=nm,Gtext=st)
   





def NXT():
    if session['page']<pagemanager('GDB.db',session['page'],'l'):
        session['page']+=1
    return redirect(url_for('vlibrary'))


def BCK():
    if session['page']>0:
        session['page']-=1
    return redirect(url_for('vlibrary'))


def vlibrary():
    WebSheild()
    
    return render_template('VLibrary.html',Gbooks = pagemanager('GDB.db',session['page'],'r'))


def index():
    

    if 'tag' not in session or 'logtag' not in session:
        session['tag'] = ''
        session['logtag'] = ''
        session['gnm'] = ''
        session['glg'] = ''
        session['gpw'] = ''
        session['grepw'] = ''
        session['gid'] = ''
        session['curname'] = ''
        session['curstory'] = ''
        session['doorto'] = '/'
        session['page']= 1 

    

    return render_template('Login.html',Gtag = session['logtag'],Glogin=session['glg'],Gpassword=session['gpw'])
    # return render_template('CreateBook.html')
def createacc():
    WebSheild()
    return render_template('CreateAccount.html',Gname = session['gnm'],Glogin=session['glg'],Gpassword=session['gpw'],Grepassword=session['grepw'],Gtag = session['tag'])
def checkreg():
    abc='qwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъфывапролджэячсмитьбю'
    notabc='1234567890'

    if request.method == "POST":
        Itsnorm = True
        nm = request.form.get('Name')
        lg = request.form.get('Login')
        pw = request.form.get('PassW')
        repw = request.form.get('RePassW') 
        if nm=='' or lg=='' or pw== '' or repw=='':
            Itsnorm = False
            session['tag'] = 'Введите все данные'
        elif pw!= repw:
            Itsnorm = False
            session['tag'] = 'Пароль не подтверждён'
        else:
            Itsnorm = False
            aa=False
            bb=False
            cc=False
            for i in pw:
                if i.lower() in abc:
                    aa = True
                elif i in notabc:
                    bb = True
                else:
                    cc = True
            if aa==bb and aa==True and cc==False:
                Itsnorm=True
            else: 
                session['tag'] = 'Пароль должен содержать и буквы и цифры'

        if Itsnorm:
            
            if add_user('GDB.db',nm,lg,pw,'Z')=='-':
                session['tag'] = 'Этот логин занят'
                Itsnorm = False
                        


                
        if Itsnorm:
            session['tag'] = ''
            session['gnm'] = None
            session['grepw'] = None



            session['gid'] = get_id('GDB.db',lg,pw)
            session['glg'] = None
            session['gpw'] = None






            return redirect(url_for('account'))
        else:
            session['gnm'] = nm
            session['glg'] = lg
            session['gpw'] = pw
            session['grepw'] = repw
            return redirect(url_for('createacc'))
    else:
        
            
        return redirect(url_for('index'))
def lastdoorbooker():
    WebSheild()
    if request.method == "POST":
       
        nm = request.form.get('NameBook')
        st = request.form.get('TextBook') 
        session['curname'] = nm
        session['curstory'] = st

    return render_template('LastDoor.html')
def returnforbook():
    
    
    return render_template('CreateBook.html',Gname = session['curname'],Gtext=session['curstory'])
# просто шаг назад, внося изменения в поля значениями из сессий
# Добавляем книгу на модерацию и стираем сессии, переброс на личный кабинет (сделать еще в будущем список книг с модерации и редактирование)
def checklog():
    
    if request.method == "POST":
        Itsnorm = True
        lg = request.form.get('Login')
        pw = request.form.get('PassW') 
        if lg=='' or pw== '':
            Itsnorm = False
            session['logtag'] = 'Введите все данные'
            session['glg'] = lg
            session['gpw'] = pw
            return redirect(url_for('index'))


        else:
            if get_id('GDB.db',lg,pw)!= None:
                
                session['gid'] = get_id('GDB.db',lg,pw)
                
                session['glg'] = None
                session['gpw'] = None

                return redirect(url_for('account'))
            else:
                session['logtag'] = 'Пользователь не найден'
                Itsnorm = False   
                session['glg'] = lg
                session['gpw'] = pw
                return redirect(url_for('index'))
        



        
            
    else:
        return redirect(url_for('index'))    
def account():
    WebSheild()
    
    return render_template('Account.html',Gname = by_id('GDB.db','nickname',session['gid']) ,Glogin= by_id('GDB.db','login',session['gid']),Gbooks= find_books('GDB.db',session['gid']))
def createbook():
    WebSheild()
    return render_template('CreateBook.html',Gname = '',Gtext='')
def WebSheild():
    if session['gid'] == '':
        return redirect(url_for('index'))
   
# nm, lg, pw, repw, tag


















p = os.getcwd()
tmpl_p = os.path.join(p,'templates')
stat_p = os.path.join(p,'static')

app = Flask(__name__, template_folder=tmpl_p, static_folder=stat_p)
app.config['SECRET_KEY'] = 'GUY-TAR'
app.add_url_rule('/','index',index)
app.add_url_rule('/createacc','createacc',createacc)
app.add_url_rule('/checkreg','checkreg',checkreg,methods = ['post','get'])
app.add_url_rule('/checklog','checklog',checklog,methods = ['post','get'])
app.add_url_rule('/account','account',account)
app.add_url_rule('/createbook','createbook',createbook,methods = ['post','get'])
app.add_url_rule('/lastdoorbooker','lastdoorbooker',lastdoorbooker,methods = ['post','get'])
app.add_url_rule('/returnforbook','returnforbook',returnforbook)
app.add_url_rule('/postbook','postbook',postbook)
app.add_url_rule('/backfrombook','backfrombook',backfrombook)
app.add_url_rule('/vlibrary','vlibrary',vlibrary)
app.add_url_rule('/NXT','NXT',NXT)
app.add_url_rule('/BCK','BCK',BCK)
app.add_url_rule('/openbook/book_<int:book_id>','openbook',openbook)





# app.add_url_rule('/','index',index)
if __name__ == "__main__":
    app.run()