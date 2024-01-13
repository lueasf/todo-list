from flask import Flask, g, jsonify
from flask import render_template, url_for, request, redirect
from flask import session
from flask_session import Session
import sqlite3

DATABASE="tasks.db"

todo = Flask(__name__)
todo.config['SESSION_TYPE'] = 'filesystem'
todo.config['SECRET_KEY'] = 'clétopsecrete'
todo.config['SESSION_COOKIE_SECURE'] = True
todo.config['SESSION_COOKIE_HTTPONLY'] = True
# httponly empeche l'accès aux cookies via js
# pour empecher le cross site scripting (XSS),
# une attaque de base "qui permet d'injecter
# dans un site web du code malveillant" : MDN
Session(todo) 


### BASE DE DONNEE ###

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = sqlite3.connect(DATABASE)
    return db

@todo.teardown_appcontext
def close_db(exc):
    db = getattr(g,'_db', None)
    if db is not None:
        db.close()

### AFFICHAGE ###

@todo.route("/")
def ok():
    return "le serveur est fonctionnel"

@todo.route("/all", methods=['GET','POST'])
def all():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    con.commit()
    con.close()
    return render_template('index.html', tasks=tasks)

@todo.route("/api/all", methods=['GET'])
def get_all():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    con.close()
    return jsonify({'tasks' : tasks})

### ACTIONS ###

@todo.route("/add", methods=['POST','GET'])
def add():
    if request.method == 'POST':
        contenu = request.form.get('contenu') #.get('') pour renvoyer None si inexistant
        statut = 'Terminé' if request.form.get('statut') else 'Non terminé' #.form[''] pour renvoyer une erreur si inexistant
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('INSERT INTO tasks (contenu, statut) VALUES (?,?)', (contenu, statut))
        con.commit()
        con.close()
        return redirect(url_for('all'))
    return render_template('add.html')

@todo.route("/edit/<int:id>", methods=['POST','GET'])
def edit(id):
    if request.method == 'POST':
        contenu = request.form.get('contenu')
        statut = 'Terminé' if request.form.get('statut') else 'Non terminé'
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('UPDATE tasks SET contenu=?, statut=? WHERE id=?', (contenu, statut, id))
        con.commit()
        con.close()
        return redirect(url_for('all'))
    return render_template('edit.html', id=id)

@todo.route("/del/<int:id>")
def delete(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('DELETE FROM tasks WHERE id=?', (id,))
    con.commit()
    con.close()
    return redirect(url_for('all'))


### USER ###
@todo.route("/register", methods=['POST','GET'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        user_password = request.form.get('user_password')
        if not user_password:
            return render_template('register.html', error='Mot de passe vide')
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('INSERT INTO user (username, password) VALUES (?,?)', (user_name, user_password))
        con.commit()
        con.close()
        return redirect(url_for('all'))
    return render_template('register.html')

@todo.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('SELECT * FROM user WHERE username=? AND password=?', (user_name, user_password))
        user = cur.fetchone()
        con.close()
        if user:
            session['username'] = user_name
            return redirect(url_for('all'))
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == "__main__":
    todo.run(debug=True)