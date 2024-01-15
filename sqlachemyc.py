from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine('sqlite:///bookstore.db')
# engine = create_engine('postgresql://user:password@host/database')
con = engine.connect()
rs = con.execute('SELECT * FROM book')
for row in rs:
    print(row)

con.close()

engine = create_engine('sqlite:///bookstore_tmp.db')
con = engine.connect()

rs = con.execute('DROP TABLE IF EXISTS book')
rs = con.execute('CREATE TABLE book (id INTEGER PRIMARY_KEY,title VARCHAR, primary_author VARCHAR)')
statement = text('INSERT INTO book(id, title, primary_author) VALUES (:id, :title, :primary_author)')
rs = con.execute(statement, {'id':1, 'title':'The Silmarillion','primary_author':'Tolkien' })

for row in rs:
    print(row)
con.close()