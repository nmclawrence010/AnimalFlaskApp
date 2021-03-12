from flask import render_template, url_for, flash, redirect, request
from SAMapp import app, db, bcrypt
from SAMapp.forms import RegistrationForm, LoginForm
from SAMapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
	{
		"author": "Niall Mclawrence",
		"title": "Forum Test 1",
		"content": "First Post Content",
		"date_posted": "Feb 16, 2021"
	},
	{
		"author": "Thomas Phillips",
		"title": "Forum Test 2",
		"content": "Second Post Content",
		"date_posted": "Feb 17, 2021"
	},
	{
		"author": "Andrew Lovell",
		"title": "Forum Test 3",
		"content": "Third Post Content",
		"date_posted": "Feb 17, 2021"
	}
]

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/logbook")
def logbook():
	return render_template("logbook.html")

@app.route("/forums")
def forums():
	return render_template("forums.html", posts=posts)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')       #Hashes the password on submit
		user = User(username=form.username.data, email=form.email.data, password=hashed_password) #Passes in the hashed password
		db.session.add(user)
		db.session.commit() #adds user to database
		flash('Your account has been created! You can now log in', 'success')   #Shows message on creation
		return redirect(url_for('login'))										#Sends them to login page
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()                  #Checks if email exists in our db
		if user and bcrypt.check_password_hash(user.password, form.password.data):  #Same for password
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')							
			return  redirect(next_page) if  next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')	#if failed will show this message
	return render_template('login.html', title='Login', form=form)	

@app.route("/logout")
def logout():
	logout_user()	
	return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')