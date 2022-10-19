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

class LjCourses(db.Model):
    
    __tablename__ = 'lj_courses'

    learning_journey_id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.String(20), primary_key=True)

    def __init__(self, learning_journey_id, course_id):
        self.learning_journey_id = learning_journey_id
        self.course_id = course_id
    
    def json(self):
        return {"learning_journey_id": self.learning_journey_id, "course_id": self.course_id}

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