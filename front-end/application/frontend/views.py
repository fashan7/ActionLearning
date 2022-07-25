import requests
from . import forms
from . import frontend_blueprint
from .api.PriviledgeClient import PrivilegeClient
from .. import login_manager

from flask import render_template, session, redirect, url_for, flash, request
from flask_login import current_user

@login_manager.user_loader
def load_user(user_id):
    return None

@frontend_blueprint.route('/', methods=['GET'])
def home():
    user_id = 3
    response_section = PrivilegeClient.group_sections(user_id)
    nav_bar = dict()
    for data in response_section:
        temp = list(data.values())
        response_sub_section = PrivilegeClient.get_sub_sections(user_id, temp[0])
        nav_bar.update({temp[0]:response_sub_section})


    return render_template('dashboard/index.html', sections=nav_bar)