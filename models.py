from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Event {self.name}>'


class ContactInfo(db.Model):
    __tablename__ = 'contact_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    phone_no = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return f'<ContactInfo {self.name}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact_info.id'), nullable=False)
    contact_info = db.relationship('ContactInfo', backref=db.backref('students', lazy=True))

    def __repr__(self):
        return f'<Student {self.contact_info.name}>'

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact_info.id'), nullable=False)
    contact_info = db.relationship('ContactInfo', backref=db.backref('staff', lazy=True))

    def __repr__(self):
        return f'<Staff {self.contact_info.name}>'

class EventManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact_info.id'), nullable=False)
    contact_info = db.relationship('ContactInfo', backref=db.backref('event_managers', lazy=True))

    def __repr__(self):
        return f'<EventManager {self.contact_info.name}>'