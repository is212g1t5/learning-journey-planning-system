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

class Registration(db.Model):
    __tablename__ = 'registration'

    reg_id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.String(20), nullable=False)
    staff_id = db.Column(db.Integer(), nullable=False)
    reg_status = db.Column(db.String(11), nullable=False)
    completion_status = db.Column(db.String(20), nullable=False)

    def __init__(self, reg_id, course_id, staff_id, reg_status, completion_status):
        self.reg_id = reg_id
        self.course_id = course_id
        self.staff_id = staff_id
        self.reg_status = reg_status
        self.completion_status = completion_status
    
    def json(self):
        return{"reg_id": self.reg_id, "course_id": self.course_id, "staff_id": self.staff_id, "reg_status": self.reg_status, "completion_status": self.completion_status}

# View Registration Details
@app.route("/registration")
def get_all():
    registration_list = Registration.query.all()
    if len(registration_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "registration": [registration.json() for registration in registration_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no registrations."
        }
    ), 404

# View Registration Details by staff_id
@app.route("/registration/<int:staff_id>")
def find_by_staff_id(staff_id):
    registration_list = Registration.query.filter_by(staff_id=staff_id)
    if registration_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "registration": [registration.json() for registration in registration_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Registration not found."
        }
    ), 404

# View Registration Details by staff_id
@app.route("/registration/<int:staff_id>")
def find_by_staff_id(staff_id):
    registration_list = Registration.query.filter_by(staff_id=staff_id)
    if registration_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "registration": [registration.json() for registration in registration_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Registration not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)