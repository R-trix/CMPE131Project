from myapp import myobj
from myapp import db


db.create_all()

myobj.run(debug=True)

"""
Helpful db commands:
User.query.filter_by(id=123).delete() //filters in a db by specific variable information

"""