import unittest
from app import create_app
import os
import json
import pytest
import datetime
from app.api.v1.models.models import Meetups


class Testing(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        expected_time = datetime.datetime.now() + datetime.timedelta(days=7)
        expected_time = expected_time.replace(microsecond=0)
        current = datetime.datetime.now()

        self.meetup1 = {
            "topic": "Innitial meetup",
            "images": ["/Desktop/pictures/<mage>", "/Desktop/pictures/<mage>"],
            "location": "Upper Hill",
            "happenOn": expected_time.strftime("%D %H:%M %p"),
            "tags": ["#At Upper Hill", "#coding", "#enjoy"]
        }

        self.meetup11 = {
            "topic": "",
            "images": ["/Desktop/pictures/<mage>", "/Desktop/pictures/<mage>"],
            "location": "Dandora",
            "happenOn": expected_time.strftime("%D %H:%M %p"),
            "tags": ["#At Dandora", "#coding", "#enjoy"]
        }

        self.meetup1created = {
            "id": 1,
            "createOn": current.strftime("%d %h %Y"),
            "topic": "Innitial meetup",
            "images": ["/Desktop/pictures/<mage>", "/Desktop/pictures/<mage>"],
            "location": "Upper Hill",
            "happenOn": expected_time.strftime("%D %H:%M %p"),
            "tags": ["#At Upper Hill", "#coding", "#enjoy"]
        }

        self.meetup2 = {
            "images": ["/Desktop/pictures/<mage>", "/Desktop/pictures/<mage>"],
            "location": "Dandora",
            "happenOn": expected_time.strftime("%D %H:%M %p"),
            "tags": ["#At Dandora", "#coding", "#enjoy"]
        }

        self.nodata = {}

    def tearDown(self):
        pass


class Testing_Meetups(Testing):
    def test_createdmeetup_success(self):
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup1), content_type="application/json")
        meet_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(meet_resp["data"], self.meetup1created)

    def test_createdmeetup_fail(self):
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup11), content_type="application/json")
        meet_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(meet_resp["error"],
                         "Below fields are required(topic,location,happenOn)")

    def test_createdmeetup_fail_no_data(self):
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.nodata), content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_getallmeetups_success(self):
        Meetups.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_getallupcoming_success(self):
        Meetups.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/upcoming', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_getsinglemeetup_success(self):
        Meetups.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/1', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_getsinglemeetup_fail(self):
        Meetups.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/1000', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_deletemeetup_fail(self):
        response = self.client.delete(
            '/api/v1/meetups/1000', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_deletemeetup_success(self):
        response = self.client.delete(
            '/api/v1/meetups/1', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)
