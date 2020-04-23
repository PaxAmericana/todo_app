from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import sqlite3
conn = sqlite3.connect('registrants.db')
db = conn.cursor()
conn.row_factory = sqlite3.Row


@app.route('/')
def tasks():
    with sqlite3.connect('registrants.db') as conn:
        conn.row_factory = sqlite3.Row
        db = conn.cursor()

        db.execute("SELECT * FROM registrants")
        todos = db.fetchall()
    return render_template('tasks.html', todos=todos)
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