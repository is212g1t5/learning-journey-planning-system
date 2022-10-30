# roles service

from flask import Flask, request, jsonify  # web framework
from flask_sqlalchemy import SQLAlchemy  # for database (ORM)
from flask_cors import CORS  # enable CORS

from os import environ  # access env variable

# ====================

#   F L A S K  &  D B  S E T U P

# ====================

app = Flask(__name__)
cors = CORS(app)  # enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), nullable=False)
    role_desc = db.Column(db.String(64), nullable=False)
    role_status = db.Column(db.Boolean, nullable=False)
    role_sector = db.Column(db.String(64), nullable=False)
    role_track = db.Column(db.String(64), nullable=False)

    def __init__(self, role_id, role_name, role_desc, role_status, role_sector, role_track):
        self.role_id = role_id
        self.role_name = role_name
        self.role_desc = role_desc
        self.role_status = role_status
        self.role_sector = role_sector
        self.role_track = role_track

    def json(self):
        return {"role_id": self.role_id, "role_name": self.role_name, "role_desc": self.role_desc, "role_status": self.role_status, "role_sector": self.role_sector, "role_track": self.role_track}

# ====================

#   A P I  E N D P O I N T S

    # get_all(): Diplay all roles
    # create_role(): Receive new role details and create new role into the db
    # get_role(role_id): Display only one role
    # update_role(role_id): Receive updated role details and reflect updated details in the db
    # soft_delete_role(role_id): Update role status to 0
    # restore_role(role_id): Update role status to 1

# ====================

#AL-25 -- View all -- 
@app.route("/roles")
def get_all():
    role_list = Role.query.all()
    if len(role_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "roles": [role.json() for role in role_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no roles."
        }
    ), 404


# AL-2 -- Add New --
@app.route("/roles/create", methods=['POST', 'GET'])
def create_role():
    data = request.get_json()
    role_list = Role.query.all()
    role_names = []
    for role in role_list:
        role_names.append(role.role_name.lower())

    if data['role_name'].lower() in role_names:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "role_name": data['role_name']
                },
                "message": "This role already exists."
            }
        ), 400

    if data['role_name'] == "":
        return jsonify(
            {
                "code": 400,
                "data": {
                    "role_name": data['role_name']
                },
                "message": "Role name cannot be empty."
            }
        ), 400

    if data['role_desc'] == "":
        return jsonify(
            {
                "code": 400,
                "data": {
                    "role_desc": data['role_desc']
                },
                "message": "Role description cannot be empty."
            }
        ), 400

    if data['role_status'] == "":
        return jsonify(
            {
                "code": 400,
                "data": {
                    "role_status": data['role_status']
                },
                "message": "Role status cannot be empty."
            }
        ), 400

    if data['role_sector'] == "":
        return jsonify(
            {
                "code": 400,
                "data": {
                    "role_sector": data['role_sector']
                },
                "message": "Role sector cannot be empty."
            }
        ), 400

    if data['role_track'] == "":
        return jsonify(
            {
                "code": 400,
                "data": {
                    "Role_track": data['role_track']
                },
                "message": "Role track cannot be empty."
            }
        ), 400

    role_id= role_list[-1].role_id +1
    role = Role(role_id=role_id, role_name=data['role_name'], role_desc=data['role_desc'], role_status=data['role_status'], role_sector=data['role_sector'], role_track=data['role_track'])

    try:
        db.session.add(role)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "role": role.role_name
                },
                "message": "An error occurred creating the role."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": role.json()
        }
    ), 201


@app.route("/roles/<int:role_id>")
def get_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    if role:
        return jsonify(role.json())

    return jsonify(
        {
            "code": 404,
            "message": "No role with this role ID.",
        }
    ), 404

# AL-3 & AL-18 Update --
@app.route("/roles/update/<int:role_id>", methods=['PUT', 'GET'])
def update_role(role_id):
    data = request.get_json()
    role = Role.query.filter_by(role_id=role_id).first()

    if role:
        if data["role_name"] == role.role_name and data["role_desc"] == role.role_desc and data["role_status"] == role.role_status and data["role_sector"] == role.role_sector and data["role_track"] == role.role_track:
            return jsonify({
                "code": 400,
                "message": "No changes made."
            }), 400
        # validation: check if no changes were made
        if data['role_name'] != role.role_name:
            if data['role_name'] != '':
                role.role_name = data['role_name']
            else:
                return jsonify({"code": 400, "message": "Role name cannot be empty."}), 400

        if data['role_desc'] != role.role_desc:
            if data['role_desc'] != '':
                role.role_desc = data['role_desc']
            else:
                return jsonify({"code": 400, "message": "Role description cannot be empty."}), 400

        if data['role_status'] != role.role_status:
            if data['role_status'] != '':
                role.role_status = data['role_status']
            else:
                return jsonify({"code": 400, "message": "Role status cannot be empty."}), 400

        if data['role_sector'] != role.role_sector:
            if data['role_sector'] != '':
                role.role_sector = data['role_sector']
            else:
                return jsonify({"code": 400, "message": "Role sector cannot be empty."}), 400

        if data['role_track'] != role.role_track:
            if data['role_track'] != '':
                role.role_track = data['role_track']
            else:
                return jsonify({"code": 400, "message": "Role track cannot be empty."}), 400

        try:
            db.session.commit()
            return jsonify({
                "code": 200,
                "data": role.json(),
                "message": "Role updated."
            })
        except:
            return jsonify({
                "code": 500,
                "message": "Role with the same name already exists."
            }), 500

    else:
        return jsonify({
            "code": 404,
            "message": "Role does not exist in database."
        }), 404


# AL-17 Delete --
@app.route("/roles/delete/<int:role_id>", methods=['DELETE'])
def soft_delete_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first() #find role from role id
    if role:
        if role.role_status == 0:
            return jsonify({
                "code": 400,
                "message": "Role is already retired."
            }), 400
        else:
            role.role_status = 0
        try:
            db.session.commit()
            return jsonify({
                "code": 200,
                "data": role.json(),
                "message": "Role retired."
            }), 200
        except:
            return jsonify({
                "code": 500,
                "message": "An error occurred while deleting the role."
            }), 500
    else:
        return jsonify({
            "code": 404,
            "message": "Role does not exist in database."
        }), 404

# AL-60 Restore --
@app.route("/roles/restore/<int:role_id>", methods=['PUT'])
def restore_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first() #find role from role id
    if role:
        if role.role_status == 1:
            return jsonify({
                "code": 400,
                "message": "Role is already active."
            }), 400
        else:
            role.role_status = 1
        try:
            db.session.commit()
            return jsonify({
                "code": 200,
                "data": role.json(),
                "message": "Role restored."
            }), 200
        except:
            return jsonify({
                "code": 500,
                "message": "An error occurred while restoring the role."
            }), 500
    else:
        return jsonify({
            "code": 404,
            "message": "Role does not exist in database."
        }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
