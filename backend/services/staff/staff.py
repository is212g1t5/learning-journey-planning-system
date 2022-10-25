from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors = CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Staff(db.Model):
        
        __tablename__ = 'staffs'
    
        staff_id = db.Column(db.Integer(), primary_key=True)
        staff_fname = db.Column(db.String(50), nullable=False)
        staff_lname = db.Column(db.String(50), nullable=False)
        dept= db.Column(db.String(50), nullable=False)
        email = db.Column(db.String(50), nullable=False)
        group = db.Column(db.Integer(), nullable=False)

        def __init__(self, staff_id, staff_fname, staff_lname, dept, email, group):
            self.staff_id = staff_id
            self.staff_fname = staff_fname
            self.staff_lname = staff_lname
            self.dept = dept
            self.email = email
            self.group = group
        
        def json(self):
            return{"staff_id": self.staff_id, "staff_fname": self.staff_fname, "staff_lname": self.staff_lname, "dept": self.dept, "email": self.email, "group": self.group}

# View Staff Details
@app.route("/staffs")
def get_all():
    staff_list = Staff.query.all()
    if len(staff_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "staffs": [staff.json() for staff in staff_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no staffs."
        }
    ), 404

# View Staff Details by group
@app.route("/staffs/<int:group>")
def find_by_group(group):
    staff_list = Staff.query.filter_by(group=group)
    if staff_list:
        return jsonify(
            {
                "code": 200,
                "data": staff_list.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No staffs found."
        }
    ), 404
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)