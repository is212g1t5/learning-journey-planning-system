from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
import sys
sys.path.append('../')
# from lj_skills.lj_skills import LjSkills
# from course.course import Course
# from skill.skill import Skills
# from learning_journey.learning_journey import LearningJourney
# from registration.registration import Registration
# from skills_courses.skills_courses import SkillsCourses

app = Flask(__name__)
cors = CORS(app)  # enable CORS for all routes
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class LjCourses(db.Model):
    
    __tablename__ = 'lj_courses'

    learning_journey_id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.String(20), primary_key=True)

    def __init__(self, learning_journey_id, course_id):
        self.learning_journey_id = learning_journey_id
        self.course_id = course_id
    
    def json(self):
        return {"learning_journey_id": self.learning_journey_id, "course_id": self.course_id}

# ##Get Course for a specific user journey
# @app.route("/lj_courses/details/<int:staff_id>/<int:learning_journey_id>")
# def get_course_by_lj(learning_journey_id,staff_id):
    
#     lj_course_list = db.session.query(LjCourses.learning_journey_id)\
#         .filter(LjCourses.learning_journey_id == learning_journey_id)\
#         .join(Course, LjCourses.course_id == Course.course_id)\
#         .join(LearningJourney, LjCourses.learning_journey_id == LearningJourney.learning_journey_id)\
#         .add_columns(Course.course_id, Course.course_name,LearningJourney.staff_id,LearningJourney.learning_journey_name)\
#         .all()
#     # [
#     # (1, 'COR001', 'Systems Thinking and Design', 130001, 'learning journey 1'), 
#     # (1, 'COR002', 'Lean Six Sigma Green Belt Certification', 130001, 'learning journey 1')
#     # ]

#     lj_skill_list = db.session.query(LjSkills.learning_journey_id)\
#         .filter(LjSkills.learning_journey_id == learning_journey_id)\
#         .join(Skills, LjSkills.skill_id == Skills.skill_id)\
#         .add_columns(Skills.skill_id, Skills.skill_name)\
#         .all()
    
#     # [(1, 1, 'Creative Thinking'), (1, 2, 'Front-End Engineering and Design')]
#     skills_courses_list =[]
#     skills_courses = SkillsCourses.query.all()
#     for skill_course in skills_courses:
#         skills_courses_list.append(skill_course.json())
#     # print(skills_courses_list)

#     staff_reg_List = db.session.query(Registration.staff_id)\
#         .filter(Registration.staff_id == staff_id)\
#         .join(Course, Registration.course_id == Course.course_id)\
#         .add_columns(Course.course_id, Course.course_name,Registration.completion_status)\
#         .all()
#     # [(130001, 'COR002', 'Lean Six Sigma Green Belt Certification', 'Completed'), (130001, 'COR001', 'Systems Thinking and Design', 'Completed')]
#     # print(staff_reg_List)
#     final_results = []
    
#     ## GET all course name, completion_staus, skill name
#     for lj_course in lj_course_list:
#         for staff_reg in staff_reg_List:
#             if lj_course[1] == staff_reg[1]:
#                 final_results.append({"learning_journey_id": lj_course[0], "course_id": lj_course[1], "course_name": lj_course[2], "staff_id": lj_course[3], "learning_journey_name": lj_course[4], "course_progress": staff_reg[3]})
#     for res in final_results:
#         skill_name =""
#         for lj_skill in lj_skill_list:
#             for skills_courses in skills_courses_list:
#                 if res["course_id"] == skills_courses["course_id"] and lj_skill[1] == skills_courses["skill_id"]:
#                     skill_name += lj_skill[2] + ", "
#         res["skill_name"] = skill_name[:-2]
    

    
#     ## Insert Skill name into final_results

#     # print(lj_course_list)
#     if len(final_results):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [res for res in final_results
#                 ]
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "No course found."
    #     }
    # ), 404
    
## View all per learning_journey_id
@app.route("/lj_courses/<int:learning_journey_id>")
def get_all_by_lj(learning_journey_id):
    lj_course_list = LjCourses.query.filter_by(learning_journey_id=learning_journey_id).all()
    if len(lj_course_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "lj_courses": [lj_course.json() for lj_course in lj_course_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no lj_courses for this learning_journey"
        }
    ), 404

## Create new lj_course
@app.route("/lj_courses/create", methods=['POST','GET'])
def create_lj_course():
    data = request.get_json()
    lj_course_list = LjCourses.query.all()
    if (len(lj_course_list)):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "lj_courses": "lj_course already exists."
                }
            }
        )
    lj_course = LjCourses(**data)
    try:
        db.session.add(lj_course)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "lj_courses": "An error occurred creating the lj_course."
                }
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": lj_course.json()
        }
    ), 201

## -- Delete --
@app.route("/lj_courses/delete/<int:learning_journey_id>/<string:course_id>", methods=['DELETE'])

def delete_lj_course(learning_journey_id,course_id):
    lj_course = LjCourses.query.filter_by(learning_journey_id=learning_journey_id,course_id=course_id).first()
    if lj_course:
        db.session.delete(lj_course)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "lj_course": "lj_course deleted."
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "lj_course not found."
        }
    ), 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)