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


def navigation_data(user_id):
    response_section = PrivilegeClient.group_sections(user_id)
    nav_bar = dict()
    for data in response_section:
        temp = list(data.values())
        response_sub_section = PrivilegeClient.get_sub_sections(user_id, temp[0])
        nav_bar.update({temp[0]: response_sub_section})
    return nav_bar


@frontend_blueprint.route('/dashboard', methods=['GET'])
def home():
    if not session.get('user'):
        return redirect(url_for('frontend.login'))
    user_id = session['user'].get('id')
    nav_data = navigation_data(user_id)

    return render_template('dashboard/index.html', sections=nav_data)


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
            return jsonify({'status': 200})
        else:
            return jsonify({'status': 401})
    return render_template('login/index.html')


@frontend_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('frontend.login'))


@frontend_blueprint.route('/user-reg', methods=['GET', 'POST'])
def user_register():
    if not session.get('user'):
        return redirect(url_for('frontend.login'))
    user_id = session['user'].get('id')
    nav_data = navigation_data(user_id)

    branches = UserClient.get_branches()
    roles = UserClient.get_roles()

    form = forms.UserForm()
    if request.method == "POST":
        response_result = UserClient.post_user_reg(form)
        return jsonify({'status': response_result.status_code})

    return render_template('user/register.html', sections=nav_data, branches=branches, roles=roles)


@frontend_blueprint.route('/branch-create', methods=['GET', 'POST'])
def branch_register():
    if not session.get('user'):
        return redirect(url_for('frontend.login'))
    user_id = session['user'].get('id')
    nav_data = navigation_data(user_id)

    form = forms.BranchForm()
    if request.method == "POST":
        response = UserClient.post_branch_reg(form)
        return jsonify({'status': response.status_code})

    return render_template('user/branch.html', sections=nav_data)


@frontend_blueprint.route('/user-roles', methods=['GET', 'POST'])
def user_roles():
    if not session.get('user'):
        return redirect(url_for('frontend.login'))

    user_id = session['user'].get('id')
    nav_data = navigation_data(user_id)

    form = forms.RolesForm()
    if request.method == "POST":
        response_result = UserClient.roles(form)
        return jsonify({'status': response_result.status_code})

    return render_template('user/user-roles.html', sections=nav_data)
