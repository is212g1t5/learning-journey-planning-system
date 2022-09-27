from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/LJPS'
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

@app.route("/roles/create", methods=['POST','GET'])
def create_role():
    data = request.get_json()
    role_list = Role.query.all()
    role_names = []
    for role in role_list:
        role_names.append(role.role_name)
    if data['role_name'] in role_names:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "role_name": data['role_name']
                },
                "message": "This role already exists."
            }
        ), 400
    if data['role_name'] == "" or data['role_desc'] == "":
        return jsonify(
            {
                "code": 400,
                "data": {
                    "role_name": data['role_name']
                },
                "message": "Role name pr role description cannot be empty ."
            }
        ), 400

    role_id= role_list[-1].role_id +1
    role = Role(role_id=role_id, role_name=data['role_name'], role_desc=data['role_desc'], role_status=data['role_status'])

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
if __name__ == '__main__':
    app.run(port=5000, debug=True)
