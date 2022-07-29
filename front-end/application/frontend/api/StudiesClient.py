import requests
from flask import session, request
import datetime
import time
from datetime import datetime as dt

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

    @staticmethod
    def get_papers():
        r = requests.get(f'http://127.0.0.1:5002/api/load-paper')
        return r.json()

    @staticmethod
    def get_paper_detail(paper_no):
        r = requests.get(f'http://127.0.0.1:5002/api/get-paper-detail/{paper_no}')
        return r.json()

    @staticmethod
    def get_paper_det(paper_id):
        r = requests.get(f'http://127.0.0.1:5002/api/get-paper-det/{paper_id}')
        return r.json()

    @staticmethod
    def get_paper_det_nocondition(paper_no):
        r = requests.get(f'http://127.0.0.1:5002/api/get-paper-detail-no/{paper_no}')
        return r.json()

    @staticmethod
    def load_questions(paper_id):
        r = requests.get(f'http://127.0.0.1:5002/api/load-questions/{paper_id}')
        return r.json()

    @staticmethod
    def get_question(paper_id, question_ord):
        r = requests.get(f'http://127.0.0.1:5002/api/get-question/{paper_id}/{question_ord}')
        return r.json()

    @staticmethod
    def get_answer(question_id):
        r = requests.get(f'http://127.0.0.1:5002/api/get-answers/{question_id}')
        return r.json()

    @staticmethod
    def get_count_answer(paper_id):
        r = requests.get(f'http://127.0.0.1:5002/api/get-total-question/{paper_id}')
        return r.json()

    @staticmethod
    def publis_paper(paper_id):
        r = requests.get(f'http://127.0.0.1:5002/api/paper-publish/{paper_id}')
        return r.json()


    @staticmethod
    def update_question(question, answer, id):
        payload = {
            'question': question,
            'answer': answer,
            'id': id
        }
        url = 'http://127.0.0.1:5002/api/update-question'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def delete_answer(question_id):
        r = requests.get(f'http://127.0.0.1:5002/api/delete-answers/{question_id}')
        return r.json()

    @staticmethod
    def insert_answer(question, answer, answer_order):
        payload = {
            'question_id': question,
            'answer': answer,
            'answer_order': answer_order
        }
        url = 'http://127.0.0.1:5002/api/answer/create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def insert_question(paper_id, question, question_order,points,correct_ans):
        payload = {
            'paper_id': paper_id,
            'question': question,
            'question_order': question_order,
            'points': points,
            'correct_ans': correct_ans,
        }
        url = 'http://127.0.0.1:5002/api/question/create'
        response = requests.request("POST", url=url, data=payload)
        return response

    @staticmethod
    def load_finished_papers():
        r = requests.get("http://127.0.0.1:5002/api/load-finished-paper")
        return r.json()

    @staticmethod
    def get_exam_id():
        r = requests.get("http://127.0.0.1:5002/api/get-exam-booking")
        return r.json()

    @staticmethod
    def book_exam(form):
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

        url = 'http://127.0.0.1:5002/api/exam-bookin'
        response = requests.request("POST", url=url, data=payload)
        return response