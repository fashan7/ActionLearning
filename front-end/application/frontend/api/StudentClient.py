import requests
from flask import session, request

from application.frontend.api.UrlClient import UrlClient


class StudentClient:
    @staticmethod
    def read_url_one():
        obj = UrlClient()
        return obj.set_url_one()

    @staticmethod
    def student_reg(form):
        ob = StudentClient.read_url_one()
        payload = {
            'firstname': form.firstname.data,
            'lastname': form.lastname.data,
            'branch': form.branch.data,
            'roll_number': form.rollnumber.data,
            'student_email': form.email.data,
            'username': form.username.data,
            'password': form.password.data,
            'gender': form.gender.data,
            'date_of_birth': form.dob.data,
            'parent_name': form.parentname.data,
            'parent_email': form.pemail.data,
            'address1': form.address1.data,
            'address2': form.address2.data,
            'address3': form.address3.data,
            'postalcode': form.postalcode.data,
            'city': form.city.data,
            'country': form.country.data,
            'parent_mobile_number': form.phone.data,
        }
        url = f'{ob}api/student/create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def get_code_roleno():
        ob = StudentClient.read_url_one()
        url = f"{ob}api/gen-role-number"
        response = requests.request(method="GET", url=url)
        res = response.json()
        return res


    @staticmethod
    def get_student(search):
        ob = StudentClient.read_url_one()
        url = f"{ob}api/search-student/{search}"
        response = requests.request(method="GET", url=url)
        res = response.json()
        return {'data':res}
