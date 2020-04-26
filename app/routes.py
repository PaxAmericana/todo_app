from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post


import sqlite3
conn = sqlite3.connect('registrants.db')
db = conn.cursor()
conn.row_factory = sqlite3.Row

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=[])

@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/tasks')
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
        return redirect(url_for('tasks'))
        # rather than past render_template(tasks.html many times, the tasks function will handle that for me, just tell it to go to that function
        #return render_template(tasks.html, todos=todos)


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('create_account.html', title='create_account', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
