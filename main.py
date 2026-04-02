from flask import Flask, redirect, url_for, session, request, render_template
import os




















def index():
    return render_template('Login.html')




















p = os.getcwd()
tmpl_p = os.path.join(p,'templates')
stat_p = os.path.join(p,'static')

app = Flask(__name__, template_folder=tmpl_p, static_folder=stat_p)
app.config['SECRET_KEY'] = 'GUY-TAR'
# app.add_url_rule('/','index',index)


app.add_url_rule('/','index',index)
if __name__ == "__main__":
    app.run()