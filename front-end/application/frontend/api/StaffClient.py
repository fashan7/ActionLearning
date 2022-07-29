import requests
from flask import session, request

from application.frontend.api.UrlClient import UrlClient


class StaffClient:
    @staticmethod
    def read_url_one():
        obj = UrlClient()
        return obj.set_url_one()

    @staticmethod
    def department_reg(form):
        ob = StaffClient.read_url_one()
        payload = {
            'name': form.dname.data
        }
        url = f'{ob}api/department/create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def get_departments():
        ob = StaffClient.read_url_one()
        url = f"{ob}api/department"
        response = requests.request(method="GET", url=url)
        branch = response.json()
        return branch

    @staticmethod
    def get_staff_latest_code():
        ob = StaffClient.read_url_one()
        url = f"{ob}api/gen-staff-code"
        response = requests.request(method="GET", url=url)
        res = response.json()
        return res

    @staticmethod
    def post_staff_reg(form):
        ob = StaffClient.read_url_one()
        payload = {
            'staffcode': form.staffcode.data,
            'firstname': form.firstname.data,
            'lastname': form.lastname.data,
            'username': form.username.data,
            'password': form.password.data,
            'gender': form.gender.data,
            'department': form.department.data,
            'branch': form.branch.data,
            'address1': form.address1.data,
            'address2': form.address2.data,
            'address3': form.address3.data,
            'postalcode': form.postalcode.data,
            'city': form.city.data,
            'country': form.country.data,
            'date_of_birth': form.dob.data,
            'email': form.email.data,
            'mobile': form.phone.data,
        }
        url = f'{ob}api/staff/create'
        response = requests.request("POST", url=url, data=payload)

        return response