from . import db
import datetime as dt
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB


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


class Staffstructure(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
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
    subfk = db.relationship('Subjects', uselist=False, backref="Course")
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

class Staff(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255), unique=False, nullable=True)
    address = db.Column(db.String(255), unique=False, nullable=True)
    gender = db.Column(db.String(255), unique=False, nullable=True)
    date_of_birth = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    mobile = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=True)
    joining_date = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<id %r>' % (self.id)

    def to_json(self):
        return {
            'full_name': self.full_name,
            'email': self.email,
            'id': self.id,
            'is_active': True,

        }

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recommendation = db.Column(db.String(255), unique=False, nullable=True)
    output = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<id %r>' % (self.id)

    def to_json(self):
        return {
            'recommendation': self.recommendation,
            'output': self.output

        }

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feedback = db.Column(db.String(255), unique=False, nullable=True)
    output = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<id %r>' % (self.id)

    def to_json(self):
        return {
            'feedback': self.feedback,
            'output': self.output

        }



class MultinomialNB:
    def __init__(self, articles_per_tag):
        self.alpha = 1
        self.priors_per_tag = {}
        self.likelyhood_per_word_per_tag = {}
        self.articles_per_tag = articles_per_tag
        self.tags = articles_per_tag.keys()
        self.train()

    def train(self):

        tag_counts_map = {tag: len(self.articles_per_tag[tag]) for tag in self.tags}  ### number of lists per tag

        self.priors_per_tag = {tag: tag_counts_map[tag] / sum(tag_counts_map.values()) for tag in
                               self.tags}  ## prob of lists globally

        self.likelyhood_per_word_per_tag = self.alternativeFunction()

    def predict(self, article):

        prob_per_tag = {tag: math.log(prior) for tag, prior in self.priors_per_tag.items()}

        for word in article:

            for tag in self.tags:

                if word in self.likelyhood_per_word_per_tag.keys():
                    prob_per_tag[tag] = prob_per_tag[tag] + math.log(self.likelyhood_per_word_per_tag[word][tag])

        return prob_per_tag

    ##############################################################################################################

    def alternativeFunction(self):

        wordFreq_perTag = {}

        totalWordsPerTag = {}

        for tag in self.tags:

            totalWordsPerTag[tag] = 0

            countVar = 0

            for article in self.articles_per_tag[tag]:

                for word in article:

                    countVar = countVar + 1

                    if word not in wordFreq_perTag.keys():

                        wordFreq_perTag[word] = {}

                        wordFreq_perTag[word][tag] = 1;

                    else:

                        if tag in wordFreq_perTag[word].keys():

                            wordFreq_perTag[word][tag] = wordFreq_perTag[word][tag] + 1;
                        else:
                            wordFreq_perTag[word][tag] = 1;

            totalWordsPerTag[tag] = countVar

        for val in wordFreq_perTag.keys():

            for tag in self.tags:

                if tag in wordFreq_perTag[val].keys():

                    wordFreq_perTag[val][tag] = (wordFreq_perTag[val][tag] + 1) / (totalWordsPerTag[tag] + 2)

                else:

                    wordFreq_perTag[val][tag] = 1 / (totalWordsPerTag[tag] + 2)

        return wordFreq_perTag

class NLP:

    def commonFunc(ipStr):
        review = re.sub('[^a-zA-Z]', ' ', ipStr)
        review = review.lower()
        review = review.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
        review = ' '.join(review)

        return review

