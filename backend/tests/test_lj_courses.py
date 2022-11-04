import unittest
from urllib import response
import flask_testing
import json

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../services/lj_courses/')

# from services.lj_courses.invokes import invoke_http
from lj_courses import app, db, LjCourses

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

# get_all_by_lj
# create_lj_course
# delete_lj_course

class TestGetAllLjCourse(TestApp):
    def test_valid_all_lj_course(self):
        ljc1 = LjCourses(learning_journey_id=1, course_id="COR001")
        db.session.add(ljc1)
        db.session.commit()

        response = self.client.get("lj_courses/1")
        
        self.assertEqual(response.json, {
            "code": 200, 
            "data": {
                "lj_courses": [
                {
                    "course_id": "COR001", 
                    "learning_journey_id": 1
                }
                ]
            }
        })
    
    def test_invalid_all_lj_course(self):
        response = self.client.get("lj_courses/1")

        self.assertEqual(response.json, {
            "code": 404,
            "message": "There are no lj_courses for this learning_journey"
        })

class TestCreateLjCourse(TestApp):
    def test_create_ljc1(self):
        request_body = {
            "course_id": "COR001", 
            "learning_journey_id": 1
        }

        response = self.client.post("/lj_courses/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                "course_id": "COR001", 
                "learning_journey_id": 1
            }
        })

    def test_create_ljc2(self):
        ljc1 = LjCourses(learning_journey_id=1, course_id="COR001")
        db.session.add(ljc1)
        db.session.commit()
        request_body = {
            "course_id": "COR001", 
            "learning_journey_id": 1
        }

        response = self.client.post("/lj_courses/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            "code": 400,
            "data": {
                "lj_courses": "lj_course already exists."
            }
        })


class TestDeleteAllLjCourse(TestApp):
    def test_delete_valid_lj_course(self):
        ljc1 = LjCourses(learning_journey_id=1, course_id="COR001")
        db.session.add(ljc1)
        db.session.commit()

        response = self.client.delete("/lj_courses/delete/1/COR001")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], {
            "lj_course": "lj_course deleted."
        })

    def test_delete_invalid_lj_course(self):

        response = self.client.delete("/lj_courses/delete/1/COR001")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "lj_course not found.")

if __name__ == '__main__':
    unittest.main()