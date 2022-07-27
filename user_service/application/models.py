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