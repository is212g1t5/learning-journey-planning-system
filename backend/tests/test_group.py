import sys
import flask_testing
from urllib import response
import unittest
sys.path.insert(0, '../services/groups/')
from groups import app, db, Groups


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


class TestGroups(TestApp):
    def test_view_all_groups(self):
        g1 = Groups(group_id=1, group_name="Group 1")
        g2 = Groups(group_id=2, group_name="Group 2")
        g3 = Groups(group_id=3, group_name="Group 3")
        db.session.add(g1)
        db.session.add(g2)
        db.session.add(g3)
        db.session.commit()

        response = self.client.get("/groups/1")
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "groups": [
                    {
                        "group_id": 1,
                        "group_name": "Group 1"
                    }
                ]
            }
        })


if __name__ == '__main__':
    unittest.main()
