import unittest

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../../services/skill/')

from skill import Skills

class TestSkills(unittest.TestCase):
    def test_to_json(self):
        skill1 = Skills(skill_id=2, skill_name="Creative Thinking", skill_category="Thinking Critically", skill_desc="Adopt diverse perspectives in combining ideas or information and making connections between different fields to create different ideas, .....", skill_status=1)

        self.assertEqual(skill1.json(), {"skill_id": 2, "skill_name": "Creative Thinking", "skill_category": "Thinking Critically", "skill_desc": "Adopt diverse perspectives in combining ideas or information and making connections between different fields to create different ideas, .....", "skill_status": 1})

    def test_valid_init(self):
        skill1 = Skills(skill_id=2, skill_name="Creative Thinking", skill_category="Thinking Critically", skill_desc="Adopt diverse perspectives in combining ideas or information and making connections between different fields to create different ideas, .....", skill_status=1)

        self.assertEqual(skill1.skill_id, 2)
        self.assertEqual(skill1.skill_name, "Creative Thinking")
        self.assertEqual(skill1.skill_category, "Thinking Critically")
        self.assertEqual(skill1.skill_desc, "Adopt diverse perspectives in combining ideas or information and making connections between different fields to create different ideas, .....")
        self.assertEqual(skill1.skill_status, 1)

    def test_no_value_init(self):
        with self.assertRaises(TypeError):
            Skills()

if __name__ == "__main__":
    unittest.main()