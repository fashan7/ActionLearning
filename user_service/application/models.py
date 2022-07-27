from . import db
import datetime as dt
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.Boolean, default=True)
    user = db.relationship('User', uselist=False, backref="roles")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    date_reg = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('useraddress.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    userpriv = db.relationship('Userpriviledge', uselist=False, backref="User")

    def encode_api_key(self):
        self.api_key = sha256_crypt.hash(self.username + str(datetime.utcnow))

    def encode_password(self):
        self.password = sha256_crypt.hash(self.password)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'api_key': self.api_key,
            'is_active': True,
            'is_admin': self.is_admin
        }


class Useraddress(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address1 = db.Column(db.String(255), unique=False, nullable=False)
    address2 = db.Column(db.String(255), unique=False, nullable=True)
    address3 = db.Column(db.String(255), unique=False, nullable=True)
    city = db.Column(db.String(100), unique=False, nullable=False)
    country = db.Column(db.String(100), unique=False, nullable=False)
    postal_code = db.Column(db.String(100), unique=False, nullable=False)
    user = db.relationship('User', uselist=False, backref="useraddress")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'address1': self.address1,
            'address2': self.address2,
            'address3': self.address3,
            'city': self.city,
            'country': self.country,
            'postal_code': self.postal_code,
        }


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.Boolean, default=True)
    user = db.relationship('User', uselist=False, backref="branch")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'branch_id': self.id,
            'branch_name': self.name
        }


class Pageallocation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route = db.Column(db.String(255), unique=False, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    image = db.Column(db.String(255), unique=False, nullable=True)
    psection = db.Column(db.String(100), unique=False, nullable=False)
    ssection = db.Column(db.String(100), unique=False, nullable=False)
    pposition = db.Column(db.Integer, unique=False, nullable=False)
    sposition = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.Boolean, default=True)
    userpriv = db.relationship('Userpriviledge', uselist=False, backref="pageallocation")

    def __repr__(self):
        return '<route {}>'.format(self.route)

    def to_json(self):
        return {
            'id': self.id,
            'route': self.route,
            'name': self.name,
            'image': self.image,
            'psection': self.psection,
            'ssection': self.ssection,
            'pposition': self.pposition,
            'sposition': self.sposition
        }


class Userpriviledge(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pageallocation_id = db.Column(db.Integer, db.ForeignKey('pageallocation.id'), nullable=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'page_id': self.pageallocation_id
        }

class Course(db.Model):
    course_name = db.Column(db.String(100),unique=False, nullable=False)
    course_semester = db.Column(db.String(100),unique=False, nullable=False)
    status = db.Column(db.Boolean,default=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subfk = db.relationship('Subjects', uselist=False, backref="course")
    def __repr__(self):
        return '<status {}>'.format(self.status)

    def to_json(self):
        return{
            'course_name':self.course_name,
            'course_semester':self.course_semester,
            'status':self.status,
            'id':self.id
        }

class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.Boolean, default=True)


    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return{
            'id': self.id,
            'course_id': self.course_id,
            'name': self.name,
            'status': self.status
        }

class Staffstructure(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.Boolean, default=True)
    staff_relation = db.relationship('Staff', uselist=False, backref="staffstructure")


    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    gender = db.Column(db.String(255), unique=False, nullable=True)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    mobile = db.Column(db.String(255), unique=False, nullable=True)
    joining_date = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    department_id = db.Column(db.Integer, db.ForeignKey('staffstructure.id'), nullable=False)

    def __repr__(self):
        return '<id %r>' % (self.id)

    def to_json(self):
        return {
            'id': self.id,
            'is_active': True,
            'gender': self.gender,
            'mobile': self.mobile,
            'department_id': self.department_id,
            'username': self.username
        }

class Studentregistration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    code = db.Column(db.String(100), unique=True, nullable=False)
    roll_number = db.Column(db.String(100), unique=True, nullable=False)
    student_address = db.Column(db.String(100), unique=False, nullable=False)
    gender = db.Column(db.String(15), unique=False, nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    parent_name = db.Column(db.String(100), unique=False, nullable=False)
    parent_address = db.Column(db.String(100), unique=False, nullable=False)
    parent_mobile_number = db.Column(db.String(15), unique=False, nullable=False)
    parent_landline = db.Column(db.String(15), unique=False, nullable=False)
    parent_email = db.Column(db.String(30), unique=False, nullable=True)
    old_school_name = db.Column(db.String(30), unique=False, nullable=False)
    old_school_grade = db.Column(db.String(100), unique=False, nullable=False)
    old_school_joined = db.Column(db.DateTime, unique=False, nullable=False)
    old_school_left = db.Column(db.DateTime, unique=False, nullable=False)
    datetime = db.Column(db.DateTime, unique=False, nullable=False)
    active = db.Column(db.Boolean, default=True, unique=False, nullable=False)
    grade = db.Column(db.Integer, unique=False, nullable=False)
    join_date = db.Column(db.DateTime, unique=False, nullable=False)
    blood_group = db.Column(db.String(100), unique=False, nullable=False)
    nationality = db.Column(db.String(100), unique=False, nullable=False)
    student_email = db.Column(db.String(100), unique=False, nullable=False)
    studentattendances = db.relationship('Studentattendance', uselist=False, backref="studentregistration")
    studentfee = db.relationship('Studentfee', uselist=False, backref="studentregistration")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'roll_number': self.roll_number,
            'student_address': self.student_address,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth,
            'parent_name': self.parent_name,
            'parent_address': self.parent_address,
            'parent_mobile_number': self.parent_mobile_number,
            'parent_landline': self.parent_landline,
            'parent_email': self.parent_email,
            'old_school_name': self.old_school_name,
            'old_school_grade': self.old_school_grade,
            'old_school_joined': self.old_school_joined,
            'old_school_left': self.old_school_left,
            'datetime': self.datetime,
            'active': self.active,
            'grade': self.grade,
            'join_date': self.join_date,
            'blood_group': self.blood_group,
            'nationality': self.nationality,
            'student_email': self.student_email
        }


class Studentattendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_code = db.Column(db.String(100), unique=False, nullable=False)
    student_name = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    day = db.Column(db.String(100), unique=False, nullable=False)
    month = db.Column(db.String(100), unique=False, nullable=False)
    year = db.Column(db.String(100), unique=False, nullable=False)
    attendance = db.Column(db.String(100), unique=False, nullable=False)
    remarks = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.Boolean, default=True, unique=False, nullable=False)
    grade = db.Column(db.Integer, unique=False, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('studentregistration.id'), nullable=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):

        return {
            'id': self.id,
            'student_code': self.student_code,
            'student_name': self.student_name,
            'student_id': self.student_id,
            'date': self.date,
            'day': self.day,
            'month': self.month,
            'year': self.year,
            'attendance': self.attendance,
            'remarks': self.remarks,
            'status': self.status,
            'grade': self.grade
        }


class Studentfee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fee_type_id = db.Column(db.String(100), unique=True, nullable=False)
    student_name = db.Column(db.String(100), unique=False, nullable=False)
    pay_date = db.Column(db.DateTime,  nullable=False)
    actual_amount = db.Column(db.FLOAT, unique=False, nullable=False)
    pay_amount = db.Column(db.FLOAT, unique=False, nullable=False)
    balance_amount = db.Column(db.FLOAT, unique=False, nullable=False)
    total_amount = db.Column(db.FLOAT, unique=False, nullable=False)
    fine = db.Column(db.FLOAT, unique=False, nullable=False)
    prefix = db.Column(db.String(100), unique=False, nullable=False)
    individual_receipt = db.Column(db.String(100), unique=False, nullable=False)
    receipt_number = db.Column(db.String(100), unique=False, nullable=False)
    mode_of_pay = db.Column(db.String(100), unique=False, nullable=False)
    bank = db.Column(db.String(100), nullable=False)
    cheque_number = db.Column(db.String(100), unique=True, nullable=False)
    cheque_date = db.Column(db.DateTime, nullable=False)

    remark = db.Column(db.String(100), unique=True, nullable=False)

    status = db.Column(db.Boolean, unique=False, nullable=False)
    active = db.Column(db.Boolean, unique=False, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('studentregistration.id'), nullable=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'id':self.id,
            'student_id': self.student_id,
            'fee_type_id': self.fee_type_id,
            'student_name': self.student_name,
            'pay_date': self.pay_date,
            'actual_amount': self.actual_amount,
            'pay_amount': self.pay_amount,
            'balance_amount': self.balance_amount,
            'total_amount': self.total_amount,
            'fine': self.fine,
            'prefix': self.prefix,
            'individual_receipt': self.individual_receipt,
            'receipt_number': self.receipt_number,
            'mode_of_pay': self.mode_of_pay,
            'bank': self.bank,
            'cheque_number': self.cheque_number,
            'cheque_date': self.cheque_date,
            'remark': self.remark,
            'status': self.status,
            'active': self.active
        }