from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from SAMapp import db
from SAMapp.models import Post
from SAMapp.posts.forms import PostForm

posts = Blueprint('posts', __name__)


#Creating new posts
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	#If the data entered on the form meets our validation then adds the post to our db
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.forums'))
	return render_template('create_post.html', title='New Post', form=form, legend='New Post')


#For going to specific posts
@posts.route("/post/<int:post_id>")
def post(post_id):
	#Stops them from going to a post that doesn't exist
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)


#For updating current posts
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
		return redirect(url_for('posts.post', post_id=post.id))
	#Gets the current details and displays them in the text fields
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form=form,
							legend='Update Post')


#For deleting a post
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
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
    return redirect(url_for('main.home'))