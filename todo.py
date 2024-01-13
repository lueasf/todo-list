from flask import Flask, g, jsonify
from flask import render_template, url_for, request, redirect
from flask import session
from flask_session import Session
import sqlite3

DATABASE="tasks.db"

todo = Flask(__name__)
todo.config['SESSION_TYPE'] = 'filesystem'
todo.config['SECRET_KEY'] = 'clétopsecrete'
Session(todo) 


### BASE DE DONNEES ###

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = sqlite3.conect(DATABASE)
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

@todo.route("/all")
def all():
    if 'username' not in session:
        return redirect(url_for('login'))
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    con.commit()
    con.close()
    return render_template('index.html', tasks=tasks)

@todo.route("/api/all", methods=['GET'])
def get_all():
    if 'username' not in session:
        return redirect(url_for('login'))
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    con.close()
    return jsonify({'tasks' : tasks})

### ACTIONS ###

@todo.route("/add", methods=['POST','GET'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
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
    pass

@todo.route("/del/<int:id>")
def delete(id):
    if 'username' not in session:
        return redirect(url_for('login'))
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
        user_password = request.form.get(' user_password')
        con = sqlite3.conect(DATABASE)
        cur = con.cursor()
        cur.execute('INSERT INTO user (username, password) VALUES (?,?)', (user_name, user_password))
        con.commit()
        con.close()
        return redirect(url_for('all'))
    return render_template('register.html')

@todo.route("/login", methods=['POST','GET'])
def login():
    return render_template('login.html')

if __name__ == "__main__":
    todo.run(debug=True)