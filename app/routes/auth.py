from flask import Blueprint, request, jsonify, make_response

from app import db
from app.dto.auth import Auth
from app.models.user import Users # TODO burdan import edecek mi?

module = Blueprint("auth", __name__, url_prefix="/auth")


@module.route('/login', methods=['POST'])
def login():
    res = Auth().login(email=request.form['username'], password=request.form['password'])

    return res


@module.route('/logout', methods=['POST'])
def logout():
    res = Auth().logout()

    return res


@module.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # from app import Users  # TODO why should I import users HERE?
    user = Users.query.filter(Users.name == data['name']).first()

    if not data['password']:
        return make_response('Wrong password.', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

    if user:
        return make_response("The user is already exists.", 403,
                             {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

    new_user = Users(name=data['name'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registeration successfully'})# genelde boyle kullanilio!
