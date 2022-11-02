import unittest
from urllib import response
import flask_testing


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
