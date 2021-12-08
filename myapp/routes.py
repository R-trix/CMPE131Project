#from flask import Flask
from werkzeug import datastructures
from myapp import myobj, db
from myapp.forms import LoginForm, RegisterForm, DeleteForm, PracticeForm, FlashCardForm, NotesForm, ShuffleForm, UploadForm, ShareForm 
from myapp.models import User, Task, FlashCards, Notes
from flask import render_template, flash, redirect, request 
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
import random
import pdfkit
from markdown import markdown
from werkzeug.utils import secure_filename

@myobj.route("/")
def main():
    """
        this will route the  primary directory of website to home.html; if user is not logged in, it will pass in the login form; if user is logged in, it will reroute to the page

        returns: render_template - main page's webpage info
    """
    users = User.query.all() #Just a checker in output if methods work as intended.
    for u in users:
        print(u.id, u.username)
    
    tasks = Task.query.all()
    for t in tasks:
        print(t.__repr__())
    
    notes = Notes.query.all()
    for n in notes:
        print(n.__repr__())
        
    cards = FlashCards.query.all()
    for c in cards:
        print(c.__repr__())
    
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

@myobj.route("/logout")
@login_required
def logout():
    """
          this allows the user to logout. 

          returns: redirects the user to the main home page after they log out
    """
    logout_user()
    return redirect("/")


@myobj.route("/createaccount", methods=["GET", "POST"])
def newacc():
    """
        this page is created so that users can make a new account; leads to a login form 
        form validate will ensure valid credentials were entered

        returns: render_template: this webpage will have the new account form info 
    """

    form = RegisterForm()

    if (form.validate_on_submit()):

        #user = User.query.filter_by(username=username).first()
        
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

@myobj.route("/deleteacc", methods=["GET", "POST"])
def delete():
    """ 
        lets users delete their account from the account dropdown menu 
        returns:
            render_template: this webpage lets users delete thier account. 
    """
    form = DeleteForm()
    
    if (form.validate_on_submit()):
        username = form.username.data
        user_to_delete = User.query.filter_by(username=username).first()
        
        notes = user_to_delete.notes.all()
        for note in notes:
            db.session.delete(note)
        
        cards = user_to_delete.cards.all()
        for card in cards:
            db.session.delete(card)
        
        tasks = user_to_delete.tasks.all()
        for task in tasks:
            db.session.delete(task)
        
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
        
    return render_template('delete.html', form=form, current_user=current_user)

@myobj.route("/stopwatch")
@login_required
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
        #card = FlashCard(term=form.term.data, definition=form.definition.data, user_id=current_user.id)
        card = FlashCards(term=form.term.data, definition=form.definition.data, user_id=current_user.id)
        db.session.add(card)
        db.session.commit()
        
        flash("FlashCard has been created.")
        return redirect("/createcard")
    return render_template("newcard.html", form=form)

@myobj.route("/cardview", methods=["POST", "GET"])
@login_required
def cardview():
    """
       outputs a page which displays all the flashcards

    Returns:
        render_template: outputs all the cards created by the user 
    """
    form = ShuffleForm()
   # cards_all = current_user.cards.all()
    cards_list = []
    for card in current_user.cards:
        cards_list.append(card)
        
    if form.validate_on_submit():
        flash("Cards shuffled.")
        random.shuffle(cards_list) 

    #cards_all = []
    # flashcards created by the user will get pushed to the cards_all list
    #for card in current_user.usercards:
    #    cards_all.append(card)
    return render_template("cardview.html", cards_all=cards_list, form=form, user=current_user)

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
    """
       the task/todo feature helps users keep track of items they need to complete. the following definitions allow them to add, delete, and mark done any of their items.

    Returns:
        render_template: todo.html which will list out anf perform desired operation on the action item
    """
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

@myobj.route('/markdown_to_pdf', methods=['GET', 'POST'])
def markdown_to_pdf():
    '''
           users upload markdown files.

        returns: pdf version of markdown file
    '''
    form = UploadForm()
    if form.validate_on_submit():
        # get file name from form
        filename = secure_filename(form.file.data.filename)
       # form.file.data.save('myapp/flashcards/' + filename)
        form.file.data.save('myapp/' + filename)
        # save the md file name and change to pdf file name
       # input_filename = "myapp/flashcards/" + filename
        input_filename = "myapp/" + filename        
        output_filename = input_filename.split(".md")
        output_filename = output_filename[0] + '.pdf'
        
        #convert md file to pdf file
        with open(input_filename, 'r') as f:
            html_string = markdown(f.read(), output_format='html')
        pdfkit.from_string(html_string, output_filename)
        return render_template('markdown_to_pdf.html', form=form, pdf=output_filename)
    
    return render_template('markdown_to_pdf.html', form=form)

@myobj.route("/practice", methods=["POST", "GET"])
@login_required
def practice():
    """
        with this feature, the user can practice preparing for the quiz/test with the flashcards they have created
    Returns:
        render_template: feature will mix the cardsets so user can prepare for their quiz/test.  
    """
    form = PracticeForm()
    cards_all = current_user.cards.all()
    #cards_all=FlashCard.query.all()
    #qsList = [] 
    #ansList = []

    correct = 0
    total_correct = 0
    incorrect = 0
    total_incorrect = 0

    # to mix:
    #random.shuffle(cards)
    random.shuffle(cards_all)

    #for card in cards_all:
    #    qsList.append(card)

    
    #for card in cards_all:
    #    ansList.append(card.definition)

    if form.validate_on_submit():
        card_index = 0
        #while card_index <= len(qsList):
        #    if form.ans.data == qsList[card_index]:
        while card_index <= len(cards_all):
            if form.ans.data == cards_all[card_index].definition:
                correct += 1
            else:
                incorrect += 1

            card_index + 1

        total_correct = correct/len(cards_all)
        total_incorrect = incorrect/len(cards_all)

    return render_template("practice.html", form=form, cards_all=cards_all, total_correct=total_correct, total_incorrect=total_incorrect)

@myobj.route("/results", methods=["POST", "GET"])
@login_required
def results():
    total_correct = request.form["total_correct"]
    total_incorrect = request.form["total_incorrect"]
    
    flash(f"Total correct is {total_correct}")
    flash(f"Total incorrect is {total_incorrect}")
    
    return redirect("/practice")

@myobj.route("/sharenotes", methods=["POST", "GET"])
@login_required
def sharenotes():
    """[summary]
    """
    form = ShareForm()
    
    option = []
    for note in current_user.notes:
        option.append((note.id, note.title))
    
    form.note.choice=option
    
    if(form.validate_on_submit()):
        sendto = User.query.filter(User.username == form.user.date, User.public==True).first()
        if(sendto is not None):
            sendto.notes.append(Note.query.filter_by(id=form.note.data).first())
            db.session.commit()
            flash(f"The note was sent to {sendto.username}.")
            redirect ("/addnote")
        else:
            flash("Sorry, the requested user was not found. Pleases try again later.")
            redirect("/sharenotes")
        
    return render_template("sharenote.html", form=form)
