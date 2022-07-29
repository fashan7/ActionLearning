import requests
from flask import session, request
import datetime
import time
from datetime import datetime as dt

from application.frontend.api.UrlClient import UrlClient


class StudiesClient:
    @staticmethod
    def read_url_one():
        obj = UrlClient()
        return obj.set_url_one()

    @staticmethod
    def course_reg(form):
        ob = StudiesClient.read_url_one()
        payload = {
            'course_name': form.cname.data,
            'course_semester': form.semester.data
        }
        url = f'{ob}api/course/create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def subject_reg(form):
        ob = StudiesClient.read_url_one()
        payload = {
            'name': form.subject.data,
            'course_id': form.course.data
        }
        url = f'{ob}api/subject-create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def get_all_courses():
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/get-courses')
        return r.json()

    @staticmethod
    def get_all_subjects():
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/get-subjects')
        return r.json()

    @staticmethod
    def get_nextPaper_code():
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/gen-paper-code')
        return r.json()

    @staticmethod
    def post_reg_paper(form):
        ob = StudiesClient.read_url_one()
        user_id = session['user'].get('id')
        payload = {
            'paper_no': form.papercode.data,
            'subject_id': form.subject.data,
            'no_of_questions': form.noquestion.data,
            'duration': form.duration.data,
            'user_id': user_id
        }
        url = f'{ob}api/paper-create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def get_papers():
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/load-paper')
        return r.json()

    @staticmethod
    def get_paper_detail(paper_no):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/get-paper-detail/{paper_no}')
        return r.json()

    @staticmethod
    def get_paper_det(paper_id):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/get-paper-det/{paper_id}')
        return r.json()

    @staticmethod
    def get_paper_det_nocondition(paper_no):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/get-paper-detail-no/{paper_no}')
        return r.json()

    @staticmethod
    def load_questions(paper_id):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/load-questions/{paper_id}')
        return r.json()

    @staticmethod
    def get_question(paper_id, question_ord):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/get-question/{paper_id}/{question_ord}')
        return r.json()

    @staticmethod
    def get_answer(question_id):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/get-answers/{question_id}')
        return r.json()

    @staticmethod
    def get_count_answer(paper_id):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/get-total-question/{paper_id}')
        return r.json()

    @staticmethod
    def publis_paper(paper_id):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/paper-publish/{paper_id}')
        return r.json()


    @staticmethod
    def update_question(question, answer, id):
        ob = StudiesClient.read_url_one()
        payload = {
            'question': question,
            'answer': answer,
            'id': id
        }
        url = f'{ob}api/update-question'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def delete_answer(question_id):
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/delete-answers/{question_id}')
        return r.json()

    @staticmethod
    def insert_answer(question, answer, answer_order):
        ob = StudiesClient.read_url_one()
        payload = {
            'question_id': question,
            'answer': answer,
            'answer_order': answer_order
        }
        url = f'{ob}api/answer/create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def insert_question(paper_id, question, question_order,points,correct_ans):
        ob = StudiesClient.read_url_one()
        payload = {
            'paper_id': paper_id,
            'question': question,
            'question_order': question_order,
            'points': points,
            'correct_ans': correct_ans,
        }
        url = f'{ob}api/question/create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def load_finished_papers():
        ob = StudiesClient.read_url_one()
        r = requests.get(f'{ob}api/load-finished-paper')
        return r.json()

    @staticmethod
    def get_exam_id():
        ob = StudiesClient.read_url_one()
        r = requests.get(f"{ob}api/get-exam-booking")
        return r.json()

    @staticmethod
    def book_exam(form):
        ob = StudiesClient.read_url_one()
        time_ = form.examtime.data
        time_ = time_+":00"
        getsecond = form.getsecond.data
        paperno = form.paperno.data
        from_time__ = datetime.datetime.strptime(time_, '%H:%M:%S').time()
        from_time = datetime.datetime.strptime(time_, '%H:%M:%S')

        from_ = datetime.datetime.timestamp(from_time)
        cal_time = from_ + (int(getsecond) / 60) * 60

        to_time = dt.fromtimestamp(cal_time).strftime('%H:%M:%S')

        diff = (cal_time - from_) / 3600

        result = StudiesClient.get_paper_det(paperno)
        subject_id = result.get('subject_id')
        paper_id = result.get('paperid')

        exam_id = StudiesClient.get_exam_id()
        payload = {
            'student_id' : form.studentid.data,
            'subject_id': form.subject_id.data,
            'exam_id': exam_id,
            'exam_date': form.examdate.data,
            'paper_id': paper_id,
            'start_time': from_time__,
            'end_time': to_time,
            'user_id': form.user_id.data,
        }

        url = f'{ob}api/exam-bookin'
        response = requests.request("POST", url=url, data=payload)
        return response