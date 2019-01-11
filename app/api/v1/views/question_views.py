from app.api.v1.views.user_views import userviews, time_now
from app.api.v1.models.models import Questions
import datetime
from flask import Blueprint, request, jsonify, make_response


@userviews.route('/questions', methods=['POST'])
def adding_a_meetupquestion():
    try:
        question_data = request.get_json()
        if not question_data:
            return jsonify({"status": 204, "error": "Such data not found"}), 204

        try:
            if not question_data["topic"] or not question_data["body"]:
                return jsonify({"status": 422, "error": "All these fields are  required(topic,body)"}), 422

        except:
            return jsonify({"status": 400, "error": "check again there are key fields missing"}), 400

        post_question = {}
        for key in question_data:
            post_question[key] = question_data[key]

        try:
            latest = Questions[-1]
            id = latest["id"]
            id = id + 1
            post_question["id"] = id
        except:
            post_question["id"] = 1

        post_question["createOn"] = time_now.strftime("%d %h %Y")
        post_question["upvotes"] = 0
        post_question["downvotes"] = 0

        Questions.append(post_question)
        return jsonify({"status": 201, "data": "Your has question successfully been added"}), 201

    except:
        return jsonify({"status": 204, "error": "Kindly note that the meetup data is required"}), 204


@userviews.route("/question/<question_id>/upvote", methods=["PATCH"])
def user_upvote(question_id):
    try:
        question_id = int(question_id)
    except:
        return jsonify({"status": 400, "error": "question id doesn't exist"}), 400

    for question in Questions:
        if question["id"] == question_id:
            return jsonify({"status": 202, "data": "You have just voted to this question"}), 202

    return jsonify({"status": 404, "error": "We can't find such a question"}), 404


@userviews.route("/questions/<question_id>/downvote", methods=["PATCH"])
def downvote_quiz(question_id):
    try:
        question_id = int(question_id)
    except:
        return jsonify({"status": 400, "error": "question id doesn't exist"}), 400

    for question in Questions:
        if question["id"] == question_id:
            return jsonify({"status": 200, "data": "You have just downvoted this question"}), 200

    return jsonify({"status": 404, "error": "question not found"}), 404