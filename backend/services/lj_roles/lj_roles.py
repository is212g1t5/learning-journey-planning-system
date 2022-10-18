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

class LjRoles(db.Model):
    learning_journey_id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column(db.Integer(), primary_key=True)

    def __init__(self, learning_journey_id, role_id):
        self.learning_journey_id = learning_journey_id
        self.role_id = role_id
    
    def json(self):
        return {"learning_journey_id": self.learning_journey_id, "role_id": self.role_id}

#-- View all per learning_journey_id --
@app.route("/lj_roles/<int:learning_journey_id>")
def get_all_by_lj(learning_journey_id):
    lj_role_list = LjRoles.query.filter_by(learning_journey_id=learning_journey_id).all()
    if len(lj_role_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "lj_roles": [lj_role.json() for lj_role in lj_role_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no lj_roles for this learning_journey"
        }
    ), 404

## -- Create new lj_role -- 
@app.route("/lj_roles/create", methods=['POST','GET'])
def create_lj_role():
    data = request.get_json()
    lj_role_list = LjRoles.query.all()
    if (len(lj_role_list)):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "lj_roles": "lj_role already exists."
                }
            }
        )
    lj_role = LjRoles(**data)
    try:
        db.session.add(lj_role)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "lj_roles": "An error occurred creating the lj_role."
                }
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": lj_role.json()
        }
    ), 201

## -- Delete lj_role --
@app.route("/lj_roles/delete/<int:learning_journey_id>/<int:role_id>", methods=['DELETE'])
def delete_lj_role(learning_journey_id, role_id):
    lj_role = LjRoles.query.filter_by(learning_journey_id=learning_journey_id, role_id=role_id).first()
    if lj_role:
        db.session.delete(lj_role)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "lj_roles": "lj_role deleted."
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "lj_roles": "lj_role not found."
            }
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
