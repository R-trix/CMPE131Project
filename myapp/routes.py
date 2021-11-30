from myapp import myobj, db
from myapp.forms import LoginForm, RegisterForm, DeleteForm
from myapp.models import User
from myapp.models import ToDo

from flask import render_template, flash, redirect, request
from flask_login import login_user  # DOUBLE CHECK######

import time
import tkinter as tk
from datetime import datetime as dt

import threading
#from myapp import login


@myobj.route("/")
def main():
    """
        this will route the  primary directory of website to home.html
        if user is not logged in, it will pass in the login form
        if user is logged in, it will reroute to the page

        returns: render_template - main page's webpage info
    """
    return render_template("home.html")  # ,user=current_user


@myobj.route("/login", methods=['GET', 'POST'])
def login():
    """
        users can login to their account via this login page
        form validate will cross-check that the info entered by the user exists in the db (ensure password matches)

        returns: render_template: webpage where user can type in their credentials in order to login
    """
    form = LoginForm()

    if(form.validate_on_submit()):

        #username = form.username.data
        #password = form.password.data
        #remember_me = form.remember_me.data

        flash(
            f'Login requested for user {form.username.data}, remember_me = {form.remember_me.data}')
        user = User.query.filter_by(username=username).first()

        if(user is None or not user.check_password(form.password.data)):
            flash("sorry, the password you entered in incorrect. please try again.")
            return redirect("/login")

        login_user(user, remember=remember_me)
        return redirect("/")

    return render_template("login.html", form=form)

# make logout def


@myobj.route("/logout")
def logout():
    """
          this allows the user to logout. 
          returns: redirects the user to the main home page after they log out
    """
    logout_user()
    return redirect("/")

# account creation


@myobj.route("/createaccount", methods=["GET", "POST"])
def newacc():
    """
        this page is created so that users can make a new account; leads to a login form 
        form validate will ensure valid credentials were entered

        returns: render_template: this webpage will have the new account and login form info 
    """

    form = RegisterForm()

    if (form.validate_on_submit()):

        username = form.username.data
        email = form.email.data
        password = form.password.data
        retypePassword = form.retypePassword.data

        credentials_check = User.check_valid_credentials(
            username=username, email=email, password=password, retypePassword=retypePassword)

        if(credentials_check == False):
            flash('Please try again.')
            return redirect("/createaccount")

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account is now created. You may log in now.")
        return redirect("/")

    return render_template("newacc.html", form=form)


@myobj.route('/stopwatch', methods=['GET', 'POST'])
class MyTimer(threading.Thread):

    def __init__(self, t):
        super(MyTimer, self).__init__()
        self.txt = t
        self.running = True

    def run(self):
        while self.running:
            self.txt['text'] = time.time()


mgui = tk.Tk()
mgui.title('Test')

txt = tk.Label(mgui, text="time")
txt.grid(row=0, columnspan=2)

timer = None


def time_convert(sec):
    elapsed = end - start
    result = "Time Taken: %02d:%02d:%02d:%02d" % (
        elapsed.days, elapsed.seconds // 3600, elapsed.seconds // 60 % 60, elapsed.seconds % 60)


def cmd1():
    global start
    start = dt.now()


def cmd2():
    end = dt.now()
    elapsed = end - start
    result = "Time Taken: %02d:%02d:%02d:%02d" % (
        elapsed.days, elapsed.seconds // 3600, elapsed.seconds // 60 % 60, elapsed.seconds % 60)
    print(result)


btn = tk.Button(mgui, text="Start", command=cmd1)
btn.grid(row=1, column=1)
btn2 = tk.Button(mgui, text="Stop", command=cmd2)
btn2.grid(row=1, column=2)

mgui.mainloop()


@myobj.route('/deleteaccount', methods=['GET', 'POST'])
def delete_acc():
    '''
        Deletes user from database
    '''
    form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        if form.username.data == user.username:
            session.pop('username', None)
            db.session.delete(user)
            db.session.commit()
            flash("Account successfully deleted.")
            return redirect(url_for('index'))
    return render_template('delete-account.html', form=form)


@myobj.route("/todo", methods=["POST", "GET"])
def todo():
    """ 
        This todo feature allows users to create a todo list to keep track of their tasks

        returns: will return mainpage or task creation form 
    """
    if request.method == "POST":
        task_content = request.form["content"]
        #new_task = Todo(content=task_content)
        new_task = todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Sorry, error adding task, pelase try again later."

    else:
        # tasks=Todo.query.all()
        # db.session.query(todo).query.all()
        # db.session.query(todo).all()
       # ToDo.query.all()
        tasks = ToDo.query.all()

        return render_template("index.html", tasks=tasks)


@myobj.route("/delete/<int:id>")
def delete(id):
    """ 
        This feature allows user to delete an item they have added to their todo task list

        returns: will return mainpage or task creation form 
    """
    # task_to_delete=Todo.query.get_or_404(id)
    task_to_delete = todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Error deleting task, pelase try again later."


@myobj.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    """ 
        This feature allows user to update an item they have added to their todo task list

        returns: will return update task form 
    """
    # task=Todo.query.get_or_404(id)
    task = todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=task)


@app_Obj.route('/create_Notes', methods=['GET', 'POST'])
def create_notes():
    forms = markdown_notes()
    title = "Create Notes in markdown"

    if form.validate_on_submit():
        new_note = NoteCards(notes_name=form.notes_name.data,
                             notes_description=form.notes_description.data)
        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/create_Notes')
        except:
            return flash('Error: Unable to save Notes!')
    else:
        notecards = NoteCards.query.all()
        return render_template('notecard.html', form=form, notecards=notecards, title=title)
