from . import perm_api_blueprint
from .. import db, login_manager
from ..models import Roles, User, Pageallocation, Userpriviledge, Branch, Useraddress
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


@perm_api_blueprint.route('/api/user-roles', methods=['GET'])
def getall_usertypes():
    items = list()
    for row in Roles.query.all():
        items.append(row.to_json())

    response = jsonify({'data': items})
    return response


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
