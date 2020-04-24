from flask import Flask, render_template, request, redirect
from tempfile import mkdtemp

app = Flask(__name__)

import sqlite3
conn = sqlite3.connect('registrants.db')
conn.row_factory = sqlite3.Row
db = conn.cursor()
from flask import session
from flask_session import Session

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
from cachelib.file import FileSystemCache
# session gives you access to a python dictionary
Session(app)

with sqlite3.connect('registrants.db') as conn:
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    db.execute("SELECT * FROM registrants")
    rows = db.fetchall()
    todos = rows
    # i'm really not sure how to use these sessions properly
    with app.test_request_context():
        session['todos'] = rows

@app.route('/')
def tasks():
    # with sqlite3.connect('registrants.db') as conn:
    #     conn.row_factory = sqlite3.Row
    #     db = conn.cursor()
    #
    #     db.execute("SELECT * FROM registrants")
    #     todos = db.fetchall()
    data= session['todos']
    print(data)
    return render_template('tasks.html', todos=data)

# GET requests allowed by default
# allow POST requests, which will constain a FORM which contains info that you can choose to POST
@app.route('/add_task', methods =["POST"])
def add_task():
    # if request.method == 'GET':
    #     return render_template('add_task.html')
    if request.method == "POST":
        with sqlite3.connect('registrants.db') as conn:
            conn.row_factory = sqlite3.Row
            db = conn.cursor()
            name = request.form.get('name')
            email = request.form.get('email')
            db.execute("INSERT INTO registrants (name, email) VALUES (?, ?)", [name, email])
            conn.commit()
        return redirect('/')
        # rather than past render_template(tasks.html many times, the tasks function will handle that for me, just tell it to go to that function
        #return render_template(tasks.html, todos=todos)