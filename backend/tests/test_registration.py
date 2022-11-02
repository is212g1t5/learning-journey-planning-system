import unittest
import flask_testing
import json
import sys
sys.path.insert(0, '../services/registration/')
from registration import app, db, Registration


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


class TestSkill(TestApp):
    # get_all() - 200
    def test_display_registration_1(self):
        s1 = Registration(1, "COR001", 130001,
                    "Complete", "Complete")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get('/registration')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'registration': [
                    {
                        'reg_id': 1,
                        'course_id': 'COR001',
                        'staff_id': 130001,
                        'reg_status': 'Complete',
                        'completion_status': 'Complete'
                    }
                ]
            }
        })

    # get_all() - 404
    def test_display_registration_2(self):
        response = self.client.get('/registration')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no registrations.',
        })

    # find_by_staff_id() - 200
    def test_find_registration_by_staff_1(self):
        s1 = Registration(1, "COR001", 130001,
                    "Complete", "Complete")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get('/registration/130001')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'registration': [
                    {
                        'reg_id': 1,
                        'course_id': 'COR001',
                        'staff_id': 130001,
                        'reg_status': 'Complete',
                        'completion_status': 'Complete'
                    }
                ]
            }
        })

    # find_by_staff_id() - 404
    def test_find_registration_by_staff_2(self):
        response = self.client.get('/registration/130001')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'Registration not found.',
        })

    
if __name__ == '__main__':
    unittest.main()