from flask import render_template, request, redirect, url_for, flash
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# import sqlite3
# conn = sqlite3.connect('registrants.db')
# db = conn.cursor()
# conn.row_factory = sqlite3.Row

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('create_account.html', title='create_account', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Hello {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('home')

@app.route("/account")
def account():
    image_filepath = url_for('static', filename='profile pictures/default.jpg')
    return render_template('account.html', title='account', image_file=image_filepath)