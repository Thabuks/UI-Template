
from flask import Blueprint, request, jsonify
import datetime
from app.api.v1.models.models import Users
from app.api.v1.utils.validations import UserValidation

time_now = datetime.datetime.now()

userviews = Blueprint('userviews', __name__)


@userviews.route("/signup", methods=["POST"])
def user_signup():
    try:
        data = request.get_json()
        validate = UserValidation(data)

        if not data:
            return jsonify({"status": 204, "error": "Such data not found"}), 204

        all_fields_filled = validate.all_required_fields_signup()
        if not all_fields_filled:
            return jsonify({"status": 400, "error": "KIndly input all fields(firstName, lastName, userName, email, phone and password)"}), 400

        fields_empty = validate.empty_fields_signup()
        if fields_empty.lstrip() != "It can't be empty!!":
            return jsonify({"status": 422, "error": fields_empty}), 422

        username_matches = validate.valid_username()
        if not username_matches:
            return jsonify({"status": 400, "error": "The username will either contain: a number,letter and _"}), 400

        username_exist = validate.username_exists()
        if username_exist:
            return jsonify({"status": 409, "error": "user already exists"}), 409

        valid_email = validate.valid_email()
        if not valid_email:
            return jsonify({"status": 400, "error": "invalid email format"}), 400

        valid_password = validate.valid_password()
        if valid_password != 1:
            return jsonify({"status": 400, "error": valid_password}), 400

        new_user = validate.add_default_fields()

        Users.append(new_user)
        return jsonify({"status": 201, "data": new_user}), 201

    except:
        return jsonify({"status": 417, "error": "signup data is required"}), 417




