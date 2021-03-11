from flask import render_template, url_for, flash, redirect
from SAMapp import app
#from SAMapp import qrgenerator 
from SAMapp.forms import RegistrationForm, LoginForm
from SAMapp.models import User, Post

posts = [
	{
		"author": "Niall Mclawrence",
		"title": "Forum Post 1",
		"content": "First Post Content",
		"date_posted": "Feb 16, 2021"
	},
	{
		"author": "Thomas Philips",
		"title": "Forum Post 2",
		"content": "Second Post Content",
		"date_posted": "Feb 17, 2021"
	},
	{
		"author": "Andrew Lovell",
		"title": "Forum Post 3",
		"content": "Third Post Content",
		"date_posted": "Feb 18, 2021"
	}
]

#Routing the pages
@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/qrgenerator")
def qrgenerator():
	return SAMapp.qrgenerator()

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
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)