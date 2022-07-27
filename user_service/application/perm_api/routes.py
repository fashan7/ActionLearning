from . import perm_api_blueprint
from .. import db, login_manager
from ..models import Roles, User, Pageallocation, Userpriviledge, Branch, Useraddress, Course, Subjects, Paper_creation, \
    Studentregistration, Questions, Answers,  Examresults, Exambooking
from flask import make_response, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from passlib.hash import sha256_crypt

"""
use to reload the user object from the userid stored in session
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


"""
sometime we have to login users without using cookies 
such as using header values
or an API key args as a query argument, in this cases we have to use 
request_loader
"""

@perm_api_blueprint.route('/', methods=['GET'])
def workttest():
    return jsonify({'work':'hurray'})


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None


@perm_api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())
    response = jsonify(data)
    return response

#put User
@perm_api_blueprint.route('/api/users/update/<id>', methods=['PUT'])
def update_users(id):
    item = User.query.filter_by(id=id).first()
    if item is not None:
       # id = request.form['id']
       # username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address1 = request.form['address1']
        address2 = request.form['address2']
        address3 = request.form['address3']
        city = request.form['city']
        country = request.form['country']
        postal_code = request.form['postal_code']

        # password=request.form['password']

        #item.id = id
       # item.username = username
        item.email = email
        item.first_name = first_name
        item.last_name = last_name
        item.address1 = address1
        item.address2 = address2
        item.address3 = address3
        item.city = city
        item.country= country
        item.postal_code = postal_code


        # user.password = password
        db.session.commit()
        response = jsonify({'message': 'Successfully updated'})
    else:
        response = jsonify({'message': 'Cannot find branch'}), 404
    return response


    '''
    user = User.query.filter_by(id=id).first()
    id = request.form['id']
    username= request.form['username']
    email= request.form['email']
    first_name=request.form['first_name']
    last_name=request.form['last_name']
    #password=request.form['password']

    user.id = id
    user.username= username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    #user.password = password

    db.session.commit()
    response = jsonify({'message': 'Successfully updated'})
    return response

'''



def set_privilege(userid):
    pages = Pageallocation.query.all()

    for row in pages:
        item = Userpriviledge()
        json_data = row.to_json()
        page_id = json_data.get('id')

        item.user_id = userid
        item.pageallocation_id = page_id
        db.session.add(item)
        db.session.commit()
#put  Userpriviledge
@perm_api_blueprint.route('/api/set-priv/<user_id>', methods=['GET'])
def user_privilege(user_id):


   # items = Pageallocation.query.join(Userpriviledge).filter(Pageallocation.status.is_(True),

                                                                 # Userpriviledge.status.is_(True),
                                                                  #Userpriviledge.user_id == 3).order_by(Pageallocation.psection).with_entities(Pageallocation.psection.distinct(), Pageallocation.pposition)

    item = Userpriviledge.query.join(Pageallocation, Pageallocation.id == Userpriviledge.pageallocation_id).join(User, User.id == Userpriviledge.user_id).filter(Userpriviledge.user_id==user_id).with_entities(Userpriviledge.status, User.username, Pageallocation.name).all()
    print("Fashan",item)
    # if item is not None:
    #     #id = request.form['id']
    #     status= request.form['status']
    #     #pageallocation_id = request.form['pageallocation_id']
    #
    #     #item.id = id
    #     item.status = status
    #    # item.pageallocation_id= pageallocation_id
    #
    #     db.session.commit()
    #     response = jsonify({'message': 'Successfully updated'})
    # else:
    #     response = jsonify({'message': 'Cannot find '}), 404
    # return response
    return {'ms':23}





    # No returns since this method is called within a function


@perm_api_blueprint.route('/api/user/create', methods=['POST'])
def user_register():
    # Address Form
    address1 = request.form['address1']
    address2 = request.form['address2']
    address3 = request.form['address3']
    city = request.form['city']
    country = request.form['country']
    postal_code = request.form['postal_code']
    item_add = Useraddress()
    item_add.address1 = address1
    item_add.address2 = address2
    item_add.address3 = address3
    item_add.city = city
    item_add.country = country
    item_add.postal_code = postal_code
    db.session.add(item_add)
    db.session.commit()

    result = item_add.to_json()
    insert_addr_id = result.get('id')

    # USER FORM

    username = request.form['username']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    usertype = request.form['usertype']
    branch_id = request.form['branch_id']

    password = sha256_crypt.hash((str(request.form['password'])))

    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.username = username
    user.authenticated = True
    user.role_id = usertype
    user.address_id = insert_addr_id
    user.branch_id = branch_id

    db.session.add(user)
    db.session.commit()
    result = user.to_json()

    response = jsonify({'message': 'User added', 'result': result})

    # When User is created, Priviledges are set
    set_privilege(result.get('id'))
    return response






@perm_api_blueprint.route('/api/user/login', methods=['POST'])
def post_login():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        if sha256_crypt.verify(str(request.form['password']), user.password):
            user.encode_api_key()
            db.session.commit()
            login_user(user)

            return make_response(jsonify({'message': 'Logged in', 'api_key': user.api_key}))

    return make_response(jsonify({'message': 'Not logged in'}), 401)


@perm_api_blueprint.route('/api/user/logout', methods=['POST'])
def post_logout():
    if current_user.is_authenticated:
        logout_user()
        return make_response(jsonify({'message': 'You are logged out'}))
    return make_response(jsonify({'message': 'You are not logged in'}))


@perm_api_blueprint.route('/api/user/<username>/exists', methods=['GET'])
def get_username(username):
    item = User.query.filter_by(username=username).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'message': 'Cannot find username'}), 404
    return response


@login_required
@perm_api_blueprint.route('/api/user', methods=['GET'])
def get_user():
    if current_user.is_authenticated:
        return make_response(jsonify({'result': current_user.to_json()}))

    return make_response(jsonify({'message': 'Not logged in'})), 401

########################################################################################################################
@perm_api_blueprint.route('/api/user-roles', methods=['GET'])
def getall_usertypes():
    items = list()
    for row in Roles.query.all():
        items.append(row.to_json())

    response = jsonify({'data': items})
    return response

#userrole
@perm_api_blueprint.route('/api/user-roles/create', methods=['POST'])
def usertype_create():
    name = request.form['name']
    item = Roles()
    item.name = name

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Role added', 'Role Data': item.to_json()})
    return response


@perm_api_blueprint.route('/api/user-role/<id>', methods=['GET'])
def usertype_get(id):
    item = Roles.query.filter_by(id=id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find a role'}), 404
    return response

@perm_api_blueprint.route('/api/user-role-delete/<id>', methods=['DELETE'])
def usertype_delete(id):
    item = Roles.query.filter_by(id=id).first()
    if item is not None:
        db.session.delete(item)
        db.session.commit()
        # response= jsonify(item.to_delete)
        response = jsonify({'message': 'Successfully deleted'})
    else:
        response = jsonify({'message': 'Cannot find a role'}), 404
    return response

@perm_api_blueprint.route('/api/user-role-update/<id>', methods=['PUT'])
def usertype_update(id):
    item = Roles.query.filter_by(id=id).first()
    if item is not None:
        name= request.form['name']
        item.name = name
        db.session.commit()
        response = jsonify({'message': 'Successfully updated'})
    else:
        response = jsonify({'message': 'Cannot find role'}), 404
    return response
########################################################################################################################
#pagealloc
@perm_api_blueprint.route('/api/page-alloc/create', methods=['POST'])
def page_allocate_create():
    route = request.form['route']
    name = request.form['name']
    image = request.form['image']
    psection = request.form['psection']
    ssection = request.form['ssection']
    pposition = request.form['pposition']
    sposition = request.form['sposition']

    item = Pageallocation()
    item.route = route
    item.name = name
    item.image = image
    item.psection = psection
    item.ssection = ssection
    item.pposition = pposition
    item.sposition = sposition

    db.session.add(item)
    db.session.commit()
    response = jsonify({'message': 'saved successfully'}), 200
    return response


@perm_api_blueprint.route('/api/pages', methods=['GET'])
def getall_pages():
    items = list()
    for row in Pageallocation.query.all():
        items.append(row.to_json())

    response = jsonify({'data': items})
    return response




@perm_api_blueprint.route('/api/get-section-postion/<user_id>', methods=['GET'])
def get_pages_sections(user_id):
    # TODO hardcode infuture will implement to make dynamic after the login page implemented
    raw_query = f"SELECT DISTINCT pageallocation.psection, pageallocation.pposition AS pageallocation_pposition, (SELECT count(p.id) FROM pageallocation p where p.psection = pageallocation.psection) AS countP FROM pageallocation JOIN userpriviledge ON pageallocation.id = userpriviledge.pageallocation_id WHERE pageallocation.status IS true AND userpriviledge.status IS true AND userpriviledge.user_id = {user_id} ORDER BY pageallocation.psection"
    items = db.session.execute(raw_query)

    # items = Pageallocation.query.join(Userpriviledge).filter(Pageallocation.status.is_(True),
    #                                                          Userpriviledge.status.is_(True),
    #                                                          Userpriviledge.user_id == 3).order_by(Pageallocation.psection).with_entities(Pageallocation.psection.distinct(), Pageallocation.pposition)
    if items is not None:
        data = list()
        for x, row in enumerate(items, start=1):
            data.append({str(row[1]): row[0], "count": row[2]})
        response = jsonify(data), 200
    else:
        response = jsonify({'message': 'Not Pages to Find'}), 404
    return response


@perm_api_blueprint.route('/api/get-subsection/<user_id>/<section_id>')
def get_subsection(user_id, section_id):
    item = Userpriviledge.query.join(Pageallocation, Pageallocation.id == Userpriviledge.pageallocation_id).join(User,
                                                                                                                 User.id == Userpriviledge.user_id).filter(
        Pageallocation.psection == section_id, Pageallocation.status.is_(True),
        Userpriviledge.user_id == user_id).order_by(Pageallocation.sposition).with_entities(Pageallocation.name,
                                                                                            Userpriviledge.status,
                                                                                            Userpriviledge.id,
                                                                                            Pageallocation.image)
    if item is not None:
        data = list()
        for row in item:
            data.append({'sub_section_name': row[0], 'status': row[1], 'user_priv_id': row[2], 'image': row[3]})
        response = jsonify(data), 200
    else:
        response = jsonify({'message': 'Not Sub Section to Find'}), 404
    return response


@perm_api_blueprint.route('/api/relate-page/<section>', methods=['GET'])
def related_page(section):
    item = Pageallocation.query.filter(Pageallocation.psection == section).all()
    if item is not None:
        items = list()
        for row in item:
            items.append(row.to_json())
        response = jsonify({'data': items})
    else:
        response = jsonify({'message': 'Cannot find Sub Section'}), 404
    return response


@perm_api_blueprint.route('/api/getall-branch', methods=['GET'])
def getall_branchs():
    items = list()
    for row in Branch.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response
#########################################################################################################################
#bracnh
@perm_api_blueprint.route('/api/branch/create', methods=['POST'])
def branch_create():
    name = request.form['name']
    item = Branch()
    item.name = name

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Branch added', 'branch': item.to_json()})
    return response


@perm_api_blueprint.route('/api/get-branch/<id>', methods=['GET'])
def branch_get(id):
    item = Branch.query.filter_by(id=id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find branch'}), 404
    return response

@perm_api_blueprint.route('/api/delete-branch/<id>', methods=['DELETE'])
def branch_delete(id):
    item = Branch.query.filter_by(id=id).first()
    if item is not None:
        db.session.delete(item)
        db.session.commit()
        #response= jsonify(item.to_delete)
        response = jsonify({'message':'Successfully deleted'})
    else:
        response = jsonify({'message': 'Cannot find branch'}), 404
    return response

@perm_api_blueprint.route('/api/update-branch/<id>', methods=['PUT'])
def branch_put(id):
    item = Branch.query.filter_by(id=id).first()
    if item is not None:
        name = request.form['name']
        #item = request.form['item']
        item.name = name
       # item.item = item
        db.session.commit()
        #response= jsonify(item.to_de)
        response = jsonify({'message':'Successfully updated'})
    else:
        response = jsonify({'message': 'Cannot find branch'}), 404
    return response
########################################################################################################################
#Course
@perm_api_blueprint.route('/api/course/create', methods=['POST'])
def course_create():
    course_name = request.form['course_name']
    course_semester = request.form['course_semester']
   # status = request.form['status']
   # id = request.form['id']
    item = Course()
    item.course_name = course_name
    item.course_semester = course_semester
   # item.status = status
    #item.id = id

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'course added', 'course': item.to_json()})
    return response

@perm_api_blueprint.route('/api/course/update/<id>', methods=['PUT'])
def course_update(id):
    item = Course.query.filter_by(id=id).first()
    if item is not None:
        course_name = request.form['course_name']
        course_semester = request.form['course_semester']

        item.course_name = course_name
        item.course_semester= course_semester

        db.session.commit()
        # response= jsonify(item.to_de)
        response = jsonify({'message': 'Successfully updated'})
    else:
        response = jsonify({'message': 'Cannot find course'}), 404
    return response

#get
@perm_api_blueprint.route('/api/course/get/<id>', methods=['GET'])
def course_get(id):
    item = Course.query.filter_by(id=id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find course'}), 404
    return response

#getall
@perm_api_blueprint.route('/api/course/getall', methods=['GET'])
def getall_course():
    items = list()
    for row in Course.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response

#Delete
@perm_api_blueprint.route('/api/course/delete/<id>', methods=['Delete'])
def delete_course(id):
    item = Course.query.filter_by(id=id).first()
    if item is not None:
        db.session.delete(item)
        db.session.commit()
        # response= jsonify(item.to_delete)
        response = jsonify({'message': 'Successfully deleted'})
    else:
        response = jsonify({'message': 'Cannot find course'}), 404
    return response
#########################################################################################################################
#subjects
@perm_api_blueprint.route('/api/create/subj', methods=['Post'])
def subject_create():
    name = request.form['name']
    course_id = request.form['course_id']
    # status = request.form['status']
    # id = request.form['id']
    item = Subjects()
    item.name = name
    item.course_id= course_id
    # item.status = status
    # item.id = id

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'subject added', 'subject': item.to_json()})
    return response


@perm_api_blueprint.route('/api/update/<id>', methods=['PUT'])
def sub_update(id):
    item = Subjects.query.filter_by(id=id).first()
    if item is not None:
        name = request.form['name']
        course_id = request.form['course_id']

        item.name = name
        item.course_id= course_id

        db.session.commit()
        # response= jsonify(item.to_de)
        response = jsonify({'message': 'Successfully updated'})
    else:
        response = jsonify({'message': 'Cannot find subject'}), 404
    return response

@perm_api_blueprint.route('/api/get/<id>', methods=['GET'])
def subject_get(id):
    item = Subjects.query.filter_by(id=id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find subject'}), 404
    return response

@perm_api_blueprint.route('/api/getall', methods=['GET'])
def subject_all():
    items = list()
    for row in Subjects.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response

@perm_api_blueprint.route('/api/sub/delete/<id>', methods=['DELETE'])
def subject_delete():
    item = Subjects.query.filter_by(id=id).first()
    if item is not None:
        db.session.delete(item)
        db.session.commit()
        # response= jsonify(item.to_delete)
        response = jsonify({'message': 'Successfully deleted'})
    else:
        response = jsonify({'message': 'Cannot find subject'}), 404
    return response

##########################################################################################################################
#paper-creation
@perm_api_blueprint.route('/api/paper-create', methods=['Post'])
def paper_create():
    paper_id = request.form['paper_id']
    subject_id = request.form['subject_id']
    duration = request.form['duration']
    no_of_questions = request.form['no_of_questions']
    paper_no= request.form['paper_no']
   # status = request.form['status']
    user_id = request.form['user_id']

    item = Paper_creation()

    item.paper_id = paper_id
    item.subject_id = subject_id
    item.duration = duration
    item.no_of_questions= no_of_questions
    item.paper_no =paper_no
   # item.status=status
    item.user_id=user_id

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'paper created', 'paper-create': item.to_json()})
    return response


@perm_api_blueprint.route('/api/paper-get/<paper_id>', methods=['GET'])
def getbyid(paper_id):
    item = Paper_creation.query.filter_by(paper_id=paper_id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find paper'}), 404
    return response

@perm_api_blueprint.route('/api/paper-getall', methods=['GET'])
def getallpaper():
    items = list()
    for row in Paper_creation.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response

@perm_api_blueprint.route('/api/paper-update', methods=['PUT'])
def paper_update(id):
    item = Paper_creation.query.filter_by(id=id).first()
    if item is not None:
        paper_id = request.form['paper_id']
        subject_id = request.form['subject_id']
        duration = request.form['duration']
        no_of_questions = request.form['no_of_questions']
        paper_no = request.form['paper_no']
        # status = request.form['status']
        user_id = request.form['user_id']


        item.paper_id = paper_id
        item.subject_id = subject_id
        item.duration = duration
        item.no_of_questions = no_of_questions
        item.paper_no = paper_no
        # item.status=status
        item.user_id = user_id

        db.session.commit()
        # response= jsonify(item.to_de)
        response = jsonify({'message': 'Successfully updated'})
    else:
        response = jsonify({'message': 'Cannot find paper'}), 404
    return response

###################################################################################################################################
#studentregisteration
@perm_api_blueprint.route('/api/student/registration/', methods=['POST'])
def Student_registration():
    name = request.form['name']
    code = request.form['code']
    roll_number = request.form['roll_number']
    student_address = request.form['student_address']
    gender = request.form['gender']
    date_of_birth = request.form['date_of_birth']
    parent_name = request.form['parent_name']
    parent_address = request.form['parent_address']
    parent_mobile_number = request.form['parent_mobile_number']
    parent_landline = request.form['parent_landline']
    parent_email = request.form['parent_email']
    old_school_name = request.form['old_school_name']
    old_school_grade = request.form['old_school_grade']
    old_school_joined = request.form['old_school_joined']
    old_school_left = request.form['old_school_left']
    datetime = request.form['datetime']
    active = request.form['active']
    grade = request.form['grade']
    join_date = request.form['join_date']
    blood_group = request.form['blood_group']
    nationality = request.form['nationality']
    student_email = request.form['student_email']
    item_add = Studentregistration()
    item_add.name = name
    item_add.code = code
    item_add.roll_number = roll_number
    item_add.student_address = student_address
    item_add.gender = gender
    item_add.date_of_birth = date_of_birth
    item_add.parent_name = parent_name
    item_add.parent_address = parent_address
    item_add.parent_mobile_number = parent_mobile_number
    item_add.parent_landline = parent_landline
    item_add.parent_email = parent_email
    item_add.old_school_name = old_school_name
    item_add.old_school_grade = old_school_grade
    item_add.old_school_joined = old_school_joined
    item_add.old_school_left = old_school_left
    item_add.datetime = datetime
    if active is 'True'or 'true':
        item_add.active = True
    else:
        item_add.active= False
    item_add.grade = grade
    item_add.join_date = join_date
    item_add.blood_group = blood_group
    item_add.nationality = nationality
    item_add.student_email = student_email
    # item_add.studentattendance =studentattendance
    db.session.add(item_add)
    db.session.commit()
    result = item_add.to_json()
    return result
@perm_api_blueprint.route('/api/get-student/<id>', methods=['GET'])
def student_get(id):
    item = Studentregistration.query.filter_by(id=id).first()
    if item is not None:
        response1 = jsonify(item.to_json())
    else:
        response1 = jsonify({'message': 'can not find Student'}), 404
    return response1
@perm_api_blueprint.route('/api/putstudentR/<id>', methods=['PUT'])
def st_put(id):
    item = Studentregistration.query.filter_by(id=id).first()
    if item is not None:
        name = request.form['name']
        code = request.form['code']
        roll_number = request.form['roll_number']
        student_address = request.form['student_address']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        parent_name = request.form['parent_name']
        parent_address = request.form['parent_address']
        parent_mobile_number = request.form['parent_mobile_number']
        parent_landline = request.form['parent_landline']
        parent_email = request.form['parent_email']
        old_school_name = request.form['old_school_name']
        old_school_grade = request.form['old_school_grade']
        old_school_joined = request.form['old_school_joined']
        old_school_left = request.form['old_school_left']
        datetime = request.form['datetime']
        active = request.form['active']
        grade = request.form['grade']
        join_date = request.form['join_date']
        blood_group = request.form['blood_group']
        nationality = request.form['nationality']
        student_email = request.form['student_email']
        item.name = name
        item.code = code
        item.roll_number = roll_number
        item.student_address = student_address
        item.gender = gender
        item.date_of_birth = date_of_birth
        item.parent_name = parent_name
        item.parent_address = parent_address
        item.parent_mobile_number = parent_mobile_number
        item.parent_landline = parent_landline
        item.parent_email = parent_email
        item.old_school_name = old_school_name
        item.old_school_grade = old_school_grade
        item.old_school_joined = old_school_joined
        item.old_school_left = old_school_left
        item.datetime = datetime
        item.active = active
        item.grade = grade
        item.join_date = join_date
        item.blood_group = blood_group
        item.nationality = nationality
        item.student_email = student_email
        db.seesion.update(item)
        db.session.commit()
        response = jsonify({"message": "updated student data"})
    else:
        response = jsonify({"message": "can not find student details"})
    return response

@perm_api_blueprint.route('/api/del-std/<id>', methods=['PUT'])
def student_delet(id):
    item = Studentregistration.query.filter_by(id=id).first()
    if item is not None:
        active = request.form['active']
        if active is 'false' or 'False':
            item.active = False
        db.session.add(item)
        db.session.commit()
        response = jsonify({'message': 'deletion completed'})
    else:
        response = jsonify({'message': 'can not find Student'}), 404
    return response
##########################################################################################################################
#question
@perm_api_blueprint.route('/api/ques/create/', methods=['POST'])
def question_create():
    question_id = request.form['question_id']
    paper_id = request.form['paper_id']
    question = request.form['question']
    question_order = request.form['question_order']
    points = request.form['points']
    correct_ans = request.form['correct_ans']

    item = Questions()


    item.question_id = question_id
    item.paper_id = paper_id
    item.question = question
    item.question_order = question_order
    item.points = points
    item.correct_ans = correct_ans

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Question created', 'questions': item.to_json()})
    return response

@perm_api_blueprint.route('/api/ques/update/', methods=['PUT'])
def question_update():
    item = Questions.query.filter_by(id=id).first()
    if item is not None:
        question_id = request.form['question_id']
        paper_id = request.form['paper_id']
        question = request.form['question']
        question_order = request.form['question_order']
        points = request.form['points']
        correct_ans = request.form['correct_ans']

        item.question_id = question_id
        item.paper_id = paper_id
        item.question = question
        item.question_order = question_order
        item.points = points
        item.correct_ans = correct_ans

        db.session.commit()
        # response= jsonify(item.to_de)
        response = jsonify({'message': 'Successfully updated'})
    else:
        response = jsonify({'message': 'Cannot find question'}), 404
    return response

@perm_api_blueprint.route('/api/ques/get/<question_id>', methods=['GET'])
def getquesbyid(question_id):
    item = Questions.query.filter_by(question_id=question_id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find subject'}), 404
    return response

@perm_api_blueprint.route('/api/ques/getall', methods=['GET'])
def getallques():
    items = list()
    for row in Questions.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response

##########################################################################################################################
#answer
@perm_api_blueprint.route('/api/ans/create/', methods=['POST'])
def answer_create():
    answer_id = request.form['answer_id']
    question_id = request.form['question_id']
    answer = request.form['answer']
    answer_order = request.form['answer_order']
    #status = request.form['status']


    item = Answers()


    item.question_id = question_id
    item.answer_id = answer_id
    item.answer= answer
    item.answer_order = answer_order

    #item.status = status

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Answer created', 'Answer': item.to_json()})
    return response

@perm_api_blueprint.route('/api/ans/update/<answer_id>', methods=['PUT'])
def answer_update(answer_id):
    item = Answers.query.filter_by(id=id).first()
    if item is not None:
        answer_id = request.form['answer_id']
        question_id = request.form['question_id']
        answer = request.form['answer']
        answer_order = request.form['answer_order']

        item.question_id = question_id
        item.answer_id = answer_id
        item.answer = answer
        item.answer_order = answer_order

        db.session.commit()
        response = jsonify({'message': 'Successfully updated'})
    else:
        response = jsonify({'message': 'Cannot find question'}), 404
    return response

@perm_api_blueprint.route('/api/ans/get/<answer_id>', methods=['GET'])
def get_ans_byID(answer_id):
    item = Answers.query.filter_by(answer_id=answer_id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find subject'}), 404
    return response

@perm_api_blueprint.route('/api/ans/getall', methods=['GET'])
def getall_ans():
    items = list()
    for row in Answers.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response


########################################################################################################################
#exambooking
@perm_api_blueprint.route('/api/exm-book/create/', methods=['POST'])
def exm_book():
    #id = request.form['id']
    exam_id = request.form['exam_id']
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    exam_date =request.form['exam_date']
    start_time= request.form['start_time']
    end_time = request.form['end_time']
    user_id = request.form['user_id']

    item = Exambooking()
   # item.id = id
    item.exam_id = exam_id
    item.student_id = student_id
    item.subject_id = subject_id
    item.exam_date = exam_date
    item.start_time = start_time
    item.end_time  = end_time
    item.user_id = user_id

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Exam-booking created', 'Exam-booking': item.to_json()})
    return response

@perm_api_blueprint.route('/api/exm-book/get/<id>', methods=['GET'])
def getexambook(id):
    item = Exambooking.query.filter_by(id=id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find exam'}), 404
    return response

@perm_api_blueprint.route('/api/exm-book/getall', methods=['GET'])
def getexambookall():
    items = list()
    for row in Exambooking.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response

@perm_api_blueprint.route('/api/exm-book/delete/<id>', methods=['DELETE'])
def deleteexm(id):
    item = Exambooking.query.filter_by(id=id).first()
    if item is not None:
        db.session.delete(item)
        db.session.commit()
        # response= jsonify(item.to_delete)
        response = jsonify({'message': 'Successfully deleted'})
    else:
        response = jsonify({'message': 'Cannot find exam'}), 404
    return response

########################################################################################################################
#examresult
@perm_api_blueprint.route('/api/exm-result/create', methods=['POST'])
def examresult():
    student_id = request.form['student_id']
    exam_id = request.form['exam_id']
    exam_log = request.form['exam_log']
    results = request.form['results']
    marks = request.form['marks']
    #id =  request.form['id']

    item = Examresults()
    # item.id = id
    item.student_id = student_id
    item.exam_id = exam_id
    item.exam_log = exam_log
    item.results = results
    item.marks = marks


    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Exam-result created', 'Exam-result': item.to_json()})
    return

@perm_api_blueprint.route('/api/exm-result/get/<id>', methods=['GET'])
def getresult(id):
    item = Examresults.query.filter_by(id=id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find result'}), 404
    return response

@perm_api_blueprint.route('/api/exm-result/getall', methods=['GET'])
def getresultall():
    items = list()
    for row in Examresults.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response