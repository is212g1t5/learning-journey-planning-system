import unittest

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../../services/groups/')

from groups import Groups

class TestGroups(unittest.TestCase):
    def test_to_json(self):
        group1 = Groups(group_id=1, group_name="Learner")

        self.assertEqual(group1.json(), {"group_id": 1, "group_name": "Learner"})

    def test_valid_init(self):
        group2 = Groups(group_id=2, group_name="Human Resource")

        self.assertEqual(group2.group_id, 2)
        self.assertEqual(group2.group_name, "Human Resource")

    def test_no_value_init(self):
        with self.assertRaises(TypeError):
            Groups()

if __name__ == "__main__":
    unittest.main()