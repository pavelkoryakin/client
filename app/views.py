#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm, AccountCreate, AccountEdit
from models import User, Account, ROLE_USER, ROLE_ADMIN

@lm.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('settings'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is None:
			flash('Email "' + form.email.data + '" is not registered') # error messages
			return render_template('login.html', 
				title = 'Sign In',
				form = form,
				css_name = 'signin')
		if user.password == form.password.data:
			user.authenticated = True
			db.session.add(user)
			flash('Your email "' + form.email.data + '" is authorized') # message
			db.session.commit()
			login_user(user)
			return redirect(url_for("settings"))
	return render_template('login.html', 
        title = 'Sign In',
        form = form,
        css_name = 'signin')
        
@login_required
@app.route('/new_account', methods = ['GET', 'POST'])
def create_account():
#	user = g.user
	form = AccountCreate()
	if form.validate_on_submit():
		account = Account(account_name = form.account_name.data, counter_id = form.counter_id.data, goal_id = form.goal_id.data, token = form.token.data, author = g.user)
		db.session.add(account)
		db.session.commit()
		flash('Your account is added!')
		return redirect(url_for('settings'))
	return render_template(
    	'new_account.html',
    	title = 'Add new account',
        form = form,
        css_name = 'settings'
	)

@login_required
@app.route('/settings', methods = ['GET', 'POST'])
def settings():
#	user = g.user
#	user = User.query.filter_by(email = user.email).first()
	accounts = g.user.accounts.all()
# 	accounts = [
# 		{
# 			'author': g.user,
# 			'account_name': 'yandex account',
# 			'counter_id': '99999999',
# 			'goal_id': '999999',
# 			'token': '99999999999999999999999'
# 		},
# 		{
# 			'author': g.user,
# 			'account_name': 'yandex account 2',
# 			'counter_id': '99999999',
# 			'goal_id': '999999',
# 			'token': '99999999999999999999999'
# 		}
# 	]
	return render_template('settings.html',
        title = 'Sign In',
        css_name = 'settings',
        accounts = accounts,
        user = g.user,
        )
        
@login_required
@app.route("/logout", methods=["GET"])
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        css_name = 'signin')
        
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500