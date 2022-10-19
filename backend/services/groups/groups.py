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

class Groups(db.Model):
    __tablename__ = 'groups'
    group_id = db.Column(db.Integer(), primary_key=True )
    group_name=  db.Column(db.String(20), primary_key=True)

    def __init__(self, group_id, group_name):
        self.group_id = group_id
        self.group_name = group_name
    
    def json(self):
        return {"group_id": self.group_id, "group_name": self.group_name}

## View all per group_id
@app.route("/groups/<int:group_id>")
def get_all_by_group(group_id):
    group_list = Groups.query.filter_by(group_id=group_id).all()
    if len(group_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "groups": [group.json() for group in group_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no groups for this group"
        }
    ), 404

app.run(host='0.0.0.0', port=5010, debug=True)