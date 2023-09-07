from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType
import datetime
import uuid

# wrapper functions
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# database schema
class BillModel(db.Model):
    __tablename__ = 'bills'


    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    tag = db.Column(db.String(20), nullable=False)
    dateTaken = db.Column(db.Text, nullable = False)
    imagePath = db.Column(db.Text, nullable = False)
    userId = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'), default=uuid.uuid4, nullable=False)


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    bills = db.relationship('BillModel', backref='users', cascade='all, delete, delete-orphan')

with app.app_context():
    db.drop_all()
    db.create_all()

# used to store provided values into dictionary
bill_put_args = reqparse.RequestParser()
bill_put_args.add_argument("title", type=str, help="Title is required", location = 'form', required = True)
bill_put_args.add_argument("description", type=str, help="Description is required", location = 'form', required = True)
bill_put_args.add_argument("tag", type=str, help="Tag is required", location = 'form', required = True)
bill_put_args.add_argument("dateTaken", type=str, help="Title is required", location = 'form', required = True)
bill_put_args.add_argument("imagePath", type=str, help="imagePath not provided", location = 'form', required = True)
bill_put_args.add_argument("userId", type=str, help="userId not provided", location = 'form', required = True)

user_put_args = reqparse.RequestParser()


# used to serialize the object
resource_fields_bill = {
    'id' : fields.String,
    'title' : fields.String,
    'description' : fields.String,
    'tag' : fields.String,
    'dateTaken' : fields.String,
    'imagePath' : fields.String,
    'userId' : fields.String
}

resource_fields_user = {
    'id' : fields.String
}

# get and post requests for the db

class Bill(Resource):
    @marshal_with(resource_fields_bill) # take return value and serailize using defined fields
    def get(self, billId):
        result = BillModel.query.filter_by(id=billId).first()
        if not result:
            abort(404, message='could not find the bill with given id')
        return result
    
    @marshal_with(resource_fields_bill)
    def post(self, billId):
        args = bill_put_args.parse_args()

        bill = BillModel(title=args["title"],
                        description=args["description"],
                        tag=args["tag"],
                        dateTaken=args["dateTaken"],
                        imagePath=args["imagePath"],
                        userId=args["userId"])

        db.session.add(bill)
        db.session.commit()

        return bill, 201

class User(Resource):
    @marshal_with(resource_fields_user)    
    def post(self):
        args = user_put_args.parse_args()

        user = UserModel()
        db.session.add(user)
        db.session.commit()
        userID = db.session.query(UserModel).order_by(UserModel.id.desc()).first()
        return userID , 201  


api.add_resource(Bill, "/bill/<string:billId>/")
api.add_resource(User, "/user/")

if __name__ == '__main__':
    app.run(debug=True)
