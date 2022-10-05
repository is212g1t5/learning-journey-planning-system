# skills service

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


class Skills(db.Model):
    __tablesname__ = "skills"

    skill_id = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_name = db.Column(db.String(64), nullable=False)
    skill_category = db.Column(db.String(64), nullable=False)
    skill_desc = db.Column(db.String(256), nullable=False)
    skill_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, skill_id, skill_name, skill_category, skill_desc, skill_status):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_category = skill_category
        self.skill_desc = skill_desc
        self.skill_status = 1 if skill_status is None else skill_status

    def json(self):
        dto = {
            'skill_id': self.skill_id,
            'skill_name': self.skill_name,
            'skill_category': self.skill_category,
            'skill_desc': self.skill_desc,
            'skill_status': self.skill_status
        }

        return dto

# ====================

#   A P I  E N D P O I N T S

    # create_skill(): Receive new skill details and create new skill into the db
    # xxxx(): xxxx
    # soft_delete_skills(skill_id): Update skill status to 0

# ====================


@app.route("/skills/create", methods=['POST'])
def create_skill():
    '''
        Takes in POST inputs for json object skill with the following details:
            - skill_name
            - skill_category
            - skill_desc
            - skill_status [Optional, default: True]
        creates a skill in the skill table
        and returns a created table or error code
    '''

    if request.is_json:
        skill = request.get_json()
        print("\nReceived skill in JSON:", skill)
        result = processCreateSkill(skill)
        return result

    # 400 Bad Request - not a JSON request
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processCreateSkill(skill):
    # JSON body values
    skill_id = None
    skill_name = request.json.get("skill_name")
    skill_category = request.json.get("skill_category")
    skill_desc = request.json.get("skill_desc")
    skill_status = request.json.get("skill_status")

    if "" in (skill_name, skill_category, skill_desc):
        # 400 Bad Request - has empty arguments or arguments not passed
        return jsonify({
            "code": 400,
            "message": "Empty inputs or Invalid JSON input: " + str(request.get_data())
        }), 400

    # Create new skill instance
    newSkill = Skills(skill_id, skill_name, skill_category,
                      skill_desc, skill_status)

    # Stage and commit into db
    try:
        db.session.add(newSkill)
        status = db.session.commit()
        print(status)
    except:
        # 500 Internal Server Error - Server unable to commit into db for unknown reason(s)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the skill."
            }
        ), 500

    # 201 Created - Request success, new resource created
    return jsonify(
        {
            "code": 201,
            "data": newSkill.json()
        }
    ), 201


@app.route("/skills/<string:skill_id>")
def get_skill(skill_id):
    skill = Skills.query.filter_by(skill_id=skill_id).first()
    if skill:
        return jsonify(skill.json())


@app.route("/skills/update/<string:skill_id>", methods=['PUT'])
def update_skill(skill_id):
    data = request.get_json()
    skill = Skills.query.filter_by(skill_id=skill_id).first()

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

@app.route("/skills/delete/<string:skill_id>", methods=['DELETE'])
def soft_delete_skills(skill_id):
    skill = Skills.query.filter_by(skill_id=skill_id).first() #find skill from skill id
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
                "message": "An error occurred while deleting the skill."
            }), 500
    else:
        return jsonify({
            "code": 404,
            "message": "Skill does not exist in database."
        }), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
