#District Datalabs Incubator 2015
#The Synthesizers
#MVP app
#
#Source: http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup

import sqlite3
from mvp_db import conn, curs, qry_commit, qry_drop_basic, qry_drop_corrupt, qry_create_basic, qry_create_corrupt
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from geco.english_class import original_output, corrupt_output


#configuration
DATABASE = 'basic.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#create application
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('MVP_SETTINGS', silent=True)

def init_db():
        qry_commit(qry_drop_basic)
        qry_commit(qry_drop_corrupt)
        qry_commit(qry_create_basic)
        qry_commit(qry_create_corrupt)
        conn.commit()
        conn.close()

init_db()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#log in log out
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


#views with routes
#seperate view from routes for later versions

@app.route('/')
def show_entries():
    cur = g.db.execute('select id, name_last, name_first, gender from basic order by name_last desc')
    entries = [dict(id=row[0], name_last=row[1], name_first=row[2], gender=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

        
    g.db.execute('''insert into basic (name_first, name_last, gender) 
        values (?, ?, ?)''',
                 [request.form['name_first'], request.form['name_last'], request.form['gender']])
    g.db.commit()
    # name_middle, address_1, address_2, city, state, zip, phone, email,
    #, ?, ?, ?, ?, ?, ?, ?, ?
    #\
    #             request.form['name_middle'], 
    #             request.form['address_1'], request.form['address_2'],\
    #             request.form['city'], request.form['state'],
    #             request.form['zip'], request.form['phone'],
    #             request.form['email'],
    flash('data entered')
    return redirect(url_for('show_entries'))

@app.route('/<int:entry_id>', methods=['GET'])
def show_record(entry_id):
    cur = g.db.execute("SELECT id, name_last, name_first, gender FROM basic WHERE id = ?", [entry_id])
    entries = [dict(id=row[0], name_last=row[1], name_first=row[2], gender=row[3]) for row in cur.fetchall()]
    return render_template('single_entry.html', entries=entries, entry_id=entry_id)
    
@app.route('/corrupt/add', methods=['POST'])
def corrupt_add():
    cur = g.db.execute("SELECT id, name_last, name_first, gender FROM basic WHERE id = ?", [request.form['entry_id']])
    #Add corrupting here
    entries = [dict(id=row[0], name_last=row[1], name_first=row[2], gender=row[3]) for row in cur.fetchall()]

    g.db.execute('''insert into corrupt (basic_id, name_first, name_last, gender) 
        values (?, ?, ?, ?)''', [request.form['entry_id'], "b", "c", "d"])
    g.db.commit()
    entry_id = float(request.form['entry_id'])
    flash('data corrupted')
    return redirect(url_for('show_corrupt', entry_id=entry_id))

@app.route('/<int:entry_id>/corrupt', methods=['GET'])
def show_corrupt(entry_id):
    #original entr
    cur = g.db.execute("SELECT id, name_last, name_first, gender FROM basic WHERE id = ?", [entry_id])
    entries = [dict(id=row[0], name_last=row[1], name_first=row[2], gender=row[3]) for row in cur.fetchall()]
    #corrupt counterpart
    cur = g.db.execute("SELECT id, name_last, name_first, gender FROM corrupt WHERE id = ?", [entry_id])
    corrupt = [dict(id=row[0], name_last=row[1], name_first=row[2], gender=row[3]) for row in cur.fetchall()]
    return render_template('single_entry.html', entries=entries, corrupt=corrupt, entry_id=entry_id)


@app.route('/csv_original')
def csv_original():
    f = original_output()
    p = f.read()
    p_n = [x+'\n' for x in p]
    f.close()
    return p

@app.route('/csv_corrupt')
def csv_corrupt():
    return corrupt_output()


if __name__ == '__main__':
    app.run()
