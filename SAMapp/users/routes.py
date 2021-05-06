from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from SAMapp import db, bcrypt
from SAMapp.models import User, Post
from SAMapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from SAMapp.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		#Hashes the password on submit
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		#Passes in the hashed password
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		#adds user to database
		db.session.add(user)
		db.session.commit()
		#Message user sees on creation												
		flash('Your account has been created! You can now log in', 'success')
		#Sends the user to the login page to now login
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		#Checks if email exists in our db
		user = User.query.filter_by(email=form.email.data).first()
		#Same for password
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			flash('You have been logged in!', 'success')						
			return  redirect(next_page) if  next_page else redirect(url_for('main.home'))
		else:
			#If failed it will show this message
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)	


@users.route("/logout")
def logout():
	logout_user()	
	return redirect(url_for('main.home'))


#Updating account details
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		print (form.data)
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.account'))
	#Gets the current details and displays them in the text fields
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file = image_file, form=form)


#Showing all posts from a certain user
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)