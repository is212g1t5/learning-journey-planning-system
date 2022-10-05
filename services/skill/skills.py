from os import environ
from flask import Flask, request, jsonify, abort
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:3306/LJPS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

 
db = SQLAlchemy(app)
CORS(app) 

class Skill(db.Model):
    __tablename__ = 'skills'

    skill_id = db.Column(db.Integer(), primary_key=True)
    skill_name = db.Column(db.String(64), nullable=False, unique=True)
    skill_category = db.Column(db.String(64), nullable=False)
    skill_desc = db.Column(db.String(64), nullable=False)
    skill_status = db.Column(db.Boolean(), nullable=False) #True = Active, False = Retired

    def __init__(self, skill_id, skill_name, skill_category, skill_desc, skill_status):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_category = skill_category
        self.skill_desc = skill_desc
        self.skill_status = skill_status

    def json(self):
        return {"skill_id": self.skill_id, "skill_name": self.skill_name, "skill_category": self.skill_category, "skill_desc": self.skill_desc, "skill_status": self.skill_status}

@app.route("/skills")
def get_skills():
    #skills = Skill.query.filter_by(skill_status=True) #this is for users to not see retired skills
    #return jsonify({"skills": [skill.json() for skill in skills]})
    return jsonify({"skills": [skill.json() for skill in Skill.query.all()]})

@app.route("/skills/delete/<string:skill_id>", methods=['DELETE'])
def soft_delete_skills(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first() #find skill from skill id
    if skill:
        if skill.skill_status == 0:
            return jsonify({
                "code": 400,
                "message": "Skill is already retired."
            }), 400
        else:
            skill.skill_status = 0
        try:
            db.session.commit()
            return jsonify({
                "code": 200,
                "data": skill.json(),
                "message": "Skill retired."
            }), 200
        except:
            return jsonify({
                "code": 500,
                "message": "An error occurred while updating the skill."
            }), 500
    else:
        return jsonify({
            "code": 404,
            "message": "Skill does not exist in database."
        }), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)