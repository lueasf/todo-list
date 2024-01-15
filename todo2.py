from flask import Flask, g, jsonify, session
from flask import render_template, url_for, request, redirect
from flask import session, abort, make_response
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

## erreur 

@todo.route('/login')
def login():
    abort(401)
    this_is_never_executed()

## session

@todo.route('/set/')
def set():
    session['somekey'] = 'somevalue'
    return 'ok'

@todo.route('/get/')
def get():
    if session.get( 'somekey', None ) == None :
        return redirect(url_for('login')) 


## cookies

@todo.route('/some_route')
def route_that_set_a_cookie():
    some_data = 'somevalue'
    resp = make_response(render_template('mynice.html'))
    resp.set_cookie('mycookie', some_data)
    return resp
device-width
@todo.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'TheBoss')
    return resp