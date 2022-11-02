from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

from os import environ
from invokes import invoke_http

app = Flask(__name__)
cors = CORS(app)  # enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


role_URL = environ.get("role_URL") or "http://localhost:5002/"
lj_skill_URL = environ.get("lj_skill_URL") or "http://localhost:5007/"
skill_URL = environ.get("skill_URL") or "http://localhost:5001/"
lj_courses_URL = environ.get("lj_courses_URL") or "http://localhost:5009/"
registration_URL = environ.get("registration_URL") or "http://localhost:5012/"
skills_courses_URL = environ.get("skills_courses_URL") or "http://localhost:5005/"

class LearningJourney(db.Model):

    __tablename__ = 'learning_journeys'

    learning_journey_id = db.Column(db.Integer(), primary_key=True)
    learning_journey_name = db.Column(db.String(50), nullable=False)
    staff_id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column(db.Integer(), primary_key=True)


    def __init__(self, learning_journey_id, learning_journey_name, staff_id, role_id):
        self.learning_journey_id = learning_journey_id
        self.learning_journey_name = learning_journey_name
        self.staff_id = staff_id
        self.role_id = role_id

    def json(self):
        return {"learning_journey_id": self.learning_journey_id, "learning_journey_name": self.learning_journey_name, "staff_id": self.staff_id, "role_id": self.role_id}

# -- View all per staff_id --


@app.route("/learning_journeys/<int:staff_id>")
def get_all_by_staff(staff_id):
    learning_journey_list = LearningJourney.query.filter_by(
        staff_id=staff_id).all()
    if len(learning_journey_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "learning_journeys": [learning_journey.json() for learning_journey in learning_journey_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no learning_journeys for this staff"
        }
    ), 404


#-- Get ALL details for a learning_journey id --
@app.route("/learning_journeys/id/<int:learning_journey_id>")
def get_all_lj_details(learning_journey_id):
    # Get LJ name, staff_id, role_id
    learning_journey = LearningJourney.query.filter_by(learning_journey_id=learning_journey_id).first()

    if not learning_journey:
        return jsonify(
            {
                "code": 404,
                "message": "There are no learning journeys with this learning journey ID."
            }
        ), 404

    id = learning_journey.learning_journey_id
    name = learning_journey.learning_journey_name
    staff_id = learning_journey.staff_id
    role_id = learning_journey.role_id

    # Get LJ role details from role_id above
    individual_role_URL = role_URL + "roles/" + str(role_id)
    role_result = invoke_http(individual_role_URL, method='GET', json=None)
    role_name = role_result["role_name"]
    role_desc = role_result["role_desc"]
    role_status = role_result["role_status"]
    role_sector = role_result["role_sector"]
    role_track = role_result["role_track"]

    # Get LJ course mapped to these skills
    individual_lj_courses_URL = lj_courses_URL + "lj_courses/" + str(id)
    lj_courses_result = invoke_http(individual_lj_courses_URL, method="GET", json=None)
    list_of_courses = [row["course_id"] for row in lj_courses_result["data"]["lj_courses"]] if lj_courses_result["code"] in range(200, 300) else []

    courses = {}

    # Get whether im enrolled into the courses
    individual_staff_registration_URL = registration_URL + "registration/" + str(staff_id)
    staff_registration_result = invoke_http(individual_staff_registration_URL, method="GET", json=None)
    list_of_registration = staff_registration_result["data"]["registration"] if staff_registration_result["code"] in range(200, 300) else []

    if lj_courses_result["code"] in range(200, 300):
        for row in lj_courses_result["data"]["lj_courses"]:
            course_id = row["course_id"]
            status = ""

            for d in list_of_registration:
                if d.get('course_id') == course_id :
                    status = d['completion_status']
                    break

            courses[course_id] = {
                "status": status
            }

    # Get LJ skills
    individual_lj_skill_URL = lj_skill_URL + "lj_skills/" + str(id)
    lj_role_skill_result = invoke_http(individual_lj_skill_URL, method="GET", json=None)
    
    print(lj_role_skill_result)

    skills = {}
    if lj_role_skill_result["code"] in range(200, 300):
        for row in lj_role_skill_result["data"]["lj_skills"]:
            row_skill_id = row["skill_id"]
            individual_skill_URL = skill_URL + "skills/" + str(row_skill_id)
            skill_result = invoke_http(individual_skill_URL, method="GET", json=None)
            skills[row_skill_id] = skill_result
            # Get course_skill mapping
            lj_skills_courses_URL = skills_courses_URL + "skills_courses/skill/" + str(row_skill_id)
            skills_courses_result = invoke_http(lj_skills_courses_URL, method="GET", json=None)
            skills[row_skill_id]["mapping"] = [d["course_id"] for d in skills_courses_result["data"]["skills_courses"] if d["course_id"] in list_of_courses]  if skills_courses_result["code"] in range(200,300) else []

    

    # code_results = [role_result["code"], lj_role_skill_result["code"], skill_result["code"], skills_courses_result["code"], lj_courses_result["code"], staff_registration_result["code"]]

    response = {
        "learning_journey_id": id,
        "learning_journey_name": name,
        "staff_id": staff_id,
        "role": {
            "role_id": role_id,
            "role_name": role_name,
            "role_desc": role_desc,
            "role_status": role_status, 
            "role_sector": role_sector,
            "role_track": role_track
        },
        "skills": skills,
        "courses": courses
    }

    return jsonify(
        {
            "code": 200,
            "data": {
                "learning_journey": response
            }
        }
    ), 200


@app.route("/learning_journeys/single_journey/<int:learning_journey_id>")
def get_single_journey(learning_journey_id):
    learning_journey = LearningJourney.query.filter_by(
        learning_journey_id=learning_journey_id).first()
    if learning_journey:
        return jsonify(
            {
                "code": 200,
                "data": learning_journey.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Learning journey not found."
        }
    ), 404


# --Create new learning_journey --
@app.route("/learning_journeys/create", methods=['POST', 'GET'])
def create_learning_journey():

    data = request.get_json()
    learning_journey_list = LearningJourney.query.all()
    learning_journey_names = []
    for learning_journey in learning_journey_list:
        learning_journey_names.append(learning_journey.learning_journey_name)

    if data['learning_journey_name'] in learning_journey_names:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "learning_journey_name": data['learning_journey_name']
                },
                "message": "A learning_journey with name '{}' already exists.".format(data['learning_journey_name'])
            }
        ), 400

    if data['learning_journey_name'] == '':
        return jsonify(
            {
                "code": 400,
                "data": {
                    "learning_journey_name": data['learning_journey_name']
                },
                "message": "Learning Journey name cannot be empty."
            }
        ), 400

    learning_journey = LearningJourney(**data)
    try:
        db.session.add(learning_journey)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "learning_journey_name": data['learning_journey_name']
                },
                "message": "An error occurred creating the learning_journey."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": learning_journey.json()
        }
    ), 201

# -- Update Learning_Journey --


@app.route("/learning_journeys/update/<int:learning_journey_id>", methods=['PUT'])
def update_learning_journey(learning_journey_id):
    learning_journey = LearningJourney.query.filter_by(
        learning_journey_id=learning_journey_id).first()
    if learning_journey:
        data = request.get_json()
        if data['learning_journey_name'] != "":
            learning_journey.learning_journey_name = data['learning_journey_name']
        else:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "learning_journey_name": data['learning_journey_name']
                    },
                    "message": "learning journey name cannot be empty."
                }
            ), 400
        try:
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "learning_journey_id": learning_journey.learning_journey_id
                    },
                    "message": "An error occurred while updating the learning journey."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": learning_journey.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Learning Journey not found."
        }
    ), 404

## -- Delete Learning_Journey -- ##


@app.route("/learning_journeys/delete/<int:learning_journey_id>", methods=['DELETE'])
def delete_learning_journey(learning_journey_id):
    learning_journey = LearningJourney.query.filter_by(
        learning_journey_id=learning_journey_id).first()
    if learning_journey:
        try:
            db.session.delete(learning_journey)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "learning_journey_id": f"{learning_journey.learning_journey_id} has been deleted."
                    },
                    "message": "An error occurred while deleting the learning_journey."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": {
                    "learning_journey_id": learning_journey.learning_journey_id
                }
            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "message": "Learning_Journey not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
