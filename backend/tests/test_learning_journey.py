import unittest
from urllib import response
import flask_testing
import json

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../services/learning_journey/')

# from services.learning_journey.invokes import invoke_http
from learning_journey import app, db, LearningJourney

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestDisplayLearningJourneys(TestApp):
    def test_display_valid_staff_learning_journeys(self):
        lj1 = LearningJourney(learning_journey_id=1, learning_journey_name="My First Learning Journey", staff_id=140882, role_id=3)
        db.session.add(lj1)
        db.session.commit()

        response = self.client.get("learning_journeys/140882")
        
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "learning_journeys": [
                    {
                        "learning_journey_id": 1,
                        "learning_journey_name": "My First Learning Journey",
                        "role_id": 3,
                        "staff_id": 140882
                    }
                ]
            }
        })
    
    def test_display_invalid_staff_learning_journeys(self):
        response = self.client.get("learning_journeys/140882")

        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no learning_journeys for this staff"
        })

class TestDisplaySingleJourney(TestApp):
    def test_display_valid_single_learning_journeys(self):
        lj1 = LearningJourney(learning_journey_id=1, learning_journey_name="My First Learning Journey", staff_id=140882, role_id=3)
        db.session.add(lj1)
        db.session.commit()

        response = self.client.get("/learning_journeys/single_journey/1")
        
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "learning_journey_id": 1,
                "learning_journey_name": "My First Learning Journey",
                "role_id": 3,
                "staff_id": 140882
            }
        })
    
    def test_display_invalid_single_learning_journeys(self):
        response = self.client.get("/learning_journeys/single_journey/1")

        self.assertEqual(response.json, {
                "code": 404,
                "message": "Learning journey not found."
        })

class TestAllLearningJourney(TestApp):
    def test_get_all_lj_details1(self):
        response = self.client.get("/learning_journeys/id/1")
        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no learning journeys with this learning journey ID."
        })

class TestCreateLearningJourney(TestApp):
    def test_create_lj1(self):
        request_body = {
            "learning_journey_id" : 1, 
            "learning_journey_name" :"My First Learning Journey", 
            "staff_id" : 140882,
            "role_id" : 3
        }

        response = self.client.post("/learning_journeys/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                "learning_journey_id" : 1, 
                "learning_journey_name" :"My First Learning Journey", 
                "staff_id" : 140882,
                "role_id" : 3
            }
        })
        
    def test_create_lj2(self):
        lj1 = LearningJourney(learning_journey_id=1, learning_journey_name="My First Learning Journey", staff_id=140882, role_id=3)
        db.session.add(lj1)
        db.session.commit()
        request_body = {
            "learning_journey_id" : 1, 
            "learning_journey_name" :"My First Learning Journey", 
            "staff_id" : 140882,
            "role_id" : 3
        }

        response = self.client.post("/learning_journeys/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 400,
            "data": {
                "learning_journey_name": "My First Learning Journey"
            },
            "message": "A learning_journey with name 'My First Learning Journey' already exists."
        })

    def test_create_lj3(self):
        request_body = {
            "learning_journey_id" : 1, 
            "learning_journey_name" :"", 
            "staff_id" : 140882,
            "role_id" : 3
        }

        response = self.client.post("/learning_journeys/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 400,
            "data": {
                "learning_journey_name": ""
            },
            "message": "Learning Journey name cannot be empty."
        })

class TestUpdateLearningJourney(TestApp):
    def test_update_lj1(self):
        lj1 = LearningJourney(learning_journey_id=1, learning_journey_name="My First Learning Journey", staff_id=140882, role_id=3)
        db.session.add(lj1)
        db.session.commit()
        request_body = {
            "learning_journey_id" : 1, 
            "learning_journey_name" :"", 
            "staff_id" : 140882,
            "role_id" : 3
        }

        response = self.client.put("/learning_journeys/update/1",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 400,
            "data": {
                "learning_journey_name": ""
            },
            "message": "learning journey name cannot be empty."
        })

    def test_update_lj2(self):
        lj1 = LearningJourney(learning_journey_id=1, learning_journey_name="My First Learning Journey", staff_id=140882, role_id=3)
        db.session.add(lj1)
        db.session.commit()
        request_body = {
            "learning_journey_id" : 1, 
            "learning_journey_name" :"My first and favourite Journey", 
            "staff_id" : 140882,
            "role_id" : 3
        }

        response = self.client.put("/learning_journeys/update/1",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "learning_journey_id" : 1, 
                "learning_journey_name": "My first and favourite Journey",
                "staff_id" : 140882,
                "role_id" : 3
            }
        })

    def test_update_lj3(self):
        request_body = {
            "learning_journey_id" : 1, 
            "learning_journey_name" :"My first and favourite Journey", 
            "staff_id" : 140882,
            "role_id" : 3
        }

        response = self.client.put("/learning_journeys/update/1",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 404,
            "message": "Learning Journey not found."
        })

class TestDeleteLearningJourney(TestApp):
    def test_delete_valid_learning_journey(self):
        lj1 = LearningJourney(learning_journey_id=1, learning_journey_name="My First Learning Journey", staff_id=140882, role_id=3)
        db.session.add(lj1)
        db.session.commit()

        response = self.client.delete("/learning_journeys/delete/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], {
            "learning_journey_id": 1
        })

    def test_delete_invalid_learning_journey(self):

        response = self.client.delete("/learning_journeys/delete/1")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Learning_Journey not found.")

if __name__ == '__main__':
    unittest.main()
