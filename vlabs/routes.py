from flask import render_template, flash, redirect, url_for, request, send_from_directory, abort
from vlabs import app, db, bcrypt
from vlabs.models import Account, Lab
from vlabs.forms import RegistrationForm, LoginForm, AddLabForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import exc
import os, shutil
import datetime

@app.route('/')
@app.route('/home')
def home():
   return render_template('index.html')


@app.route('/labs')
def labs():
    lab_list = Lab.query.all()
    return render_template('pages/labs.html', lab_list=lab_list)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    register_form = RegistrationForm()
    login_form = LoginForm()

    if register_form.validate_on_submit():
            try:
                hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
                new_account = Account(email=register_form.email.data, password=hashed_password)
                db.session.add(new_account)
                db.session.commit()
                flash(f'New account created, you can now log in', 'green')
                return redirect(url_for('login'))
            except exc.IntegrityError as e:
                db.session().rollback()
                flash(f'Email already exists! Please try a different one', 'red darken-3')
                return redirect(url_for('login'))

    if login_form.validate_on_submit():
        account = Account.query.filter_by(email=login_form.email.data).first()
        if account and bcrypt.check_password_hash(account.password, login_form.password.data):
            login_user(account)
            flash(f'Logged in successfully, {login_form.email.data}', 'green')
            return redirect(url_for('account'))
        else:
            flash(f'Login unsuccessful. Please check email and/or password and try again.', 'red darken-3')
            return redirect(url_for('login'))

    return render_template('pages/login.html', login_form=login_form, register_form=register_form)


@app.route('/account')
@login_required
def account():
    return render_template('pages/account.html')


@app.route('/lab/new', methods=['POST', 'GET'])
@login_required
def add():
    if request.method =='POST':
        files = request.files.getlist('file[]')
        title = request.form['title']
        directory_name = title.lower().replace(' ', '-').replace('"', '').replace("'", "").replace(',','')
        stream = request.form['stream']
        description = request.form['description']
        str_date = request.form['date']
        date = datetime.datetime.strptime(str_date, '%b %d, %Y').date()
        account_id = current_user.id
        lab_path = directory_name + '/index.html'
        path = app.config['UPLOAD_FOLDER'] + directory_name
        print(path)
        new_lab = Lab(title=title, stream=stream, description=description, lab_url=lab_path, date_posted=date, account_id=account_id)
        db.session.add(new_lab)
        db.session.commit()
        for file in files:
            filename = secure_filename(file.filename)
            if not os.path.exists(path):
                os.makedirs(path)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], directory_name, filename))
        flash(f'Successfully uploaded!', 'green')
        return redirect(url_for('add'))
    else:
        return render_template('pages/add-new-lab.html')


@app.route('/lab/delete')
@login_required
def delete():
    # lab_list = Lab.query.all()
    return render_template('pages/remove-lab.html')

@app.route('/lab/delete/delete_one/', defaults={'lab_id': ''})
@app.route('/lab/delete/delete_one/<lab_id>', methods=['POST', 'GET'])
@login_required
def delete_lab(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    if lab.author != current_user:
        return redirect(url_for('account'))
    if request.method=='POST':
        if lab.author != current_user:
            abort(403)
        else:
            lab_url_name = lab.lab_url
            directory_name = lab_url_name.split('/')[0]
            path = app.config['UPLOAD_FOLDER'] + directory_name
            shutil.rmtree(path, ignore_errors=True)
            db.session.delete(lab)
            db.session.commit()
            flash(f'Deleted lab - {lab.title}','green')
            return redirect(url_for('delete'))
    return render_template('pages/lab-single.html', lab=lab)


@app.route('/simulation')
def simulation():
    return render_template('pages/chart.html')


@app.route('/logout')
def logout():
    logout_user()
    flash(f'Logged out successfully', 'green')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/errors/404.html')

@app.errorhandler(403)
def no_permission(e):
    return render_template('pages/errors/403.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('pages/errors/500.html')
