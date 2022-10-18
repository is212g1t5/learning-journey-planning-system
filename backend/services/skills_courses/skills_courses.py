from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors = CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SkillsCourses(db.Model):
    __tablename__ = 'skills_courses'
    skill_id = db.Column(db.Integer(), primary_key=True)
    course_id=  db.Column(db.String(20), primary_key=True)

    def __init__(self, skill_id, course_id):
        self.skill_id = skill_id
        self.course_id = course_id

    def json(self):
        return {"skills_id": self.skill_id, "course_id": self.course_id}

# -- view all skills_courses by course_id -- 
@app.route("/skills_courses/course/<string:course_id>")
def get_all_by_course(course_id):
    skills_courses_list = SkillsCourses.query.filter_by(course_id=course_id).all()
    if len(skills_courses_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skills_courses": [skills_courses.json() for skills_courses in skills_courses_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no skills_courses for this skill"
        }
    ), 404

# -- view all skills_courses by skill_id -- 
@app.route("/skills_courses/skill/<int:skill_id>")
def get_all_by_skills(skill_id):
    skills_courses_list = SkillsCourses.query.filter_by(skill_id=skill_id).all()
    if len(skills_courses_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skills_courses": [skills_courses.json() for skills_courses in skills_courses_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no skills_courses for this skill"
        }
    ), 404

## -- Create a new skills_courses --
@app.route("/skills_courses", methods=['POST'])
def create_skills_courses():
    data = request.get_json()
    skills_courses = SkillsCourses(**data)
    try:
        db.session.add(skills_courses)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "skills_courses": skills_courses.json()
                },
                "message": "An error occurred while creating the skills_courses."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": {
                "skills_courses": skills_courses.json()
            }
        }
    ), 201

## -- Map skills_courses --
@app.route("/skills_courses/map", methods=['POST'])
def map_skills_courses():
    data = request.get_json()
    skills = data["skill_ids"]
    course_id = data["course_id"]
    new_skills = [SkillsCourses(skill, course_id) for skill in skills]

    SkillsCourses.query.filter_by(course_id=course_id).delete()

    try:
        db.session.add_all(new_skills)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "skills_courses": [new_skill.json() for new_skill in new_skills]
                },
                "message": "An error occurred while creating the skills_courses."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": {
                "skills_courses": [new_skill.json() for new_skill in new_skills]
            }
        }
    ), 201

# -- Delete skills_courses by course_id --
@app.route("/skills_courses/delete/<string:course_id>/<int:skill_id>", methods=['DELETE'])
def delete_skills_courses(course_id, skill_id):
    skills_courses = SkillsCourses.query.filter_by(skill_id=skill_id,course_id=course_id).first()
    if skills_courses:
        db.session.delete(skills_courses)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skills_courses": skills_courses.json()
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "skills_courses not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)