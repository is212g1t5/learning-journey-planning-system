import unittest
import flask_testing
import json
import sys
sys.path.insert(0, '../services/skills_courses/')
from skills_courses import app, db, SkillsCourses


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

class TestSkillCourses(TestApp):
    # get_all() - 200
    def test_display_skills_courses_1(self):
        s1 = SkillsCourses(1, 1)
        db.session.add(s1)
        db.session.commit()

        response = self.client.get('/skills_courses/all')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skills_courses': [
                    {
                        'course_id': '1',
                        'skill_id': 1
                    }
                ]
            }
        })

    # get_all() - 404
    def test_display_skills_courses_2(self):
        response = self.client.get('/skills_courses/all')
        self.assertEqual(response.json, {
            'code': 404,
            'message': 'No data found.',
        })

    # get_all_by_course
    def test_display_skills_courses_3(self):
        s1 = SkillsCourses(1, 1)
        s2 = SkillsCourses(2, 1)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        response = self.client.get('/skills_courses/course/1')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skills_courses': [
                    {
                        'course_id': '1',
                        'skill_id': 1
                    },{
                        'course_id': '1',
                        'skill_id': 2
                    }
                ]
            }
        })
    #get_all_by_skills 
    def test_display_skills_courses_4(self):
        s1 = SkillsCourses(1, 1)
        s2 = SkillsCourses(1, 2)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        response = self.client.get('/skills_courses/skill/1')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skills_courses': [
                    {
                        'course_id': '1',
                        'skill_id': 1
                    },{
                        'course_id': '2',
                        'skill_id': 1
                    }
                ]
            }
        })
    # create_skill_course() - 201
    def test_create_skill_course(self):

        request_body = {
            'skill_id': 1,
            'course_id': 1
        }
        response = self.client.post('/skills_courses', data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.json, {
            'code': 201,
            'data': {
                'skills_courses':{
                    'skill_id': 1,
                    'course_id': '1'
                }
            }
        })

    # create_skill_course() - 500
    def test_create_skill_course_2(self):
        s1 = SkillsCourses(1, '1')
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_id': 1,
            'course_id': '1'
        }
        response = self.client.post('/skills_courses', data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.json, {
            'code': 500,
            'data':{
                'skills_courses':
                    {'course_id': '1', 'skill_id': 1}
                },
            'message': 'An error occurred while creating the skills_courses.'
        })

    #map skills_Courses - 201
    def test_map_skills_courses(self):
        request_body = {
            'skill_id': 1,
            'course_id': 1
        }
        response = self.client.post('/skills_courses', data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.json, {
            'code': 201,
            'data': {
                'skills_courses':{
                    'skill_id': 1,
                    'course_id': '1'
                }
            }
        })

    #map skills_Courses - 500
    def test_map_skills_courses_2(self):
        s1 = SkillsCourses(1, 1)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_id': 1,
            'course_id': '1'
        }
        response = self.client.post('/skills_courses', data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.json, {
            'code': 500,
            'data':{
                'skills_courses':
                    {
                        'course_id': '1', 
                        'skill_id': 1
                    }
                }
                ,
                
            'message': 'An error occurred while creating the skills_courses.'
        })

    # delete_skill_course() - 200
    def test_delete_skill_course(self):
        s1 = SkillsCourses(1, 1)
        db.session.add(s1)
        db.session.commit()

        response = self.client.delete('/skills_courses/delete/1/1')
        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'skills_courses':
                {
                    'skill_id': 1,
                    'course_id': '1'
                }
            }
        })


if __name__ == '__main__':
    unittest.main()

