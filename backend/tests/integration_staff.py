
import unittest
from urllib import response
import flask_testing
import sys
sys.path.insert(0, '../services/staff/')
from staff import app, db, Staff

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


class TestViewStaffDetails(TestApp):
    # View Staff Details - 200
    def test_view_staff_details_1(self):
        s1 = Staff(1, "John", "Doe", "IT", "johndoe@gmail.com", 1)
        s2 = Staff(2, "Jane", "Doe", "IT", "janedoe@gmail.com", 2)
        s3 = Staff(3, "John", "Smith", "IT", "johnsmith@gmail.com", 1)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()

        response = self.client.get('/staffs')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'staffs': [
                    {
                        'staff_id': 1,
                        'staff_fname': 'John',
                        'staff_lname': 'Doe',
                        'dept': 'IT',
                        'email': 'johndoe@gmail.com',
                        'group': 1
                    },
                    {
                        'staff_id': 2,
                        'staff_fname': 'Jane',
                        'staff_lname': 'Doe',
                        'dept': 'IT',
                        'email': 'janedoe@gmail.com',
                        'group': 2
                    },
                    {
                        'staff_id': 3,
                        'staff_fname': 'John',
                        'staff_lname': 'Smith',
                        'dept': 'IT',
                        'email': 'johnsmith@gmail.com',
                        'group': 1
                    }
                ]
            }
        })

    # View Staff Details - 404
    def test_view_staff_details_2(self):
        response = self.client.get('/staffs')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no staffs.'
        })

    # View Staff Details - 200
    def test_view_staff_details_3(self):
        s1 = Staff(1, "John", "Doe", "IT", "johndoe@gmail.com", 1)
        s2 = Staff(2, "Jane", "Doe", "IT", "janedoe@gmail.com", 2)
        s3 = Staff(3, "John", "Smith", "IT", "johnsmith@gmail.com", 1)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()

        response = self.client.get('/staffs/1')
        self.assertEqual(response.json, {
            'code': 200,
            'data': [
                {
                    'staff_id': 1,
                    'staff_fname': 'John',
                    'staff_lname': 'Doe',
                    'dept': 'IT',
                    'email': 'johndoe@gmail.com',
                    'group': 1
                },
                {
                    'staff_id': 3,
                    'staff_fname': 'John',
                    'staff_lname': 'Smith',
                    'dept': 'IT',
                    'email': 'johnsmith@gmail.com',
                    'group': 1
                }
            ]

        })
    
    # View Staff Details - 404
    def test_view_staff_details_4(self):
        response = self.client.get('/staffs/1')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'No staffs found.'
        })


if __name__ == '__main__':
    unittest.main()
