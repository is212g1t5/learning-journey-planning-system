from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__ = 'courses'

    course_id = db.Column(db.String(24), primary_key=True)
    course_name = db.Column(db.String(64), nullable=False)
    course_desc = db.Column(db.String(250), nullable=False)
    course_status = db.Column(db.Integer, nullable=False)
    course_type = db.Column(db.String(10), nullable=False)
    course_category = db.Column(db.String(50), nullable=False)

    def __init__(self, course_id, course_name, course_desc,course_status,course_type,course_category):
        self.course_id = course_id
        self.course_name = course_name
        self.course_desc = course_desc
        self.course_status = course_status
        self.course_type = course_type
        self.course_category = course_category

    def json(self):
        return{"course_id": self.course_id, "course_name": self.course_name, "course_desc": self.course_desc, "course_status": self.course_status, "course_type": self.course_type, "course_category": self.course_category}

#-- AL-20 -- View All Courses --
@app.route("/courses")
def get_all():
    course_list = Course.query.all()
    if len(course_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": [course.json() for course in course_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no courses."
        }
    ), 404


# -- Find Course by ID --
@app.route("/courses/<string:course_id>")
def find_by_name(course_id):
    course_list = Course.query.all()
    if len(course_list):
        course = Course.query.filter_by(course_id=course_id).first()
        if course:
            return jsonify(
                {
                    "code": 200,
                    "data": course.json()
                }
            )
    return jsonify(
        {
            "code": 404,
            "data": {
                "course_id": course_id
            },
            "message": "Course not found."
        }
    ), 404

# -- Update Courses --
@app.route("/courses/update/<string:course_id>", methods=['PUT'])
def update_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        data = request.get_json()
        if data['course_name'] != '':
            course.course_name = data['course_name']
        else:
            return jsonify(
                {
                    "code": 409,
                    "data": {
                        "course_name": data['course_name']
                    },
                    "message": "Course name cannot be empty."
                }
            ), 409
        if data['course_desc'] != '':
            course.course_desc = data['course_desc']
        else:
            return jsonify(
                {
                    "code": 409,
                    "data": {
                        "course_desc": data['course_desc']
                    },
                    "message": "Course description cannot be empty." 
                }
            ), 409
        if data['course_status'] != '':

            course.course_status = data['course_status']
        else:
            return jsonify(
                {
                    "code": 409,
                    "data": {
                        "course_status": data['course_status']
                    },
                    "message": "Course status cannot be empty."
                }
            ), 409
        if data['course_type'] != '':
            course.course_type = data['course_type']
        else:
            return jsonify(
                {
                    "code": 409,
                    "data": {
                        "course_type": data['course_type']
                    },
                    "message": "Course type cannot be empty."
                }
            ), 409
        if data['course_category'] != '':
            course.course_category = data['course_category']
        else:
            return jsonify(
                {
                    "code": 409,
                    "data": {
                        "course_category": data['course_category']
                    },
                    "message": "Course category cannot be empty."
                }
            ), 409
        try:
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "course_id": course_id
                    },
                    "message": "An error occurred while updating the course."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": course.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "data": {
                "course_id": course_id
            },
            "message": "Course not found."
        }
    ), 404

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=5003, debug=True)

# 