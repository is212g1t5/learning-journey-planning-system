import unittest
from urllib import response
import flask_testing
from learning_journey import app, db, LearningJourney
from skill import app, db, Skills

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../services/learning_journey/')

\

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


class TestSkill(TestApp):
    # display_skill() - 200
    def test_display_skills_1(self):
        s1 = Skills(1, "Python", "Programming",
                    "Python is a programming language", 1)
        db.session.add(s1)
        db.session.commit()

        response = self.client.get('/skills')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skills': [
                    {
                        'skill_category': 'Programming',
                        'skill_desc': 'Python is a programming language',
                        'skill_id': 1,
                        'skill_name': 'Python',
                        'skill_status': True
                    }
                ]
            }
        })

    # display_skill() - 404
    def test_display_skills_2(self):
        response = self.client.get('/skills')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no skills.',
            'data': [],
        })

    # create_skill() - 201
    def test_create_skill(self):
        request_body = {
            'skill_id': 1,
            'skill_name': 'Python',
            'skill_category': 'Programming',
            'skill_desc': 'Python is a programming language',
            'skill_status': True
        }

        response = self.client.post("/skills/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'code': 201,
            'data': {
                'skill_category': 'Programming',
                'skill_desc': 'Python is a programming language',
                'skill_id': 1,
                'skill_name': 'Python',
                'skill_status': True

            }
        })

    # create_skill() - 400
    def test_create_skill_invalid_skill(self):
        request_body = {
            'skill_id': 1,
            'skill_name': '',
            'skill_category': 'Programming',
            'skill_desc': 'Python is a programming language',
            'skill_status': True
        }

        response = self.client.post("/skills/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'code': 400,
            'message': 'Empty inputs or Invalid JSON input: b\'{"skill_id": 1, "skill_name": "", "skill_category": "Programming", "skill_desc": "Python is a programming language", "skill_status": true}\''
        })

    # get_skill() - doesn't have a status code
    def test_get_skill(self):
        s1 = Skills(1, "Python", "Programming",
                    "Python is a programming language", 1)
        db.session.add(s1)
        db.session.commit()

        response = self.client.get('/skills/1')
        self.assertEqual(response.json, {

            'skill_category': 'Programming',
            'skill_desc': 'Python is a programming language',
            'skill_id': 1,
            'skill_name': 'Python',
            'skill_status': True
        })

    # update_skill() - 200
    def test_update_skill(self):
        s1 = Skills(1, "Python", "Programming",
                    "Python is a programming language", 1)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_id': 1,
            'skill_name': 'Python',
            'skill_category': 'Not Programming',
            'skill_desc': 'Python is a programming language',
            'skill_status': True
        }

        response = self.client.put("/skills/update/1",
                                   data=json.dumps(request_body),
                                   content_type='application/json')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skill_category': 'Not Programming',
                'skill_desc': 'Python is a programming language',
                'skill_id': 1,
                'skill_name': 'Python',
                'skill_status': True

            },
            'message': 'Skill updated.'
        })

    # update_skill() - 400
    def test_update_skill_invalid_skill_1(self):
        s1 = Skills(1, "Python", "Programming",
                    "Python is a programming language", 1)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_id': 1,
            'skill_name': '',
            'skill_category': 'Not Programming',
            'skill_desc': 'Python is a programming language',
            'skill_status': True
        }

        response = self.client.put("/skills/update/1",
                                   data=json.dumps(request_body),
                                   content_type='application/json')
        self.assertEqual(response.json, {
            'code': 400,
            'message': 'Skill name cannot be empty.'
        })

    # update_skill() - 404
    def test_update_skill_invalid_skill_2(self):
        request_body = {
            'skill_id': 1,
            'skill_name': 'Python',
            'skill_category': 'Not Programming',
            'skill_desc': 'Python is a programming language',
            'skill_status': True
        }

        response = self.client.put("/skills/update/1",
                                   data=json.dumps(request_body),
                                   content_type='application/json')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'Skill does not exist in database.'
        })

    # update_skill() - 500
    # def test_update_skill_invalid_skill_3(self):
    #     s1 = Skills(1, "Python", "Programming"," Python is a programming language", 1)
    #     s2 = Skills(2, "Java", "Programming"," Java is a programming language", 1)
    #     db.session.add(s1)
    #     db.session.add(s2)
    #     db.session.commit()

    #     request_body = {
    #         'skill_id': 1,
    #         'skill_name': 'Java',
    #         'skill_category': 'Programming',
    #         'skill_desc': 'Python is a programming language',
    #         'skill_status': True
    #     }

    #     response = self.client.put("/skills/update/1",
    #                                data=json.dumps(request_body),
    #                                content_type='application/json')
    #     self.assertEqual(response.json, {
    #         'code': 500,
    #         'message': 'Skill name already exists.'
    #     })

    # soft_delete_skill() - 200
    def test_soft_delete_skill_1(self):
        s1 = Skills(1, "Python", "Programming",
                    "Python is a programming language", 1)
        db.session.add(s1)
        db.session.commit()

        response = self.client.delete("/skills/delete/1")
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skill_category': 'Programming',
                'skill_desc': 'Python is a programming language',
                'skill_id': 1,
                'skill_name': 'Python',
                'skill_status': False
            },
            'message': 'Skill retired.'
        })

    # soft_delete_skill() - 404
    def test_soft_delete_skill_2(self):
        response = self.client.delete("/skills/delete/1")
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'Skill does not exist in database.'
        })

    # restore_skill() - 200
    def test_restore_skill_1(self):
        s1 = Skills(1, "Python", "Programming",
                    "Python is a programming language", 0)
        db.session.add(s1)
        db.session.commit()

        response = self.client.put("/skills/restore/1")
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skill_category': 'Programming',
                'skill_desc': 'Python is a programming language',
                'skill_id': 1,
                'skill_name': 'Python',
                'skill_status': True
            },
            'message': 'Skill restored.'
        })

    # restore_skill() - 404
    def test_restore_skill_2(self):
        response = self.client.put("/skills/restore/1")
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'Skill does not exist in database.'
        })

    # restore_skill() - 400
    def test_restore_skill_3(self):
        s1 = Skills(1, "Python", "Programming",
                    "Python is a programming language", 1)
        db.session.add(s1)
        db.session.commit()

        response = self.client.put("/skills/restore/1")
        self.assertEqual(response.json, {
            'code': 400,
            'message': 'Skill is already active.'
        })

if __name__ == '__main__':
    unittest.main()
