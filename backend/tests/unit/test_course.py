import unittest

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../../services/course/')

from course import Course

class TestCourse(unittest.TestCase):
    def test_to_json(self):
        course1 = Course(course_id="SAL004", course_name="Stakeholder Management", course_desc="Develop a stakeholder engagement plan and negotiate with stakeholders to arrive at mutually-beneficial arrangements.",course_status=1, course_type="Internal", course_category="Sales")

        self.assertEqual(course1.json(), {"course_id": "SAL004", "course_name": "Stakeholder Management", "course_desc": "Develop a stakeholder engagement plan and negotiate with stakeholders to arrive at mutually-beneficial arrangements.", "course_status": 1, "course_type": "Internal", "course_category": "Sales"})

    def test_valid_init(self):
        course1 = Course(course_id="SAL004", course_name="Stakeholder Management", course_desc="Develop a stakeholder engagement plan and negotiate with stakeholders to arrive at mutually-beneficial arrangements.",course_status=1, course_type="Internal", course_category="Sales")

        self.assertEqual(course1.course_id, "SAL004")
        self.assertEqual(course1.course_name, "Stakeholder Management")
        self.assertEqual(course1.course_desc, "Develop a stakeholder engagement plan and negotiate with stakeholders to arrive at mutually-beneficial arrangements.")
        self.assertEqual(course1.course_status, 1)
        self.assertEqual(course1.course_type, "Internal")
        self.assertEqual(course1.course_category, "Sales")

    def test_no_value_init(self):
        with self.assertRaises(TypeError):
            Course()

if __name__ == "__main__":
    unittest.main()