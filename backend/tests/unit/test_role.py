import unittest

# importing sys
import sys

# adding Folder_2 to the system path
sys.path.insert(0, '../../services/role/')

from role import Role

class TestRole(unittest.TestCase):
    def test_to_json(self):
        role1 = Role(role_id=1, role_name="Designer", role_desc="The Designer (Engineering Design) develops technical drawings and models based on pre-defined specifications and engineering calculations.", role_status=1, role_sector="Engineering Services", role_track="Engineering Design")

        self.assertEqual(role1.json(), {"role_id": 1, "role_name": "Designer", "role_desc": "The Designer (Engineering Design) develops technical drawings and models based on pre-defined specifications and engineering calculations.", "role_status": 1, "role_sector": "Engineering Services", "role_track": "Engineering Design"})

    def test_valid_init(self):
        role2 = Role(role_id=12, role_name="Manager", role_desc="The Manager (Project Financing) is responsible for planning and leading the project financing scoping, modelling and delivery.", role_status=1, role_sector="Engineering Services", role_track="Project Financing")

        self.assertEqual(role2.role_id, 12)
        self.assertEqual(role2.role_name, "Manager")
        self.assertEqual(role2.role_desc, "The Manager (Project Financing) is responsible for planning and leading the project financing scoping, modelling and delivery.")
        self.assertEqual(role2.role_status, 1)
        self.assertEqual(role2.role_sector, "Engineering Services")
        self.assertEqual(role2.role_track, "Project Financing")

    def test_no_value_init(self):
        with self.assertRaises(TypeError):
            Role()

if __name__ == "__main__":
    unittest.main()