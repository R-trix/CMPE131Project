#from flask import Flask
from werkzeug import datastructures
from myapp import myobj, db
from myapp.forms import LoginForm, RegisterForm, DeleteForm, SearchForm, PracticeForm, FlashCardForm, NotesForm
from myapp.models import User, Task, FlashCard, Notes
from flask import render_template, flash, redirect, request 
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
import random

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
    return render_template("stopwatch.html")
    """
       outputs a stopwatch for timing

    Returns:
        render_template: returns stopwatch to use for students.
    """


@myobj.route("/createcard", methods=["POST", "GET"])
@login_required
def createcard():
    """ 
        This feature will let users create flashcards.

    Returns:
        render_template: webpage will ask user to input a word & its definition in a box in order for the flashcard to be created. 
        A button will enter the flashcard into the database
    """
    form = FlashCardForm()
    # once user hits submit, flashcard will be created and be added into the database
    if form.validate_on_submit():
        card = FlashCard(term=form.term.data, definition=form.definition.data, user_id=current_user.id)
        db.session.add(card)
        db.session.commit()

        # the flashcard will be under the user's account if they are signed in
        #if current_user.is_authenticated == True:
        #    card.User.append(current_user)
        #    db.session.commit()
        flash("FlashCard has been created.")
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
    #cards_all = []
    # flashcards created by the user will get pushed to the cards_all list
    #for card in current_user.usercards:
    #    cards_all.append(card)
    cards_all = current_user.cards.all()
    return render_template("cardview.html", cards_all=cards_all)

@myobj.route("/addnote", methods=["POST", "GET"])
@login_required
def add_note():
    
    form = NotesForm()
    
    if (form.validate_on_submit()):

        title = form.title.data
        body = form.body.data
        user_id = current_user.id
        
        note = Notes(title=title, body=body, user_id=user_id)
        db.session.add(note)
        db.session.commit()
        flash(f'Note created.')
        return redirect("/addnote")

    return render_template("addnote.html", form=form)
    
@myobj.route("/displaynotes", methods=["POST", "GET"])
@login_required
def display_notes():
    notes = current_user.notes.all()
    
    return render_template("displaynotes.html", notes=notes, user=current_user)
    
@myobj.route("/task", methods=["POST", "GET"])
@login_required
def list_tasks():
    tasks = current_user.tasks.all()
    return render_template("todo.html", tasks=tasks)


@myobj.route("/addtask", methods=["POST", "GET"])
@login_required
def task_add():
    user_id = current_user.id
    content = request.form['content']
    if not content:
        flash("Please enter something in the field.")
        return redirect("/task")

    task = Task(content, user_id)
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
    if request.method=="POST":
        searched = request.POST['searched']
        createcard """
    #if(form.validate_on_submit):
     #   input = form.search.data
        
    #return render_template("search.html", form=form, )
   # if request.method == 'POST' and form.validate_on_submit():
    #    return redirect("/searchres", query=form.search.data)
    #return render_template('search.html', form=form)



# Change order of flash cards based on how often user got answer correct
@myobj.route("/practice", methods=["POST", "GET"])
@login_required
def practice():
    """
        with this feature, the user can practice preparing for the quiz/test with the flashcards they have created

    Returns:
        render_template: feature will mix the cardsets so user can prepare for their quiz/test. the page should keep track of the correct/incorrect answers of the user. 
    """
    form = PracticeForm()
    cards = current_user.cards.all()

    qsList = []
    
    ansList = []

    correct = 0
    incorrect = 0

    # to mix:
    #random.shuffle(cards)

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