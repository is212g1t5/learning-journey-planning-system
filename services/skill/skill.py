from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/LJPS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Skill(db.Model):
    __tablename__ = 'skills'

    skill_id = db.Column(db.Integer(), primary_key=True)
    skill_name = db.Column(db.String(64), nullable=False, unique=True)
    skill_category = db.Column(db.String(64), nullable=False)
    skill_desc = db.Column(db.String(64), nullable=False)
    skill_status = db.Column(db.Boolean(), nullable=False)

    def __init__(self, skill_id, skill_name, skill_category, skill_desc, skill_status):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_category = skill_category
        self.skill_desc = skill_desc
        self.skill_status = skill_status

    def json(self):
        return {"skill_id": self.skill_id, "skill_name": self.skill_name, "skill_category": self.skill_category, "skill_desc": self.skill_desc, "skill_status": self.skill_status}


@app.route("/skill/<string:skill_id>")
def get_skill(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    if skill:
        return jsonify(skill.json())


@app.route("/skill/update/<string:skill_id>", methods=['GET', 'PUT'])
def update_skill(skill_id):
    data = request.get_json()
    skill = Skill.query.filter_by(skill_id=skill_id).first()

    if skill:
        if data["skill_name"] == skill.skill_name and data["skill_category"] == skill.skill_category and data["skill_desc"] == skill.skill_desc and data["skill_status"] == skill.skill_status:
            return jsonify({
                "code": 400,
                "message": "No changes made."
            }), 400
        # validation: check if no changes were made
        if data['skill_name'] != skill.skill_name:
            if data['skill_name'] != '':
                skill.skill_name = data['skill_name']
            else:
                return jsonify({"code": 400, "message": "Skill name cannot be empty."}), 400

        if data['skill_category'] != skill.skill_category:
            if data['skill_category'] != '':
                skill.skill_category = data['skill_category']
            else:
                return jsonify({"code": 400, "message": "Skill category cannot be empty."}), 400

        if data['skill_desc'] != skill.skill_desc:
            if data['skill_desc'] != '':
                skill.skill_desc = data['skill_desc']
            else:
                return jsonify({"code": 400, "message": "Skill description cannot be empty."}), 400

        if data['skill_status'] != skill.skill_status:
            if data['skill_status'] != '':
                skill.skill_status = data['skill_status']
            else:
                return jsonify({"code": 400, "message": "Skill status cannot be empty."}), 400
        try:
            db.session.commit()
            return jsonify({
                "code": 200,
                "data": skill.json(),
                "message": "Skill updated."
            })
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


if __name__ == '__main__':
    app.run(port=5001, debug=True)
