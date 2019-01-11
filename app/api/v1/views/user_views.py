from flask import Blueprint, request, jsonify, make_response

USERVIEW =Blueprint('USERVIEW',__name__)

@USERVIEW.route('/signin', methods =['POST'])
def landing():
    """This is the login method"""
    data = request.get_json()
    username = data['username']
    email = data['email']

    return make_response(jsonify({
        "status": "ok",
        "username": username,
        "email": email
    }), 201)