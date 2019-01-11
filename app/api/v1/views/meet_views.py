from app.api.v1.views.user_views import userviews, time_now
from app.api.v1.models.models import Meetups
import datetime
from flask import Blueprint, request, jsonify, make_response


@userviews.route('/meetups', methods=['POST'])
def create_meetup():
    try:
        meetups_data = request.get_json()
        if not meetups_data:
            return jsonify({"status": 204, "error": "Data not Found"}), 204

        try:
            if not meetups_data["topic"] or not meetups_data["location"] or not meetups_data["happenOn"]:
                return jsonify({"status": 422, "error": "Fill in all Fields (topic,location,happenOn)"}), 422

        except:
            return jsonify({"status": 400, "error": "Checkout the missin key"}), 400

        upcoming_meetup = {}
        for key in meetups_data:
            upcoming_meetup[key] = meetups_data[key]

        try:
            previous = Meetups[-1]
            id = previous["id"]
            id = id + 1
            upcoming_meetup["id"] = id
        except:
            upcoming_meetup["id"] = 1

        upcoming_meetup["createOn"] = time_now.strftime("%d %h %Y")

        Meetups.append(upcoming_meetup)
        return jsonify({"status": 201, "data": upcoming_meetup}), 201

    except:
        return jsonify({"status": 204, "error": "Meetup data is required"}), 204

