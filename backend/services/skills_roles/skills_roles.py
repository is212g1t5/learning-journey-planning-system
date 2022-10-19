from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors = CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SkillsRoles(db.Model):
    __tablename__ = 'skills_roles'
    skill_id = db.Column(db.Integer(), primary_key=True )
    role_id=  db.Column(db.Integer(), primary_key=True)

    def __init__(self, skill_id, role_id):
        self.skill_id = skill_id
        self.role_id = role_id

    def json(self):
        return {"skills_id": self.skill_id, "role_id": self.role_id}

## -- view all skills_roles by role_id --
@app.route("/skills_roles/<int:role_id>")
def get_all_by_roles(role_id):
    skills_roles_list = SkillsRoles.query.filter_by(role_id=role_id).all()
    if len(skills_roles_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skills_roles": [skills_roles.json() for skills_roles in skills_roles_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no skills_roles for this role"
        }
    ), 404

## -- Create a new skills_roles --
@app.route("/skills_roles", methods=['POST'])
def create_skills_roles():
    data = request.get_json()
    skills_roles = SkillsRoles(**data)
    try:
        db.session.add(skills_roles)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "skills_roles": skills_roles.json()
                },
                "message": "An error occurred while creating the skills_roles."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": skills_roles.json(),
            "message": "skills_roles created successfully."
        }
    ), 201

## -- Delete a skills_roles --
@app.route("/skills_roles/<int:skill_id>/<int:role_id>", methods=['DELETE'])
def delete_skills_roles(skill_id, role_id):
    skills_roles = SkillsRoles.query.filter_by(skill_id=skill_id, role_id=role_id).first()
    if skills_roles:
        db.session.delete(skills_roles)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skill_id": skill_id,
                    "role_id": role_id
                }
            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "message": "skills_roles not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)