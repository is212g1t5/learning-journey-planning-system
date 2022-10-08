from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/ljps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class LearningJourney(db.Model):
    
    __tablename__ = 'learning_journeys'

    learning_journey_id = db.Column(db.Integer(), primary_key=True)
    learning_journey_name = db.Column(db.String(50), nullable=False)
    staff_id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(64), nullable=False)


    def __init__(self, learning_journey_id, learning_journey_name, staff_id, role_id,role_name):
        self.learning_journey_id = learning_journey_id
        self.learning_journey_name = learning_journey_name
        self.staff_id = staff_id
        self.role_id = role_id
        self.role_name = role_name


    def json(self):
        return {"learning_journey_id": self.learning_journey_id, "learning_journey_name": self.learning_journey_name, "staff_id": self.staff_id, "role_id": self.role_id, "role_name": self.role_name}

#-- View all per staff_id --
@app.route("/learning_journeys/<int:staff_id>")
def get_all_by_staff(staff_id):
    learning_journey_list = LearningJourney.query.filter_by(staff_id=staff_id).all()
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


#--Create new learning_journey --
@app.route("/learning_journeys/create", methods=['POST','GET'])
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

#-- Update Learning_Journey --
@app.route("/learning_journeys/update/<int:learning_journey_id>", methods=['PUT'])
def update_learning_journey(learning_journey_id):
    learning_journey = LearningJourney.query.filter_by(learning_journey_id=learning_journey_id).first()
    if learning_journey:
        data = request.get_json()
        if data['learning_journey_name'] != "":
            learning_journey.learning_journey_name = data['learning_journey_name']
        else:
            return jsonify(
                {
                    "code": 409,
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
                "code": 201,
                "data": learning_journey.json()
            }
        ),201
    return jsonify(
        {
            "code": 404,
            "message": "Learning Journey not found."
        }
    ), 404

## -- Delete Learning_Journey -- ##
@app.route("/learning_journeys/delete/<int:learning_journey_id>", methods=['DELETE'])
def delete_learning_journey(learning_journey_id):
    learning_journey = LearningJourney.query.filter_by(learning_journey_id=learning_journey_id).first()
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
                "code": 202,
                "data": {
                    "learning_journey_id": learning_journey.learning_journey_id
                }
            }
        ),202

    return jsonify(
        {
            "code": 404,
            "message": "Learning_Journey not found."
        }
    ), 404 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

