import requests
from flask import session, request

class StudiesClient:

    @staticmethod
    def course_reg(form):
        payload = {
            'course_name': form.cname.data,
            'course_semester': form.semester.data
        }
        url = ' http://127.0.0.1:5002/api/course/create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def subject_reg(form):
        payload = {
            'name': form.subject.data,
            'course_id': form.course.data
        }
        url = ' http://127.0.0.1:5002/api/subject-create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def get_all_courses():
        r = requests.get(f'http://127.0.0.1:5002/api/get-courses')
        return r.json()

    @staticmethod
    def get_all_subjects():
        r = requests.get(f'http://127.0.0.1:5002/api/get-subjects')
        return r.json()

    @staticmethod
    def get_nextPaper_code():
        r = requests.get(f'http://127.0.0.1:5002/api/gen-paper-code')
        return r.json()

    @staticmethod
    def post_reg_paper(form):
        user_id = session['user'].get('id')
        payload = {
            'paper_no': form.papercode.data,
            'subject_id': form.subject.data,
            'no_of_questions': form.noquestion.data,
            'duration': form.duration.data,
            'user_id': user_id
        }
        url = ' http://127.0.0.1:5002/api/paper-create'
        response = requests.request("POST", url=url, data=payload)
        return response
