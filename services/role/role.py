from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ljps'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Role(db.Model):
    
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(64), nullable=False)
    role_desc = db.Column(db.String(64), nullable=False)
    role_status = db.Column(db.Boolean(), nullable=False)
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
@app.route("/roles/create", methods=['POST','GET'])
def create_role():
    data = request.get_json()
    role_list = Role.query.all()
    role_names = []
    for role in role_list:
        role_names.append(role.role_name.lower())

    if data['role_name'].lower() in role_names:
        return jsonify(
            {
                "code": 409,
                "data": {
                    "role_name": data['role_name'].lower()
                },
                "message": "This role already exists."
            }
        ), 400

    if data['role_name'] == "":
        return jsonify(
            {
                "code": 409,
                "data": {
                    "role_name": data['role_name']
                },
                "message": "Role name cannot be empty."
            }
        ), 400
        
    if data['role_desc'] == "":
        return jsonify(
            {
                "code": 409,
                "data": {
                    "role_desc": data['role_desc']
                },
                "message": "Role description cannot be empty."
            }
        ), 400

    if data['role_status'] == "":
        return jsonify(
            {
                "code": 409,
                "data": {
                    "role_status": data['role_status']
                },
                "message": "Role status cannot be empty."
            }
        ), 400
    
    if data['role_sector'] == "":
        return jsonify(
            {
                "code": 409,
                "data": {
                    "role_sector": data['role_sector']
                },
                "message": "Role sector cannot be empty."
            }
        ), 400
    
    if data['role_track'] == "":
        return jsonify(
            {
                "code": 409,
                "data": {
                    "Role_track": data['role_track']
                },
                "message": "Role track cannot be empty."
            }
        ), 400


    role_id= role_list[-1].role_id +1
    role = Role(role_id=role_id, role_name=data['role_name'].lower(), role_desc=data['role_desc'].lower(), role_status=data['role_status'], role_sector=data['role_sector'].lower(), role_track=data['role_track'].lower())

    try:
        db.session.add(role)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "role": role.role_name.lower()
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

# AL-3 & AL-18 -- Update --
@app.route("/roles/update/<int:role_id>", methods=['PUT','GET'])
def update_role(role_id):
    pass


#AL-17 --hide_role--
@app.route("/roles/delete/<int:role_id>", methods=['PUT'])
def hide_role(role_id):
    pass




if __name__ == '__main__':
    app.run(port=5000, debug=True)
