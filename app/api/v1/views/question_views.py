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