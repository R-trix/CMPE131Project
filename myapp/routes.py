from myapp import myobj, db
from myapp .forms import LoginForm, RegisterForm, DeleteForm
from myapp.models import User

from flask import render_template, flash, redirect
from flask_login import login_user ######DOUBLE CHECK######

from myapp import login

@myobj.route("/")
def main():
    """
        this will route the  primary directory of website to home.html
	if user is not logged in, it will pass in the login form
	if user is logged in, it will reroute to the page

	returns: render_template - main page's webpage info
    """
    return render_template('home.html',user=current_user)


@myobj.route("/login",methods=['GET','POST'])
def login():
    """
	users can login to their account via this login page
	form validate will cross-check that the info entered by the user exists in the db (ensure password matches)
	
	returns: render_template: webpage where user can type in their credentials in order to login
    """
    form = LoginForm()

    if(form.validate_on_submit()): 

        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(username = username).first()

        if(user is None or not user.check_password(form.password.data)):
            flash("sorry, the password you entered in incorrect. please try again.")
            return redirect('/login')


        login_user(user, remember = remember_me)
        return redirect('/')


    return render_template('login.html', form=form)

#make logout def

#account creation
@myobj.route("/create account", methods=["GET", "POST"])
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

        if(credentials_check[0] == False):
            flash(f'{credentials_check[1]} Try again.')
            return redirect('/create account')

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account is now created. You may log in now.')
        return redirect('/')

    return render_template('register.html', form=form)

#need to add delete acc def
