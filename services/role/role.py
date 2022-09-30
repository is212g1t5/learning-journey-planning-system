from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(64), nullable=False)
    role_desc = db.Column(db.String(64), nullable=False)
    role_status = db.Column(db.Boolean(), nullable=False)

    def __init__(self, role_id, role_name, role_desc, role_status):
        self.role_id = role_id
        self.role_name = role_name
        self.role_desc = role_desc
        self.role_status = role_status

    def json(self):
        return {"role_id": self.role_id, "role_name": self.role_name, "role_desc": self.role_desc, "role_status": self.role_status}

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
        print(data['role_name'])
        return jsonify(
            {
                "code": 409,
                "data": {
                    "role_name": data['role_name'].lower()
                },
                "message": "This role already exists."
            }
        ), 400
    if data['role_name'] == "" or data['role_desc'] == "":
        return jsonify(
            {
                "code": 409,
                "data": {
                    "role_name": data['role_name']
                },
                "message": "Role name or role description cannot be empty."
            }
        ), 400

    role_id= role_list[-1].role_id +1
    role = Role(role_id=role_id, role_name=data['role_name'].lower(), role_desc=data['role_desc'].lower(), role_status=data['role_status'])

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
@app.route("/roles/update/<int:role_id>", methods=['POST','GET'])
def update_role(role_id):
    pass


#AL-17 --Delete--
@app.route("/roles/delete/<int:role_id>", methods=['DELETE'])
def delete_role(role_id):
    pass




if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)
