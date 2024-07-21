from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

user_courses = db.Table('user_courses',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.UniqueConstraint('member_id', 'course_id', name='uix_member_course')
)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)
    
    orders = db.relationship('Order', backref='member', lazy='dynamic')
    courses = db.relationship('Course', secondary=user_courses, back_populates='members', lazy='dynamic')

    def __repr__(self):
        return f"<Member {self.username}>"
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    
    def __repr__(self):
        return f"<Order {self.price}>"
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    members = db.relationship('Member', secondary=user_courses, back_populates='courses', lazy='dynamic')

    def __repr__(self):
        return f"<Course {self.name}>"

if __name__ == "__main__":
    app.run()
