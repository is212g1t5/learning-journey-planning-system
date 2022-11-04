import unittest
from urllib import response
import flask_testing
import json

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../services/lj_role_skill/')

# from services.lj_role_skill.invokes import invoke_http
from lj_role_skill import app, db, LjSkills

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

class TestGetAllLjSkill(TestApp):
    def test_valid_all_lj_Skill(self):
        ljs1 = LjSkills(learning_journey_id=1, skill_id=1, role_id=2)
        db.session.add(ljs1)
        db.session.commit()

        response = self.client.get("lj_skills/1")
        
        self.assertEqual(response.json, {
            "code": 200, 
            "data": {
                "lj_skills": [
                {
                    "learning_journey_id": 1,
                    "skill_id": 1,
                    "role_id": 2
                }
                ]
            }
        })
    
    def test_invalid_all_lj_Skill(self):
        response = self.client.get("lj_skills/1")

        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no lj_skills for this learning_journey"
        })

class TestCreateLjSkill(TestApp):
    def test_create_ljs1(self):
        request_body = {
            "learning_journey_id": 1,
            "skill_id": 1,
            "role_id": 2
        }

        response = self.client.post("/lj_skills/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                "learning_journey_id": 1,
                "skill_id": 1,
                "role_id": 2
            }
        })

    def test_create_ljs2(self):
        ljs1 = LjSkills(learning_journey_id=1, skill_id=1, role_id=2)
        db.session.add(ljs1)
        db.session.commit()
        request_body = {
            "learning_journey_id": 1,
            "skill_id": 1,
            "role_id": 2
        }

        response = self.client.post("/lj_skills/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 400,
            "data": {
                "lj_skills": "lj_skill already exists."
            }
        })

class TestDeleteAllLjSkill(TestApp):
    def test_delete_valid_lj_skill(self):
        ljs1 = LjSkills(learning_journey_id=1, skill_id=1, role_id=2)
        db.session.add(ljs1)
        db.session.commit()

        response = self.client.delete("/lj_skills/delete/1/1/2")

        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "lj_skills": "lj_skill deleted."
            }
        })

    def test_delete_invalid_lj_skill(self):

        response = self.client.delete("/lj_skills/delete/1/1/2")

        self.assertEqual(response.json, {
            "code": 404,
            "data": {
                "lj_skills": "lj_skill not found."
            }
        })

if __name__ == '__main__':
    unittest.main()