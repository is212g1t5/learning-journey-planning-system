import unittest
import flask_testing
import json
import sys
sys.path.insert(0, '../services/role/')
from role import app, db, Role


class TestApp(flask_testing.TestCase):
   app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
   app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
   app.config['TESTING'] = 1

   def create_app(self):
      return app

   def setUp(self):
      db.create_all()

   def tearDown(self):
      db.session.remove()
      db.drop_all()


class TestRole(TestApp):
   # get_all() - 200
   def test_success_get_all(self):
      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  1, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      response = self.client.get('/roles')
      self.assertEqual(response.json, {
         'code': 200,
         'data': {
               'roles': [
                  {
                     "role_id": 1, 
                     "role_name": "Software Engineer",
                     "role_desc": "Build and optimize software infrastructure",
                     "role_status": 1,
                     "role_sector": "Software Development",
                     "role_track": "Product Design"
                  }
               ]
         }
      })

   # get_all() - 404
   def test_fail_get_all(self):
      response = self.client.get('/roles')
      self.assertEqual(response.json, {
         'code': 404,
         "message": "There are no roles."
      })

   # create_role() - 201
   def test_create_role(self):
      request_body = {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "Build and optimize software infrastructure",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": "Product Design"
      }

      response = self.client.post("/roles/create",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
               "code": 201,
               "data": "Software Engineer has been created."
         })

   # create_role() - 400
   #role already exists
   def test_create_role(self):
      request_body = {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "Build and optimize software infrastructure",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": "Product Design"
      }

      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  1, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      #second call to create same role
      response = self.client.post("/roles/create",
                                 data=json.dumps(request_body),
                                 content_type='application/json')

      self.assertEqual(response.json, {
         "code": 400,
         "data": {
            "role_name": "Software Engineer"
         },
         "message": "This role already exists."
      })

   #no role name
   def test_no_name_create(self):
      request_body = {
         "role_id": 1, 
         "role_name": "",
         "role_desc": "Build and optimize software infrastructure",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": "Product Design"
      }

      response = self.client.post("/roles/create",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
            "code": 400,
            "data": {
               "role_name": ""
            },
            "message": "Role name cannot be empty."
      })

   #no role description
   def test_no_desc_create(self):
      request_body = {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": "Product Design"
      }

      response = self.client.post("/roles/create",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
            "code": 400,
            "data": {
               "role_desc": ""
            },
            "message": "Role description cannot be empty."
      })

   #no role status
   def test_no_status_create(self):
      request_body = {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "Build and optimize software infrastructure",
         "role_status": "",
         "role_sector": "Software Development",
         "role_track": "Product Design"
      }

      response = self.client.post("/roles/create",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
            "code": 400,
            "data": {
               "role_status": ""
            },
            "message": "Role status cannot be empty."
      })

   #no role sector
   def test_no_sector_create(self):
      request_body = {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "Build and optimize software infrastructure",
         "role_status": 1,
         "role_sector": "",
         "role_track": "Product Design"
      }

      response = self.client.post("/roles/create",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
            "code": 400,
            "data": {
               "role_sector": ""
            },
            "message": "Role sector cannot be empty."
      })

   #no role track
   def test_no_sector_create(self):
      request_body = {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "Build and optimize software infrastructure",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": ""
      }

      response = self.client.post("/roles/create",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
            "code": 400,
            "data": {
               "Role_track": ""
            },
            "message": "Role track cannot be empty."
      })

   # get_role() - doesn't have a status code
   def test_get_role(self):
      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  1, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      response = self.client.get('/roles/1')
      self.assertEqual(response.json, {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "Build and optimize software infrastructure",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": "Product Design"
      })
   
   #get_role() - 404
   def test_fail_get_role(self):

      response = self.client.get('/roles/1')
      self.assertEqual(response.json, {
         "code": 404,
         "message": "No role with this role ID.",
      })


   # update_role() - 200
   def test_update_role(self):
      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  1, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      request_body = {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "Develop and maintain internal and client software",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": "Product Design"
      }

      response = self.client.put("/roles/update/1",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
         "code": 200,
         "data": {
            "role_id": 1, 
            "role_name": "Software Engineer",
            "role_desc": "Develop and maintain internal and client software",
            "role_status": 1,
            "role_sector": "Software Development",
            "role_track": "Product Design"
         },
         "message": "Role updated."
      })

   # update_role() - 400
   def test_no_name_update(self):
      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  1, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      request_body = {
         "role_id": 1, 
         "role_name": "",
         "role_desc": "Develop and maintain internal and client software",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": "Product Design"
      }

      response = self.client.put("/roles/update/1",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
         'code': 400,
         'message': 'Role name cannot be empty.'
      })

   # update_role() - 404
   def test_invalid_update_role(self):
      request_body = {
         "role_id": 1, 
         "role_name": "Software Engineer",
         "role_desc": "Develop and maintain internal and client software",
         "role_status": 1,
         "role_sector": "Software Development",
         "role_track": "Product Design"
      }

      response = self.client.put("/roles/update/1",
                                 data=json.dumps(request_body),
                                 content_type='application/json')
      self.assertEqual(response.json, {
         "code": 404,
         "message": "Role does not exist in database."
      })

   # soft_delete_role() - 200
   def test_soft_delete_role_1(self):
      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  1, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      response = self.client.delete("/roles/delete/1")
      self.assertEqual(response.json, {
         "code": 200,
         "data": {
            "role_id": 1, 
            "role_name": "Software Engineer",
            "role_desc": "Develop and maintain internal and client software",
            "role_status": False,
            "role_sector": "Software Development",
            "role_track": "Product Design"
         },
         "message": "Role retired."
      })

   # soft_delete_role() - 404
   def test_soft_delete_role2(self):
      response = self.client.delete("/roles/delete/1")
      self.assertEqual(response.json, {
         'code': 404,
         "message": "Role does not exist in database."
      })

   #soft_delete_role() - 400
   def test_fail_soft_delete_role(self):
      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  0, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      response = self.client.delete("/roles/delete/1")
      self.assertEqual(response.json, {
         "code": 400,
         "message": "Role is already retired."
      })

   # restore_role() - 200
   def test_restore_role1(self):
      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  0, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      response = self.client.put("/roles/restore/1")
      self.assertEqual(response.json, {
         "code": 200,
         "data": {
            "role_id": 1, 
            "role_name": "Software Engineer",
            "role_desc": "Develop and maintain internal and client software",
            "role_status": True,
            "role_sector": "Software Development",
            "role_track": "Product Design"
         },
         "message": "Role restored."
      })

   # restore_role() - 404
   def test_fail_restore_role_1(self):
      response = self.client.put("/roles/restore/1")
      self.assertEqual(response.json, {
         'code': 404,
         "message": "Role does not exist in database."
      })

   # restore_role() - 400
   def test_fail_restore_role_2(self):
      s1 = Role(1, "Software Engineer", "Build and optimize software infrastructure",
                  1, "Software Development", "Product Design")
      db.session.add(s1)
      db.session.commit()

      response = self.client.put("/roles/restore/1")
      self.assertEqual(response.json, {
         "code": 400,
         "message": "Role is already active."
      })


if __name__ == '__main__':
   unittest.main()
