from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask import * 
from SAMapp import db, bcrypt
from SAMapp.models import User, Post, Animal
from SAMapp.main.forms import AddAnimalForm, UpdateAnimalInfoForm
from flask_login import login_user, current_user, logout_user, login_required
from SAMapp.QRCode import qrgen
from SAMapp.users.utils import save_picture_animal

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	return render_template("home.html")


@main.route("/logbook")
def logbook():
	return render_template("logbook.html")


@main.route("/forums")
def forums():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('forums.html', posts=posts)


@main.route("/about")
def about():
	return render_template("about.html")


@main.route('/animal/new', methods=['GET', 'POST'])
def addnewanimal():
	form = AddAnimalForm()
	if form.validate_on_submit():
		animal = Animal(species=form.species.data, feeding_information=form.feeding_information.data
						,residency_status=form.residency_status.data, extra_information=form.extra_information.data)
		db.session.add(animal)
		db.session.commit()
		flash('New animal added', 'success')
		return redirect(url_for('main.home'))
	return render_template("add_new_animal.html", form=form, legend='Add new animal')


#For going to specific animals
@main.route("/logbook/<string:this_species>")
def animal_profiles(this_species):
	#Stops them from going to an animal that doesn't exist
	#animal_profiles = Animal.query.get_or_404(this_species)
	animal_profiles = Animal.query.filter_by(species=this_species).first_or_404()
	return render_template('logbook.html', animal=animal_profiles)


@main.route("/logbook/<string:this_species>/update", methods=['GET', 'POST'])
def update_animal(this_species):
	animal = Animal.query.filter_by(species=this_species).first_or_404()
	form = UpdateAnimalInfoForm()
	if form.validate_on_submit():
		if form.animal_image.data:
			picture_file = save_picture_animal(form.picture.data)
			animal.animal_image = picture_file
		animal.species = form.species.data
		animal.feeding_information = form.feeding_information.data
		animal.residency_status = form.residency_status.data
		animal.extra_information = form.extra_information.data
		db.session.commit()
		flash('Animal has been updated!', 'success')
		return redirect(url_for('main.animal_profiles', this_species=animal.species))
	elif request.method == 'GET':
		form.species.data = animal.species
		form.feeding_information.data = animal.feeding_information
		form.residency_status.data = animal.residency_status
		form.extra_information.data = animal.extra_information
	animal_image = url_for('static', filename='animal_pics/' + animal.animal_image)
	return render_template('update_animal.html', form=form, legend='Update existing animal')


#For deleting an animal
@main.route("/logbook/<string:this_species>/delete", methods=['POST'])
@login_required
def delete_animal(this_species):
	animal = Animal.query.filter_by(species=this_species).first_or_404()
	db.session.delete(animal)
	db.session.commit()
	flash('Animal has been removed from the database!', 'success')
	return redirect(url_for('main.home'))


@main.route('/converted', methods = ['POST'])
def convert():
	global text
	print("qr gen 123")
	text = request.form['Test']
	return render_template('download.html')


@main.route('/download')
def download():
    qrgen(text)
    filename = text+'.png'
    return send_file('static/qr_codes/' + filename,as_attachment=True)
