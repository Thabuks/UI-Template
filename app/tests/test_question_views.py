import unittest
from app import create_app
import os
import json
import pytest
import datetime
from app.api.v1.models.models import Questions


class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.question1 = {}

        self.question2 = {
            "topic": "no body",
            "body": ""
        }

        self.question3 = {
            "body": "xxxxxxx"
        }

        self.question4 = {
            "body": "here is the body",
            "topic": "meetup topic"
        }

    def tearDown(self):
        pass

    def test_postquestion_success(self):
        response = self.client.post(
            '/api/v1/questions', data=json.dumps(self.question4), content_type="application/json")
        q_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(q_resp["data"], "Your question has been added successfully")

    def test_question_no_data(self):
        response = self.client.post(
            '/api/v1/questions', data=json.dumps(self.question1), content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_question_empty_fields(self):
        response = self.client.post(
            '/api/v1/questions', data=json.dumps(self.question2), content_type="application/json")
        q_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(q_resp["error"],
                         "Below fields are mandatory(topic,body)")

    def test_missing_key_fields(self):
        response = self.client.post(
            '/api/v1/questions', data=json.dumps(self.question3), content_type="application/json")
        q_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(q_resp["error"], "Check the missing field")

    def test_upvote_success(self):
        response = self.client.patch(
            '/api/v1/questions/1/upvote')
        q_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 202)
        self.assertEqual(q_resp["data"], "You have just voted to this question")

    def test_downvote_success(self):
        Questions.append({"id": 1, "topic": "my first", "body": "no body"})
        response = self.client.patch(
            '/api/v1/questions/1/downvote')
        q_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(q_resp["data"], "You have just downvoted to this question")

    def test_upvote_fail(self):
        response = self.client.patch(
            '/api/v1/questions/100/upvote')
        q_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(q_resp["error"], "such a question could not found")
