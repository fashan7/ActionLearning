import requests
from . import forms
from . import frontend_blueprint
from .api.PriviledgeClient import PrivilegeClient
from .api.UserClient import UserClient
from .. import login_manager

from flask import render_template, session, redirect, url_for, flash, request, jsonify
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    item = UserClient.get_user()
    return item.get('result')


@frontend_blueprint.route('/', methods=['GET'])
def home():
    if not session.get('user'):
        return redirect(url_for('frontend.login'))
    user_id = session['user'].get('id')
    response_section = PrivilegeClient.group_sections(user_id)
    nav_bar = dict()
    for data in response_section:
        temp = list(data.values())
        response_sub_section = PrivilegeClient.get_sub_sections(user_id, temp[0])
        nav_bar.update({temp[0]: response_sub_section})

    return render_template('dashboard/index.html', sections=nav_bar)

@frontend_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated or (session.get('user') and len(session['user']) > 0):
        return redirect(url_for('frontend.home'))

    form = forms.LoginForm()
    if request.method == "POST":
        api_key = UserClient.post_login(form)
        if api_key:
            session['user_api_key'] = api_key
            user = UserClient.get_user()
            session['user'] = user['result']
            flash('Welcome back, ' + user['result']['username'], 'success')
            return jsonify({'status':200})
        else:
            return jsonify({'status':401})
    return render_template('login/index.html')


@frontend_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('frontend.login'))



