import requests
from flask import session, request

from application.frontend.api.UrlClient import UrlClient


class UserClient:
    @staticmethod
    def read_url_one():
        obj = UrlClient()
        return obj.set_url_one()

    @staticmethod
    def post_login(form):
        ob = UserClient.read_url_one()
        api_key = False
        payload = {
            'username': form.username.data,
            'password': form.password.data
        }
        url = f'{ob}api/user/login'
        response = requests.request("POST", url=url, data=payload)
        if response:
            d = response.json()
            if d['api_key'] is not None:
                api_key = d['api_key']
        return api_key

    @staticmethod
    def get_user():
        ob = UserClient.read_url_one()
        headers = {
            'Authorization': 'Basic ' + session['user_api_key']
        }
        url = f'{ob}api/user'
        response = requests.request(method="GET", url=url, headers=headers)
        user = response.json()
        return user

    @staticmethod
    def get_branches():
        ob = UserClient.read_url_one()
        url = f"{ob}api/getall-branch"
        response = requests.request(method="GET", url=url)
        branch = response.json()
        return branch.get('results')

    @staticmethod
    def get_roles():
        ob = UserClient.read_url_one()
        url = f"{ob}api/user-roles"
        response = requests.request(method="GET", url=url)
        roles = response.json()
        return roles.get('data')

    @staticmethod
    def post_user_reg(form):
        ob = UserClient.read_url_one()
        payload = {
            'first_name': form.firstname.data,
            'last_name': form.lastname.data,
            'email': form.email.data,
            'username': form.username.data,
            'password': form.password.data,
            'usertype': form.roles.data,
            'branch_id': form.branch.data,
            'address1': form.address1.data,
            'address2': form.address2.data,
            'address3': form.address3.data,
            'postal_code': form.postalcode.data,
            'city': form.city.data,
            'country': form.country.data
        }
        url = f'{ob}api/user/create'
        response = requests.request("POST", url=url, data=payload)

        return response
        
    @staticmethod
    def post_branch_reg(form):
        ob = UserClient.read_url_one()
        pay_load = {
            'name': form.bname.data
        }
        url = f'{ob}api/branch/create'
        response = requests.request('POST', url=url, data=pay_load)
        return response
        
    @staticmethod
    def roles(form):
        ob = UserClient.read_url_one()
        payload = {
            'name': form.rolename.data
        }
        url = f'{ob}api/user-roles/create'
        response = requests.request("POST", url=url, data=payload)

        return response

    @staticmethod
    def get_all_users():
        ob = UserClient.read_url_one()
        url = f"{ob}api/users"
        response = requests.request(method="GET", url=url)
        users = response.json()
        return users

    @staticmethod
    def get_all_users_withtypes():
        ob = UserClient.read_url_one()
        url = f"{ob}api/users-with-usert"
        response = requests.request(method="GET", url=url)
        users = response.json()
        return users

    @staticmethod
    def recommendation(form):
        ob = UserClient.read_url_one()
        payload = {
            'recommendation': form.recommendation.data
        }

        url = f'{ob}api/student-recommendation/recommendation'
        response = requests.request("POST", url=url, data=payload)

        return response

    @staticmethod
    def feedback(form):
        ob = UserClient.read_url_one()
        payload = {
            'feedback': form.feedback.data
        }

        url = f'{ob}api/student-recommendation/feedback'
        response = requests.request("POST", url=url, data=payload)

        return response