import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from SAMapp import app, db, bcrypt
from SAMapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from SAMapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/logbook")
def logbook():
	return render_template("logbook.html")

#Select what the current animal is ?????????????????????????????????????????
def current_animal(current_species):
	form = SelectCurrentAnimalForm()
	if form.validate_on_submit():
		current_species = AddAnimal.query.filter_by(species=species.data).first()

@app.route("/forums")
def forums():
	posts = Post.query.all()
	return render_template("forums.html", posts=posts)

#Creating new posts
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	#If the data entered on the form meets our validation then adds the post to our db
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('forums'))
	return render_template('create_post.html', title='New Post', form=form, legend='New Post')

#For going to specific posts
@app.route("/post/<int:post_id>")
def post(post_id):
	#Stops them from going to a post that doesn't exist
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

#For updating current posts
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	#Checks if the post exists in our db
	post = Post.query.get_or_404(post_id)
	#Checks that the current user is the owner of the post and throws a 403 error if not
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('post', post_id=post.id))
	#Gets the current details and displays them in the text fields
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form=form,
							legend='Update Post')

#For deleting a post
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	#Checks if the post exists in our db
    post = Post.query.get_or_404(post_id)
    #Checks that the current user is the owner of the post and throws a 403 error if not
    if post.author != current_user:
        abort(403)
    #Deletes the post from the db
    db.session.delete(post)
    db.session.commit()
    #Confirmation message that their post has been deleted
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
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
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		#Checks if email exists in our db
		user = User.query.filter_by(email=form.email.data).first()
		#Same for password
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')							
			return  redirect(next_page) if  next_page else redirect(url_for('home'))
		else:
			#If failed it will show this message
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)	

@app.route("/logout")
def logout():
	logout_user()	
	return redirect(url_for('home'))

#Saving the profile pic
def save_picture(form_picture):
	#Creates a random 8 bit hex code to assign the image name so we dont have repeat names in the db
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn =random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	
	#Resizing the image before saving
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)		
	i.save(picture_path)

	return picture_fn

#Updating account details
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('account'))
	#Gets the current details and displays them in the text fields
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file = image_file, form=form)