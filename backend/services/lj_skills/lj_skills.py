from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors = CORS(app)  # enable CORS for all routes
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class LjSkills(db.Model):
    
    __tablename__ = 'lj_skills'

    learning_journey_id = db.Column(db.Integer(), primary_key=True)
    skill_id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column(db.Integer(), primary_key=True)

    def __init__(self, learning_journey_id, skill_id, role_id):
        self.learning_journey_id = learning_journey_id
        self.skill_id = skill_id
        self.role_id = role_id
    
    def json(self):
        return {"learning_journey_id": self.learning_journey_id, "skill_id": self.skill_id, "role_id": self.role_id}

#-- View all per learning_journey_id --
@app.route("/lj_skills/<int:learning_journey_id>")
def get_all_by_lj(learning_journey_id):
    lj_skill_list = LjSkills.query.filter_by(learning_journey_id=learning_journey_id).all()
    if len(lj_skill_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "lj_skills": [lj_skill.json() for lj_skill in lj_skill_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no lj_skills for this learning_journey"
        }
    ), 404

#--Create new lj_skill --
@app.route("/lj_skills/create", methods=['POST','GET'])
def create_lj_skill():
    data = request.get_json()
    lj_skill_list = LjSkills.query.all()
    if (len(lj_skill_list)):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "lj_skills": "lj_skill already exists."
                }
            }
        ), 400

    lj_skill = LjSkills(**data)

    try:
        db.session.add(lj_skill)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "lj_skills": "An error occurred creating the lj_skill."
                }
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": lj_skill.json()
        }
    ), 201

#-- Delete lj_skill --
@app.route("/lj_skills/delete/<int:learning_journey_id>/<int:skill_id>/<int:role_id>", methods=['DELETE'])
def delete_lj_skill(learning_journey_id, skill_id, role_id):
    lj_skill = LjSkills.query.filter_by(learning_journey_id=learning_journey_id, skill_id=skill_id, role_id=role_id).first()
    if lj_skill:
        db.session.delete(lj_skill)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "lj_skills": "lj_skill deleted."
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "lj_skills": "lj_skill not found."
            }
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)