import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_resource():
    return "user resource works"

@users.route('/register', methods=["POST"])
def register():
    payload = request.get_json()

    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    print(payload)

    # check for unique email
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(
            data={},
            message="That email address is already in use.",
            status=401
        ), 401
    except models.DoesNotExist:
        pw_hash = generate_password_hash(payload['password'])
        created_user = models.User.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )
        print(created_user)

        login_user(created_user)

        # respond w/ new object and success message
        created_user_dict = model_to_dict(created_user)
        print(created_user_dict)
        
        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered!",
            status=201
        ), 201

