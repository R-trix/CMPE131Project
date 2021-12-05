#from flask import Flask
from os import urandom
from myapp import myobj, db

from myapp.forms import LoginForm, RegisterForm, DeleteForm, SearchForm, Practice, FlashCard

from myapp.models import User
from myapp.models import Task
from myapp.models import FlashCard

from flask import render_template, flash, redirect, request 
# DOUBLE CHECK######
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
import random 
from random import shuffle

#import time
#import tkinter as tk
#from datetime import datetime as dt

import threading
#from myapp import login


@myobj.route("/")
def main():
    """
        this will route the  primary directory of website to home.html; if user is not logged in, it will pass in the login form; if user is logged in, it will reroute to the page

        returns: render_template - main page's webpage info
    """
    if (current_user.is_anonymous):
        return render_template("homeanon.html")  # ,user=current_user
    else:
        return render_template("home.html", current_user=current_user)


@myobj.route("/login", methods=['GET', 'POST'])
def login():
    """
        users can login to their account via this login page
        form validate will cross-check that the info entered by the user exists in the db (ensure password matches)

        returns: render_template: login form where users can input the required info to login
    """
    form = LoginForm()

    if(form.validate_on_submit()):

        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        flash(f'Login requested for user {form.username.data}')
        user = User.query.filter_by(username=username).first()

        if(user is None):
            flash(
                "Sorry, the username you entered doesn't exist. Please create an account.")
            return redirect("/login")

        if(not user.check_password(form.password.data)):
            flash("Sorry, the password you entered in incorrect. Please try again.")
            return redirect("/login")

        login_user(user, remember=remember_me)
        current_user.is_anonymous = False
        return redirect("/")

    return render_template("login.html", form=form)

# make logout def


@myobj.route("/logout")
@login_required
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

        returns: render_template: this webpage will have the new account form info 
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


@myobj.route("/stopwatch")
def stopwatch():
    
    """
       outputs a stopwatch for timing

    Returns:
        render_template: returns stopwatch to use for students.
    """
    return render_template("stopwatch.html")


@myobj.route("/createcard", methods=["POST", "GET"])
@login_required
def createcard():
    """ 
        This feature will let users create flashcards.

    Returns:
        render_template: webpage will ask user to input a word & its definition in a box in order for the flashcard to be created. 
        A button will enter the flashcard into the database
    """
    form = FlashCard()
    # once user hits submit, flashcard will be created and be added into the database
    if form.validate_on_submit():
        #flash("Added flashcard.")
        card = FlashCard(term=form.term.data, definition=form.definition.data)
        db.session.add(card)
        db.session.commit()

        # the flashcard will be under the user's account if they are signed in
        if current_user.is_authenticated == True:
            card.Users.append(current_user)
            db.session.commit()
        return redirect("/createcard")
    return render_template("newcard.html", form=form)


@myobj.route("/cardview", methods=["POST", "GET"])
@login_required
def cardview():
    """
       outputs a page which displays all the flashcards

    Returns:
        render_template: prints all the cards created by the user 
    """
    cards_all = []
    # flashcards created by the user will get pushed to the cards_all list
    for card in current_user.usercard:
        cards_all.append(card)
  #  return render_template("cardview.html", cards_all=cards_all, '''form=form''')
    return render_template("cardview.html", cards_all=cards_all)



@myobj.route("/task", methods=["POST", "GET"])
@login_required
def list_tasks():
    tasks = Task.query.all()
    return render_template("todo.html", tasks=tasks)


@myobj.route("/addtask", methods=["POST", "GET"])
@login_required
def task_add():
    content = request.form['content']
    if not content:
        return "Sorry, please try again"

    task = Task(content)
    db.session.add(task)
    db.session.commit()

    return redirect("/task")


@myobj.route("/delete/<int:task_id>")
@login_required
def task_delete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect("/task")

    db.session.delete(task)
    db.session.commit()
    return redirect("/task")


@myobj.route("/done/<int:task_id>")
@login_required
def task_done(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect("/task")
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect("/task")


@myobj.route('/create_Notes', methods=['GET', 'POST'])
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

"""
@myobj.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect("/searchres", query=form.search.data)
    return render_template('search.html', form=form)


@myobj.route("/searchres/<query>")
@login_required
def search_result(query):
    results = User.query.whoosh_search(query).all()
    return render_template("searchres.html", query=query, results=results)
""" 

# Change order of flash cards based on how often user got answer correct


@myobj.route("/practice", methods=["POST", "GET"])
@login_required
def practice():
    """
        with this feature, the user can practice preparing for the quiz/test with the flashcards they have created

    Returns:
        render_template: feature will mix the cardsets so user can prepare for their quiz/test. the page should keep track of the correct/incorrect answers of the user. 
    """
    form = Practice()
    cards_all = FlashCard.query.all()

    qsList = []
    ansList = []

    correct = 0
    incorrect = 0

    # to mix:
    random.shuffle(cards_all)

    for card in cards_all:
        qsList.append(card.term)

    for card in cards_all:
        ansList.append(card.definition)

    if form.validate_on_submit():
        card_index = 0
        while card_index <= len(qsList):
            if form.ans == qsList[card_index]:
                correct += 1
            else:
                incorrect += 1

            card_index + 1

        total_correct = correct/len(qsList)
        total_incorrect = incorrect/len(qsList)

        # return redirect("/score", total_correct = total_correct, total_incorrect=total_incorrect)
    return render_template("practice.html", form=form, qsList=qsList)


"""
@myobj.route("/todo", methods=["POST", "GET"])
def todo():
    """
# This todo feature allows users to create a todo list to keep track of their tasks

# returns: will return mainpage or task creation form
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


# @myobj.route("/delete/<int:id>")
@myobj.route("/delete", methods=["GET", "POST"])
def delete(id):
    """
# This feature allows user to delete an item they have added to their todo task list

# returns: will return mainpage or task creation form
"""
    # task_to_delete=Todo.query.get_or_404(id)
    task_to_delete = todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Error deleting task, pelase try again later."


@myobj.route("/update", methods=["GET", "POST"])
def update(id):
    """
#   This feature allows user to update an item they have added to their todo task list

#   returns: will return update task form
"""
    # task=Todo.query.get_or_404(id)
    task = todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating task, sorry, try again later. "

    else:
        return render_template('update.html', task=task)
"""
