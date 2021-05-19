from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask import * 
from SAMapp import db, bcrypt, mail
from SAMapp.models import User, Post, Animal, Feedings, Cleanings, Monitoring
from SAMapp.main.forms import AddAnimalForm, UpdateAnimalInfoForm, AddFeedingForm, AddCleaningForm, AddMonitoringForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from SAMapp.QRCode import qrgen
from SAMapp.users.utils import save_picture_animal, send_reset_email
from base64 import b64encode
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	animal_grid = db.engine.execute("SELECT species, animal_image FROM Animal")
	return render_template('home.html', animal_grid=animal_grid)


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


@main.route("/qrpage")
def qrpage():
	return render_template("qrpage.html")


@main.route('/animal/new', methods=['GET', 'POST'])
@login_required
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
	animal_profiles = Animal.query.filter_by(species=this_species).first_or_404()
	feeding_data = db.engine.execute("SELECT user_id, DATETIME(date_completed), extra_info, animal_id FROM feedings ORDER BY date_completed DESC LIMIT 5;")
	cleaning_data = db.engine.execute("SELECT user_id, DATETIME(date_completed), extra_info, animal_id FROM cleanings ORDER BY date_completed DESC LIMIT 5;")
	monitoring_data = db.engine.execute("SELECT user_id, DATETIME(date_completed), extra_info, animal_id FROM monitoring ORDER BY date_completed DESC LIMIT 5;")
	animal_image = url_for('static', filename='animal_pics/' + animal_profiles.animal_image)
	return render_template('logbook.html', animal=animal_profiles, feeding_data = feeding_data, cleaning_data=cleaning_data, monitoring_data=monitoring_data, animal_image=animal_image)


@main.route("/logbook/<string:this_species>/update", methods=['GET', 'POST'])
@login_required
def update_animal(this_species):
	print ("memes")
	animal = Animal.query.filter_by(species=this_species).first_or_404()
	form = UpdateAnimalInfoForm()
	if form.validate_on_submit():
		print (form.data)
		if form.picture.data:
			print()
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
	return render_template('update_animal.html', form=form, animal_image = animal_image, legend='Update existing animal')


@main.route("/logbook/<string:this_species>/new_feeding", methods=['GET', 'POST'])
@login_required
def new_feeding(this_species):
	animal = Animal.query.filter_by(species=this_species).first_or_404()
	form = AddFeedingForm()
	if form.validate_on_submit():
		feeding = Feedings(extra_info=form.extra_information.data, animal_feedings = animal, user_completed = current_user)
		db.session.add(feeding)
		db.session.commit()
		flash('Feeding successfully added', 'success')
		return redirect(url_for('main.animal_profiles', this_species=animal.species))
	return render_template("add_new_feeding.html", form=form, legend='Add Feeding')


@main.route("/logbook/<string:this_species>/new_cleaning", methods=['GET', 'POST'])
@login_required
def new_cleaning(this_species):
	animal = Animal.query.filter_by(species=this_species).first_or_404()
	form = AddCleaningForm()
	if form.validate_on_submit():
		cleaning = Cleanings(extra_info=form.extra_information.data, animal_cleaning = animal, user2_completed = current_user)
		db.session.add(cleaning)
		db.session.commit()
		flash('Cleaning successfully added', 'success')
		return redirect(url_for('main.animal_profiles', this_species=animal.species))
	return render_template("add_new_feeding.html", form=form, legend='Add Cleaning')


@main.route("/logbook/<string:this_species>/new_monitoring", methods=['GET', 'POST'])
@login_required
def new_monitoring(this_species):
	animal = Animal.query.filter_by(species=this_species).first_or_404()
	form = AddMonitoringForm()
	if form.validate_on_submit():
		monitoring = Monitoring(extra_info=form.extra_information.data, animal_monitoring = animal, user3_completed = current_user)
		db.session.add(monitoring)
		db.session.commit()
		flash('Monitoring successfully added', 'success')
		return redirect(url_for('main.animal_profiles', this_species=animal.species))
	return render_template("add_new_feeding.html", form=form, legend='Add Monitoring')


#For deleting an animal
@main.route("/logbook/<string:this_species>/delete", methods=['POST'])
@login_required
def delete_animal(this_species):
	animal = Animal.query.filter_by(species=this_species).first_or_404()
	db.session.delete(animal)
	db.session.commit()
	flash('Animal has been removed from the database!', 'success')
	return redirect(url_for('main.home'))


#QR Generator stuff that wasnt used in the end
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


@main.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
		if current_user.is_authenticated:
			return redirect(url_for('main.home'))
		form = RequestResetForm()
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			send_reset_email(user)
			flash('An email has been sent with instructions to reset your password', 'info')
			return redirect(url_for('users.login'))
		return render_template('reset_request.html', title='Reset Password', form=form)


@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token	(token):
		if current_user.is_authenticated:
			return redirect(url_for('main.home'))
		user = User.verify_reset_token(token)
		if user is None:
			flash('That is an invalid or expired token', 'warning')
			return redirect(url_for('main.reset_request'))
		form = ResetPasswordForm()
		if form.validate_on_submit():
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user.password = hashed_password
			db.session.commit()
			flash('Your password has beeen updated', 'success')
			return redirect(url_for('users.login'))
		return render_template('reset_token.html', title='Reset Password', form=form)