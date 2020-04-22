from flask import Flask, render_template, request, redirect

app = Flask(__name__)

todos = [
        "go to the allergy office",
        "watch the databases video while you're there",
        "try to work on SQL via the web course so that you can complete CETO.. all friday/saturday",
]

@app.route('/')
def tasks():
    return render_template('tasks.html', todos=todos)
# GET requests allowed by default
# allow POST requests, which will constain a FORM which contains info that you can choose to POST
@app.route('/add_task', methods =["GET", "POST"])
def add_task():
    if request.method == 'GET':
        return render_template('add_task.html')
    if request.method == "POST":
        todo = request.form.get('task')
        todos.append(todo)
        return redirect('/')
        # rather than past render_template(tasks.html many times, the tasks function will handle that for me, just tell it to go to that function
        #return render_template(tasks.html, todos=todos)