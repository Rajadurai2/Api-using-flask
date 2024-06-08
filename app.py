from flask import Flask, request, jsonify
from config import Config
from models import db, Event,ContactInfo,Student,Staff,EventManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3 


app = Flask(__name__)
app.config.from_object(Config)

connect = sqlite3.connect('database.db') 

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    contact = ContactInfo(
        name=data['name'],
        email=data['email'],
        phone_no=data['phone_no'],
        password=hashed_password
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    contact = ContactInfo.query.filter_by(email=data['email']).first()
    if not contact or not check_password_hash(contact.password, data['password']):
        return jsonify({"message": "Invalid email or password!"}), 401
    return jsonify({"message": "Login successful!", "user": {
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "phone_no": contact.phone_no
    }}), 200

@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(
        name=data['name'],
        description=data.get('description'),
        date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'),
        location=data['location']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'}), 201

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d %H:%M:%S'),
        'location': event.location
    } for event in events]), 200

@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify({
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d %H:%M:%S'),
        'location': event.location
    }), 200

@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.get_json()
    event = Event.query.get_or_404(id)
    event.name = data['name']
    event.description = data.get('description', event.description)
    event.date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
    event.location = data['location']
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'}), 200

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'}), 200

# Helper function to get or create contact info
def get_or_create_contact_info(data):
    contact = ContactInfo.query.filter_by(email=data['email']).first()
    if not contact:
        contact = ContactInfo(name=data['name'], email=data['email'], phone_no=data['phone_no'],password=data['password'])
        db.session.add(contact)
        db.session.commit()
    return contact

@app.route('/students', methods=['GET', 'POST'])
def handle_students():
    if request.method == 'POST':
        data = request.json
        contact = get_or_create_contact_info(data)
        student = Student(contact_id=contact.id)
        db.session.add(student)
        db.session.commit()
        return jsonify({"id": student.id, "name": contact.name, "email": contact.email, "phone_no": contact.phone_no}), 201
    elif request.method == 'GET':
        students = Student.query.all()
        return jsonify([
            {
                "id": student.id,
                "name": student.contact_info.name,
                "email": student.contact_info.email,
                "phone_no": student.contact_info.phone_no
            }
            for student in students
        ])

@app.route('/staff', methods=['GET', 'POST'])
def handle_staff():
    if request.method == 'POST':
        data = request.json
        contact = get_or_create_contact_info(data)
        staff = Staff(contact_id=contact.id)
        db.session.add(staff)
        db.session.commit()
        return jsonify({"id": staff.id, "name": contact.name, "email": contact.email, "phone_no": contact.phone_no}), 201
    elif request.method == 'GET':
        staff_members = Staff.query.all()
        return jsonify([
            {
                "id": staff.id,
                "name": staff.contact_info.name,
                "email": staff.contact_info.email,
                "phone_no": staff.contact_info.phone_no
            }
            for staff in staff_members
        ])

@app.route('/event-managers', methods=['GET', 'POST'])
def handle_event_managers():
    if request.method == 'POST':
        data = request.json
        contact = get_or_create_contact_info(data)
        event_manager = EventManager(contact_id=contact.id)
        db.session.add(event_manager)
        db.session.commit()
        return jsonify({"id": event_manager.id, "name": contact.name, "email": contact.email, "phone_no": contact.phone_no}), 201
    elif request.method == 'GET':
        event_managers = EventManager.query.all()
        return jsonify([
            {
                "id": event_manager.id,
                "name": event_manager.contact_info.name,
                "email": event_manager.contact_info.email,
                "phone_no": event_manager.contact_info.phone_no
            }
            for event_manager in event_managers
        ])

@app.route('/contact/<int:id>', methods=['GET'])
def get_contact_details(id):
    contact = ContactInfo.query.get_or_404(id)
    return jsonify({
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "phone_no": contact.phone_no
    })



if __name__ == '__main__':
    app.run(debug=True)
