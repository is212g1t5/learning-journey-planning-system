import unittest

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../../services/learning_journey/')

from learning_journey import LearningJourney

class TestLearningJourney(unittest.TestCase):
    def test_to_json(self):
        lj1 = LearningJourney(learning_journey_id=1, learning_journey_name="My First Learning Journey", staff_id=140882, role_id=3)

        self.assertEqual(lj1.json(), {"learning_journey_id": 1, "learning_journey_name": "My First Learning Journey", "staff_id": 140882, "role_id": 3})

    def test_valid_init(self):
        lj1 = LearningJourney(learning_journey_id=5, learning_journey_name="My LJ Name Here", staff_id=140078, role_id=2)
        
        self.assertEqual(lj1.learning_journey_id, 5)
        self.assertEqual(lj1.learning_journey_name, "My LJ Name Here")
        self.assertEqual(lj1.staff_id, 140078)
        self.assertEqual(lj1.role_id, 2)

    def test_no_value_init(self):
        with self.assertRaises(TypeError):
            LearningJourney()

if __name__ == "__main__":
    unittest.main()