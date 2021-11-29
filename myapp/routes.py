from myapp import myobj, db
from myapp.forms import LoginForm, RegisterForm, DeleteForm
from myapp.models import User

from flask import render_template, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user ######DOUBLE CHECK######

#from myapp import login

@myobj.route("/")
def main():
    """
        this will route the  primary directory of website to home.html
	if user is not logged in, it will pass in the login form
	if user is logged in, it will reroute to the page
	returns: render_template - main page's webpage info
    """
    if current_user.is_authenticated:
        return render_template("home.html")
    else:
        return render_template("homeanon.html") #,user=current_user

@myobj.route("/login",methods=['GET','POST'])
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

        flash(f'Login requested for user {form.username.data}, remember_me = {form.remember_me.data}')
        user = User.query.filter_by(username = username).first()

        if(user is None or not user.check_password(form.password.data)):
            flash("sorry, the password you entered in incorrect. please try again.")
            return redirect("/login")


        login_user(user, remember = remember_me)
        return redirect("/")


    return render_template("login.html", form=form)

#make logout def
@myobj.route("/logout")
@login_required
def logout():
    """
          this allows the user to logout. 
	  returns: redirects the user to the main home page after they log out
    """
    logout_user()
    return redirect("/")
 
#account creation
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

        credentials_check = User.check_valid_credentials(username=username, email=email, password=password, retypePassword=retypePassword)

        if(credentials_check == False):
            flash('Please try again.')
            return redirect("/createaccount")

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account is now created. You may log in now.")
        return redirect("/")

    return render_template("newacc.html", form=form)

#need to add delete acc def
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
    if request.method=="POST":
        task_content=request.form["content"]
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Sorry, error adding task, pelase try again later."

    else:
        tasks=Todo.query.all()
        return render_template("index.html", tasks=tasks)


@myobj.route("/delete/<int:id>")
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
	    db.session.delete(task_to_delete)
	    db.session.commit()
	    return redirect("/")
    except:
	    return "Error deleting task, pelase try again later."


@myobj.route("/update/<int:id>",methods=["GET", "POST"])
def update(id):
    task=Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=task)