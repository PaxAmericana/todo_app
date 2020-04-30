from flask import render_template, request, redirect, url_for, flash, abort
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, PostForm, TaskForm
from blog.models import User, Post, Task
from flask_login import login_user, current_user, logout_user, login_required


# import sqlite3
# conn = sqlite3.connect('registrants.db')
# db = conn.cursor()
# conn.row_factory = sqlite3.Row

@app.route("/")
@app.route("/home")
def home():
    # default is 1, required to be an int
    selected_page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=selected_page, per_page=2)
    # on the paginate object, you must use posts.items... to get the values on that page
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/tasks', methods=["GET", "POST"])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(content=form.content.data, author=current_user)
        db.session.add(new_task)
        db.session.commit()
    tasks = Task.query.filter_by(author=current_user)
    return render_template('tasks.html', tasks=tasks, form=form)

@app.route('/task/<int:task_id>')
@login_required
def task(task_id):
    task = Task.query.get_or_404(task_id)
    # notice that filter by id is so common that you can just type in Model.query(id), the 404 function helps if the iD DNE
    # it's interesting how you update db.session with the model instance, but then you query the model
    return render_template('task.html', task=task)

@app.route('/task/<int:task_id>/delete', methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user != task.author:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('your task has been deleted', 'success')
    return redirect(url_for('tasks'))

@app.route('/slide')
@login_required
def slide():
    # rather than getting one task as a time and querying one at a time, you can paginate all the lines together
    slide_number = request.args.get('page',1,type=int)
    tasks = Task.query.order_by(Task.id).paginate(page=slide_number, per_page=1)
    # notice that filter by id is so common that you can just type in Model.query(id), the 404 function helps if the iD DNE
    # it's interesting how you update db.session with the model instance, but then you query the model
    return render_template('slide.html', tasks=tasks)

@app.route('/task/<task_id>/edit', methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm()
    if form.validate_on_submit():
        task.content = form.content.data
        db.session.commit()
        flash('Your Task is Updated', "success")
        return redirect(url_for('tasks'))
    elif request.method=="GET":
        # fill in the form with the current info
        form.content.data = task.content
    # notice that filter by id is so common that you can just type in Model.query(id), the 404 function helps if the iD DNE
    # it's interesting how you update db.session with the model instance, but then you query the model
    return render_template('edit_task.html', form=form, task=task)

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
        login_user(user)
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
@login_required
def account():
    image_filepath = url_for('static', filename='profile pictures/default.jpg')
    return render_template('account.html', title='account', image_file=image_filepath)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    # this is equivalent to form.method == "POST" , plus it checks our valid input methods (form validators)
    if form.validate_on_submit():
        # grab the form and save it
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('your post is now in the matrix', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods = ["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        # forbidden link - Insufficient permissions
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # updating is suuuuuper simple with sqlAlchemy
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post was Updated", "success")
        return redirect(url_for('post', post_id=post.id))
    # to fill in the form with the current data - set the form object!
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title=post.title,form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete', methods = ["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        # forbidden link - Insufficient permissions
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted', "success")
    return redirect(url_for('home'))