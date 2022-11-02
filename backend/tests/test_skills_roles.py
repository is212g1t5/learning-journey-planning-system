import unittest
import flask_testing
import json
import sys
sys.path.insert(0, '../services/skills_roles/')
from skills_roles import app, db, SkillsRoles


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

class TestSkillsRoles(TestApp):

    #get_all_by_roles() - 200
    def test_get_all_by_roles_1(self):
        s1 = SkillsRoles(1, 1)
        db.session.add(s1)
        db.session.commit()

        response = self.client.get('/skills_roles/1')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skills_roles': [
                    {
                        'role_id': 1,
                        'skills_id': 1,
                    }
                ]
            }
        })
    #get_all_by_roles() - 404
    def test_get_all_by_roles_2(self):
        response = self.client.get('/skills_roles/1')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no skills_roles for this role',

        })

    #create_skills_roles() - 201
    def test_create_skills_roles(self):
        request_body = {
            'role_id': 1,
            'skill_id': 1,
        }
        response = self.client.post('/skills_roles', json=request_body)
        self.assertEqual(response.json, {
            'code': 201,
            'data': {
                    'role_id': 1,
                    'skills_id': 1,
            },
            "message": "skills_roles created successfully."
        })
    
    #create_skills_roles() - 500
    def test_create_skills_roles_2(self):
        s1 = SkillsRoles(1, 1)
        db.session.add(s1)
        db.session.commit()
        request_body = {
            'role_id': 1,
            'skill_id': 1,
        }
        response = self.client.post('/skills_roles', json=request_body)
        self.assertEqual(response.json, {
            'code': 500,
            'data':{
                'skills_roles':
                {
                    'role_id': 1,
                    'skills_id': 1
                }
            },
            'message': 'An error occurred while creating the skills_roles.',
        })
    #delete_skills_roles() - 200
    def test_delete_skills_roles(self):
        s1 = SkillsRoles(1, 1)
        db.session.add(s1)
        db.session.commit()
        response = self.client.delete('/skills_roles/1/1')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'role_id': 1,
                'skill_id': 1,
            }
        })
    #delete_skills_roles() - 404
    def test_delete_skills_roles_2(self):
        response = self.client.delete('/skills_roles/1/1')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'skills_roles not found.',
        })
        

if __name__ == '__main__':
    unittest.main()
