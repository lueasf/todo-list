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
def all():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    con.commit()
    con.close()
    return render_template('index.html', tasks=tasks)

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

@todo.route("/del/<int:id>")
def delete(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('DELETE FROM tasks WHERE id=?', (id,))
    con.commit()
    con.close()
    return redirect(url_for('all'))

if __name__ == "__main__":
    todo.run(debug=True, port=5454)