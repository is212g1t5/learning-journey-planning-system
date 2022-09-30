# skills service

from flask import Flask, request, jsonify # web framework
from flask_sqlalchemy import SQLAlchemy # for database (ORM)

from os import environ # access env variable

# ====================

#   F L A S K  &  D B  S E T U P

# ====================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Skills(db.Model):
    __tablesname__ = "skills"

    skill_id = db.Column(db.Integer, primary_key = True, nullable=True)
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
    # xxxx(): xxxx

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

    # Create new skill instance
    newSkill = Skills(skill_id, skill_name, skill_category, skill_desc, skill_status)
    
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)