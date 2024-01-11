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
def index():
    return 'Le serveur est fonctionnel'

if __name__ == '__main__':
    todo.run(debug=True)
