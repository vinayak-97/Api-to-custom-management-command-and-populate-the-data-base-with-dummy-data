import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#intialization
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#data base
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#intialization of the db
db = SQLAlchemy(app)
#intialization of mashmallow
ma = Marshmallow(app)

#memeber class/model
class Members(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    tz = db.Column(db.String(80))
    start_time = db.Column(db.String(80))
    end_time = db.Column(db.String(80))

    def __init__(self,name,tz,start_time,end_time):
        #self.id = id
        self.name = name
        self.tz = tz
        self.start_time = start_time
        self.end_time = end_time

#db.create_all()
#member schema
class MemberSchema(ma.Schema):
    class meta:
        fields = ('id','name','tz','start_time','end_time')


#init schema
member_schema = MemberSchema()
members_schema =MemberSchema(many=True)


#create a member
@app.route("/member",methods=["POST"])
def add_member():
    name = request.json['name']
    tz = request.json['tz']
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    
    new_member = Members(name,tz,start_time,end_time)
    db.session.add(new_member)
    db.session.commit()

    return member_schema.jsonify(new_member)

#get all memebers

@app.route("/member",methods=["GET"])
def get_members():
    all_members = Members.query.all()
    result = members_schema.dump(all_members)
    return jsonify(result)

@app.route("/member/<id>",methods=["GET"])
def get_member(id):
    member = Members.query.get(id)
    return member_schema.jsonify(member)

@app.route("/member/<id>",methods=["PUT"])
def update_member(id):
    member = Members.query.get(id)
    name = request.json['name']
    tz = request.json['tz']
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    
    member.name = name
    member.tz = tz
    member.start_time = start_time
    member.end_time = end_time

    
    db.session.commit()

    return member_schema.jsonify(member)

#delete member
@app.route("/member/<id>",methods=["DELETE"])
def delete_member(id):
    member = Members.query.get(id)
    db.session.delete(member)
    db.session.commit()
    return member_schema.jsonify(member)



#run server

if __name__ == "__main__":
    app.run(debug=True)
