from flask import Flask, g
from flask import render_template, url_for, request, redirect
import sqlite3

DATABASE="tasks.db"

todo = Flask(__name__)

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

@todo.route("/")
def ok():
    return "le serveur est fonctionnel"

@todo.route("/all")
def rall():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    con.commit()
    con.close()
    return render_template('index.html', tasks=tasks)

@todo.route("/add", methods=['POST','GET'])
def f():
    if request.method == 'POST':
        contenu = request.form.get('contenu')
        status = request.form['status']
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execte('INSERT INTO tasks (contenu, status) VALUES (?,?)', (contenu, status))
        con.commit()
        con.close()
        return redirect(url_for('rall'))
    return render_template('add.html')

if __name__ == "__main__":
    todo.run(debug=True)