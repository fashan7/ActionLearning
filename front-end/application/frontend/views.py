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
    response_section = PrivilegeClient.group_sections()
    sections = list()
    for data in response_section:
        sections.append(list(data.values()))
    return render_template('dashboard/index.html', sections=sections)