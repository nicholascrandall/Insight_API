from flask_login.utils import logout_user
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
            message="Successfully registered!",
            status=201
        ), 201

@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['username'] = payload['username'].lower()
    print(payload)

    # lookup user by email

    try:
        user = models.User.get(models.User.username == payload['username'])

        # if the user exists
        user_dict = model_to_dict(user)
        password_correct = check_password_hash(user_dict['password'], payload['password'])

        if (password_correct):
            login_user(user)
            user_dict.pop('password')

            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['username']}",
                status=200
            ), 200
        else:
            print('pw is no good')
            return jsonify(
                data={},
                message="Username or password is incorrect",
                status=401
            ), 401
    except models.DoesNotExist:
        print("Username not found")
        return jsonify(
            data={},
            message="Username or password is incorrect",
            status=401
        ), 401

@users.route('/logout', methods=['GET'])
def logout():
    logout_user()

    return jsonify(
        data={},
        status=200,
        message="Successfully logged out"
    ), 200