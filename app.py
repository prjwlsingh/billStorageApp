"""

task list:
    1. Start server
    2. Make class for sql database
    3. write get and post API definitions

"""

app.config['S3_BUCKET'] = "S3_BUCKET_NAME"
app.config['S3_KEY'] = "AWS_ACCESS_KEY"
app.config['S3_SECRET'] = "AWS_ACCESS_SECRET"
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

from flask import *
import json
import sqlite3
from bill import Bill
import os
from dotenv import load_dotenv

load_dotenv()

import boto3, botocore

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

app = Flask(__name__)

# create db
def create_db():
    c = sqlite3.connect("bill.db").cursor()
    c.execute("CREATE TABLE IF NOT EXISTS BILL("
              "id TEXT, title TEXT, description TEXT, tag TEXT, date TEXT, cloudPath TEXT, userId TEXT)"
              )
    
    c.execute("CREATE TABLE IF NOT EXISTS USER("
              "userId TEXT)"
              )
    c.connection.close()

@app.route('/', methods=['GET'])
def create_db():
    create_db()
    return 'bill and user DB created'

"""
there are 4 app routes
1. retrieve list of user bills
2. post image 
3. retrieve bill using bill id
4. create bill to put in db


"""

# get list of user bills from db
@app.route('/getUserBill', methods=['GET'])
def get_userBills(userId):
    c = sqlite3.connect("bill.db").cursor()
    c.execute("SELECT * FROM BILL WHERE userId=?", userId)
    data = c.fetchall()
    return jsonify(data)



# get a bill with particular bill id
@app.route('/getBill', methods=['GET'])
def get_bill(billId):
    c = sqlite3.connect("bill.db").cursor()
    c.execute("SELECT * FROM BILL WHERE id=?", billId)
    data = c.fetchall()
    return jsonify(data)



# post bill into db
@app.route('/createBill', methods=['POST','GET'])
def create_bill(payload):
    db = sqlite3.connect("bill.db")
    c = db.cursor()
    bill = Bill(request.form["billTitle"],
                request.form["billDescription"],
                request.form["tag"],
                request.form["date"],
                request.form["cloudPath"],
                request.form["userID"]
                )   

    c.execute("INSERT INTO bill VALUES(?,?,?,?,?)",
              (bill.id, bill.title, bill.description, bill.tag, bill.date, bill.cloudPath, bill.userId))
    
    db.commit()
    data = c.lastrowid
    return json.dumps(data)

   

# post image to cloud
@app.route('/postImage', methods=['POST', 'GET'])
def post_image():
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)

    else:
        return redirect("/")


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], file.filename)

#server

if __name__ == '__main__':
    app.run(port=8888)
