import requests
from flask import session, request

class UserClient:
    @staticmethod
    def post_login(form):
        api_key = False
        payload = {
            'username': form.username.data,
            'password': form.password.data
        }
        url = 'http://127.0.0.1:5002/api/user/login'
        response = requests.request("POST", url=url, data=payload)
        if response:
            d = response.json()
            if d['api_key'] is not None:
                api_key = d['api_key']
        return api_key

    @staticmethod
    def get_user():
        headers = {
            'Authorization': 'Basic ' + session['user_api_key']
        }
        url = 'http://127.0.0.1:5002/api/user'
        response = requests.request(method="GET", url=url, headers=headers)
        user = response.json()
        return user

