import email
from flask_cors import CORS
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import Staff, Trekker, Trek, Booking, Admin, TrekStaff, db
from datetime import date, datetime


today = date.today()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'abc123xyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app, supports_credentials=True)

@app.route('/api/home')
def home():
    return "Welcome to the Home Page!"

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    role = data.get("role", "")
    if not username or not password or not role:
        return jsonify({"success": False, "message": "All fields are required."}), 400
    if role == "Admin":
        user = Admin.query.filter_by(username=username).first()
    elif role == "Staff":
        user = Staff.query.filter_by(username=username).first()
    elif role == "Trekker":
        user = Trekker.query.filter_by(username=username).first()
    else:
        return jsonify({"success": False, "message": "Invalid role."}), 400
    if not user:
        return jsonify({"success": False, "message": "No user."}), 401
    if not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "Invalid username or password."}), 401
    if user.status != "Active":
        return jsonify({"success": False, "message": "Your account has been blacklisted. Please contact the administrator."}), 403
    token = create_access_token(identity=str(user.id))
    return jsonify({"success": True, "message": "Login successful.", "role": role, "token": token}), 200

@app.route("/api/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    user_id = int(get_jwt_identity())
    admin = Admin.query.filter_by(id=user_id).first()
    total_treks = Trek.query.count()
    total_staffs = Staff.query.count()
    total_trekkers = Trekker.query.count()
    total_bookings = Booking.query.count()
    bookings = db.session.query(Booking.id.label("id"), Booking.booking_date.label("booking_date"), Booking.status.label("status"), Booking.payment_status.label("payment_status"), Trek.name.label("trek"), Trek.start_date.label("start_date"), Trek.end_date.label("end_date"), Trekker.name.label("trekker")).join(Trek, Trek.id == Booking.trek_id).join(Trekker, Trekker.id == Booking.trekker_id).all()
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404
    return jsonify({
        "success": True,
        "user": {"id": admin.id, "username": admin.username, "email": admin.email},
        "total_treks": total_treks,
        "total_staffs": total_staffs,
        "total_trekkers": total_trekkers,
        "total_bookings": total_bookings,
        "bookings": [{"id": booking.id, "trekker": booking.trekker, "trek": booking.trek, "booking_date": booking.booking_date.strftime("%d-%m-%Y"), "payment_status": booking.payment_status, "status": booking.status} for booking in bookings]
    }), 200

@app.route("/api/admin/treks", methods=["GET", "POST"])
@jwt_required()
def get_treks():
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404
    if request.method == "GET":
        treks = Trek.query.all()
        for trek in treks:
            trek.assigned_staffs = [assignment.staff_id for assignment in TrekStaff.query.filter_by(trek_id=trek.id).all()]
        return jsonify({
            "success": True,
            "user": {"id": admin.id, "username": admin.username, "email": admin.email},
            "treks": [{"id": trek.id, "name": trek.name, "location": trek.location, "start_date": trek.start_date.strftime("%Y-%m-%d"), "end_date": trek.end_date.strftime("%Y-%m-%d"), "difficulty_level": trek.difficulty_level, "price": trek.price, "description": trek.description, "photo": trek.photo, "status": trek.status, "available_slots": trek.available_slots, "assigned_staffs": trek.assigned_staffs} for trek in treks]
        }), 200
    elif request.method == "POST":
        data = request.get_json()
        name = data.get("name", "").strip()
        location = data.get("location", "").strip()
        start_date_str = data.get("start_date", "").strip()
        end_date_str = data.get("end_date", "").strip()
        difficulty_level = data.get("difficulty", "").strip()
        price = data.get("price")
        description = data.get("description", "").strip()
        photo = data.get("photo", "").strip()
        status = data.get("status", "Active").strip()
        available_slots = data.get("availableSlots")
        if not name or not location or not start_date_str or not end_date_str or not difficulty_level or price is None or available_slots is None:
            return jsonify({"success": False, "message": "All fields are required."}), 400
        new_trek = Trek(name=name, location=location, start_date=datetime.strptime(start_date_str, "%Y-%m-%d").date(), end_date=datetime.strptime(end_date_str, "%Y-%m-%d").date(), difficulty_level=difficulty_level, price=price, description=description, photo=photo, status=status, available_slots=available_slots)
        db.session.add(new_trek)
        db.session.commit()
        return jsonify({"success": True, "message": "Trek created successfully."}), 201

@app.route("/api/admin/treks/<int:trek_id>/manage", methods=["POST"])
@jwt_required()
def manage_trek(trek_id):
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    trek = Trek.query.get(trek_id)
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404
    if not trek:
        return jsonify({"success": False, "message": "Trek not found."}), 404
    if request.method == "POST":
        data = request.get_json()
        trek.name = data.get("name", trek.name)
        trek.location = data.get("location", trek.location)
        trek.start_date = datetime.strptime(data.get("start_date", trek.start_date), "%Y-%m-%d").date()
        trek.end_date = datetime.strptime(data.get("end_date", trek.end_date), "%Y-%m-%d").date()
        trek.difficulty_level = data.get("difficulty", trek.difficulty_level)
        trek.price = data.get("price", trek.price)
        trek.description = data.get("description", trek.description)
        trek.photo = data.get("photo", trek.photo)
        trek.status = data.get("status", trek.status)
        trek.available_slots = data.get("availableSlots", trek.available_slots)
        TrekStaff.query.filter_by(trek_id=trek_id).delete()
        if trek.status != "Closed":
            assigned_staffs = data.get("assignedStaffs", [])
            new_assignments = [TrekStaff(trek_id=trek_id, staff_id=staff_id) for staff_id in assigned_staffs]
            db.session.add_all(new_assignments)
        db.session.commit()
        return jsonify({"success": True, "message": "Trek updated successfully."}), 200

@app.route("/api/admin/trekking-staff", methods=["GET", "POST"])
@jwt_required()
def manage_trekking_staff():
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    if request.method == "GET":
        staffs = Staff.query.all()
        return jsonify({
            "success": True,
            "user": {"id": admin.id, "username": admin.username, "email": admin.email},
            "staffs": [{"id": staff.id, "name": staff.name, "email": staff.email, "contact": staff.contact, "experience": staff.experience, "specialization": staff.specialization, "status": staff.status} for staff in staffs]
        }), 200
    elif request.method == "POST":
        data = request.get_json()
        name = data.get("name", "").strip()
        username = data.get("username", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        contact = data.get("contact", "").strip()
        experience = data.get("experience", "").strip()
        specialization = data.get("specialization", "").strip()
        if not name or not username or not email or not password or not contact:
            return jsonify({"success": False, "message": "All fields are required."}), 400
        existing_username = Staff.query.filter_by(username=username).first()
        if existing_username:
            return jsonify({"success": False, "message": "This username is already taken."}), 400
        existing_staff = Staff.query.filter_by(email=email).first()
        if existing_staff:
            return jsonify({"success": False, "message": "Staff with this email already exists."}), 400
        password_hash = generate_password_hash(password)
        new_staff = Staff(name=name, username=username, email=email, password=password_hash, contact=contact, experience=experience, specialization=specialization)
        db.session.add(new_staff)
        db.session.commit()
        return jsonify({"success": True, "message": "Staff added successfully."}), 201

@app.route("/api/admin/trekking-staff/<int:staff_id>/status", methods=["PUT"])
@jwt_required()
def update_staff_status(staff_id):
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    staff = Staff.query.get(staff_id)
    data = request.get_json() if request.method == "PUT" else None
    status = data.get("status") if data else None
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404
    if not staff:
        return jsonify({"success": False, "message": "Staff not found."}), 404
    if request.method == "PUT":
        if status not in ["Active", "Blacklisted"]:
            return jsonify({"success": False, "message": "Invalid status."}), 400
        staff.status = status
        db.session.commit()
        return jsonify({"success": True, "message": f"Staff status updated to {staff.status}."}), 200

@app.route("/api/admin/trekkers", methods=["GET"])
@jwt_required()
def get_trekkers():
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404

    trekkers = Trekker.query.all()
    return jsonify({
        "success": True,
        "user": {"id": admin.id, "username": admin.username, "email": admin.email},
        "trekkers": [{"id": trekker.id, "name": trekker.name, "email": trekker.email, "contact": trekker.contact, "status": trekker.status} for trekker in trekkers]
    }), 200

@app.route("/api/admin/trekkers/<int:trekker_id>/status", methods=["PUT"])
@jwt_required()
def update_trekker_status(trekker_id):
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    trekker = Trekker.query.get(trekker_id)
    data = request.get_json() if request.method == "PUT" else None
    status = data.get("status") if data else None
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404
    if not trekker:
        return jsonify({"success": False, "message": "Trekker not found."}), 404
    if request.method == "PUT":
        if status not in ["Active", "Blacklisted"]:
            return jsonify({"success": False, "message": "Invalid status."}), 400
        trekker.status = status
        db.session.commit()
        return jsonify({"success": True, "message": f"Trekker status updated to {trekker.status}."}), 200

@app.route("/api/admin/bookings", methods=["GET"])
@jwt_required()
def get_bookings():
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404
    bookings = db.session.query(Booking.id.label("id"), Trekker.name.label("trekker_name"), Trek.name.label("trek_name"), Booking.booking_date, Booking.payment_status, Booking.status).join(Trekker, Booking.trekker_id == Trekker.id).join(Trek, Booking.trek_id == Trek.id).all()
    return jsonify({
        "success": True,
        "user": {"id": admin.id, "username": admin.username},
        "bookings": [{"id": booking.id, "trekker_name": booking.trekker_name, "trek_name": booking.trek_name, "booking_date": booking.booking_date.strftime("%d-%m-%Y"), "payment_status": booking.payment_status, "status": booking.status} for booking in bookings]
    }), 200

@app.route("/api/admin/bookings/<int:booking_id>/manage", methods=["POST"])
@jwt_required()
def manage_booking(booking_id):
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    booking = Booking.query.get(booking_id)
    trek_id = booking.trek_id
    trek = Trek.query.get(trek_id)
    prev_status = booking.status
    data = request.get_json() if request.method == "POST" else None
    status = data.get("status") if data else None
    payment_status = data.get("payment_status") if data else None
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404
    if not booking:
        return jsonify({"success": False, "message": "Booking not found."}), 404
    if request.method == "POST":
        if status not in ["Pending", "Confirmed", "Cancelled"]:
            return jsonify({"success": False, "message": "Invalid status."}), 400
        if prev_status in ["Pending", "Confirmed"] and status == "Cancelled":
            trek.available_slots += 1
        elif prev_status == "Cancelled" and status in ["Pending", "Confirmed"]:
            trek.available_slots -= 1
        booking.status = status if status else booking.status
        booking.payment_status = payment_status if payment_status else booking.payment_status
        db.session.commit()
        return jsonify({"success": True, "message": f"Booking status updated to {booking.status}."}), 200

@app.route("/api/staff/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():
    user_id = int(get_jwt_identity())
    staff = Staff.query.get(user_id)
    if not staff:
        return jsonify({"success": False, "message": "Staff not found."}), 404
    treks = db.session.query(Trek.id.label("id"), Trek.name.label("name"), Trek.location.label("location"), Trek.start_date.label("start_date"), Trek.end_date.label("end_date"), Trek.status.label("status"), Trek.available_slots.label("slots"), db.func.count(db.case((Booking.status.in_(["Confirmed", "Pending"]), Booking.id), else_=None)).label("participants")).select_from(TrekStaff).join(Trek, TrekStaff.trek_id == Trek.id).filter(TrekStaff.staff_id == staff.id).outerjoin(Booking, Booking.trek_id == Trek.id).group_by(TrekStaff.id, Trek.id).all()
    assigned_treks = len(treks)
    total_participants = sum(trek.participants for trek in treks)
    ongoing_treks = sum(1 for trek in treks if trek.start_date <= today and trek.end_date >= today and trek.status == "Open")
    return jsonify({
        "success": True,
        "user": {"id": staff.id, "name": staff.name},
        "assigned_treks": assigned_treks,
        "total_participants": total_participants,
        "ongoing_treks": ongoing_treks,
        "treks": [{"id": trek.id, "name": trek.name, "location": trek.location, "start_date": trek.start_date.strftime("%Y-%m-%d") if trek.start_date else None, "end_date": trek.end_date.strftime("%Y-%m-%d") if trek.end_date else None, "participants": trek.participants, "slots": trek.slots + trek.participants, "status": trek.status} for trek in treks]}), 200

@app.route("/api/staff/treks", methods=["GET"])
@jwt_required()
def staff_treks():
    user_id = int(get_jwt_identity())
    staff = Staff.query.get(user_id)
    if not staff:
        return jsonify({"success": False, "message": "Staff not found."}), 404
    treks = db.session.query(Trek.id.label("id"), Trek.name.label("name"), Trek.location.label("location"), Trek.start_date.label("start_date"), Trek.end_date.label("end_date"), Trek.status.label("status"), Trek.available_slots.label("slots"), Trek.photo.label("photo"), Trek.price.label("price"), Trek.description.label("description"), Trek.difficulty_level.label("difficulty"), db.func.count(db.case((Booking.status.in_(["Confirmed", "Pending"]), Booking.id), else_=None)).label("participants")).select_from(TrekStaff).join(Trek, TrekStaff.trek_id == Trek.id).filter(TrekStaff.staff_id == staff.id).outerjoin(Booking, Booking.trek_id == Trek.id).group_by(TrekStaff.id, Trek.id).all()
    return jsonify({
        "success": True,
        "user": {"id": staff.id, "name": staff.name},
        "treks": [{"id": trek.id, "name": trek.name, "location": trek.location, "start_date": trek.start_date.strftime("%Y-%m-%d") if trek.start_date else None, "end_date": trek.end_date.strftime("%Y-%m-%d") if trek.end_date else None, "participants": trek.participants, "available_slots": trek.slots, "status": trek.status, "photo": trek.photo, "price": trek.price, "description": trek.description, "difficulty": trek.difficulty} for trek in treks]
    }), 200

@app.route("/api/staff/treks/<int:trek_id>/manage", methods=["POST"])
@jwt_required()
def manage_staff_trek(trek_id):
    user_id = int(get_jwt_identity())
    staff = Staff.query.get(user_id)
    trek = Trek.query.get(trek_id)
    if not staff:
        return jsonify({"success": False, "message": "Staff not found."}), 404
    if not trek:
        return jsonify({"success": False, "message": "Trek not found."}), 404
    if request.method == "POST":
        data = request.get_json()
        trek.end_date = data.get("end_date", trek.end_date)
        trek.status = data.get("status", trek.status)
        trek.available_slots = data.get("availableSlots", trek.available_slots)
        db.session.commit()
        return jsonify({"success": True, "message": "Trek updated successfully."}), 200

@app.route("/api/staff/participants", methods=["GET", "POST"])
@jwt_required()
def manage_participants():
    user_id = int(get_jwt_identity())
    staff = Staff.query.get(user_id)
    if not staff:
        return jsonify({"success": False, "message": "Staff not found."}), 404
    if request.method == "GET":
        treks = db.session.query(Trek.id.label("id"), Trek.name.label("name"), Trek.start_date.label("start_date"), Trek.end_date.label("end_date")).select_from(TrekStaff).join(Trek, TrekStaff.trek_id == Trek.id).filter(TrekStaff.staff_id == staff.id).all()
        return jsonify({
            "success": True,
            "user": {"id": staff.id, "name": staff.name},
            "treks": [{"id": trek.id, "name": trek.name, "start_date": trek.start_date.strftime("%d-%m-%Y"), "end_date": trek.end_date.strftime("%d-%m-%Y")} for trek in treks]
        }), 200
    if request.method == "POST":
        data = request.get_json()
        trek_id = data.get("assignedTrek") if data else None
        if not trek_id:
            return jsonify({"success": False, "message": "Trek ID is required."}), 400
        trek = Trek.query.get(trek_id)
        if not trek:
            return jsonify({"success": False, "message": "Trek not found."}), 404
        participants = db.session.query(Trekker.name.label("name"), Trekker.email.label("email"), Trekker.contact.label("contact"), Booking.id.label("id"), Booking.booking_date.label("booking_date"), Booking.payment_status.label("payment_status"), Booking.status.label("status")).join(Booking, Booking.trekker_id == Trekker.id).filter(Booking.trek_id == trek_id).all()
        return jsonify({
            "success": True, 
            "user": {"id": staff.id, "name": staff.name},
            "participants": [{"id": participant.id, "name": participant.name, "email": participant.email, "contact": participant.contact, "booking_date": participant.booking_date.strftime("%d-%m-%Y") if participant.booking_date else None, "payment_status": participant.payment_status, "status": participant.status} for participant in participants]
        }), 200

@app.route("/api/staff/participants/<int:participant_id>/manage", methods=["POST"])
@jwt_required()
def update_participant(participant_id):
    user_id = int(get_jwt_identity())
    staff = Staff.query.get(user_id)
    booking = Booking.query.get(participant_id)
    trek_id = booking.trek_id
    trek = Trek.query.get(trek_id)
    prev_status = booking.status
    data = request.get_json() if request.method == "POST" else None
    status = data.get("status") if data else None
    payment_status = data.get("payment_status") if data else None
    if not staff:
        return jsonify({"success": False, "message": "Staff not found."}), 404
    if not booking:
        return jsonify({"success": False, "message": "Participant not found."}), 404
    if request.method == "POST":
        if status not in ["Pending", "Confirmed", "Cancelled"]:
            return jsonify({"success": False, "message": "Invalid status."}), 400
        if prev_status in ["Pending", "Confirmed"] and status == "Cancelled":
            trek.available_slots += 1
        elif prev_status == "Cancelled" and status in ["Pending", "Confirmed"]:
            trek.available_slots -= 1
        booking.status = status if status else booking.status
        booking.payment_status = payment_status if payment_status else booking.payment_status
        db.session.commit()
        return jsonify({"success": True, "message": f"Booking status updated to {booking.status}."}), 200

@app.route("/api/staff/profile", methods=["GET", "PUT"])
@jwt_required()
def staff_profile():
    user_id = int(get_jwt_identity())
    staff = Staff.query.get(user_id)
    if not staff:
        return jsonify({"success": False, "message": "Staff not found."}), 404
    if request.method == "PUT":
        data = request.get_json()
        staff.contact = data.get("contact", staff.contact)
        staff.experience = data.get("experience", staff.experience)
        staff.specialization = data.get("specialization", staff.specialization)
        db.session.commit()
    return jsonify({
        "success": True,
        "user": { "id": staff.id, "name": staff.name, "username": staff.username, "email": staff.email, "contact": staff.contact, "experience": staff.experience, "specialization": staff.specialization, "status": staff.status}
    }), 200

@app.route("/api/trekker/registration", methods=["POST"])
def trekker_registration():
    data = request.get_json()
    name = data.get("name", "").strip()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    confirmPassword = data.get("confirmPassword", "")
    contact = data.get("contact", "").strip()
    if not name or not username or not email or not password or not confirmPassword or not contact:
        return jsonify({"success": False, "message": "All fields are required."}), 400
    if password != confirmPassword:
        return jsonify({"success": False, "message": "Passwords do not match."}), 400
    existing_username = Trekker.query.filter_by(username=username).first()
    if existing_username:
        return jsonify({"success": False, "message": "This username is already taken."}), 400
    existing_trekker = Trekker.query.filter_by(email=email).first()
    if existing_trekker:
        return jsonify({"success": False, "message": "Trekker with this email already exists."}), 400
    password_hash = generate_password_hash(password)
    new_trekker = Trekker(name=name, username=username, email=email, password=password_hash, contact=contact)
    db.session.add(new_trekker)
    db.session.commit()
    return jsonify({"success": True, "message": "Trekker registered successfully."}), 200

@app.route("/api/trekker/dashboard", methods=["GET"])
@jwt_required()
def trekker_dashboard():
    user_id = int(get_jwt_identity())
    trekker = Trekker.query.get(user_id)
    treks = Trek.query.filter(Trek.status.in_(["Open", "Upcoming"]), Trek.start_date > today).order_by(Trek.id.desc()).limit(4).all()
    bookings = db.session.query(Booking.id.label("id"), Booking.booking_date.label("booking_date"), Booking.status.label("status"), Booking.payment_status.label("payment_status"), Trek.name.label("trek_name"), Trek.start_date.label("start_date"), Trek.end_date.label("end_date")).join(Trek, Trek.id == Booking.trek_id).filter(Booking.trekker_id == user_id).limit(3).all()
    if not trekker:
        return jsonify({"success": False, "message": "Trekker not found."}), 404
    return jsonify({"success": True, 
        "user": {"id": trekker.id, "name": trekker.name, "email": trekker.email, "contact": trekker.contact},
        "treks": [{"id": trek.id, "name": trek.name, "photo": trek.photo, "location": trek.location, "start_date": trek.start_date.strftime("%d-%m-%Y"), "end_date": trek.end_date.strftime("%d-%m-%Y"), "difficulty_level": trek.difficulty_level, "price": trek.price, "available_slots": trek.available_slots} for trek in treks],
        "bookings": [{"id": booking.id, "booking_date": booking.booking_date.strftime("%d-%m-%Y"), "trek_name": booking.trek_name, "trek_dates": booking.start_date.strftime("%d-%m-%Y") + " to " + booking.end_date.strftime("%d-%m-%Y"), "status": booking.status, "payment_status": booking.payment_status} for booking in bookings]
    }), 200

@app.route("/api/trekker/browse-treks", methods=['GET', 'POST'])
@jwt_required()
def trekker_browse():
    user_id = int(get_jwt_identity())
    trekker = Trekker.query.get(user_id)
    treks = Trek.query.filter(Trek.status.in_(["Open", "Upcoming"]), Trek.start_date > today).all()
    if request.method == 'GET':
        return jsonify({"success": True,
            "user": {"id": trekker.id, "name": trekker.name, "email": trekker.email, "contact": trekker.contact},
            "treks": [{"id": trek.id, "name": trek.name, "photo": trek.photo, "location": trek.location, "start_date": trek.start_date.strftime("%d-%m-%Y"), "end_date": trek.end_date.strftime("%d-%m-%Y"), "difficulty_level": trek.difficulty_level, "price": trek.price, "available_slots": trek.available_slots, "status": trek.status} for trek in treks]
        })
    elif request.method == 'POST':
        data = request.get_json()
        trek_id = data.get("trek_id", "")
        payment_mode = data.get("payment_mode", "")
        if not trek_id:
            return jsonify({"success": False, "message": "Trek not found."}), 404
        if not payment_mode:
            return jsonify({"success": False, "message": "Invalid payment mode"}), 404
        existing_booking = Booking.query.filter(Booking.trek_id == trek_id, Booking.trekker_id == user_id).first()
        if existing_booking:
            return jsonify({"success": False, "message": f"You have aldready booked this trek on{ existing_booking.booking_date.strftime('%d-%m-%Y') }."}), 409
        trek = Trek.query.filter_by(id=trek_id).first()
        slots = trek.available_slots - 1
        trek.available_slots = slots
        new_booking = Booking(trek_id=trek_id, trekker_id=user_id, payment_mode=payment_mode)
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"success": True, "message": "Booking registered successfully."}), 200

@app.route("/api/trekker/bookings", methods=['GET'])
@jwt_required()
def trekker_bookings():
    user_id = int(get_jwt_identity())
    trekker = Trekker.query.get(user_id)
    if request.method == 'GET':
        bookings = db.session.query(Booking.id.label("id"), Booking.booking_date.label("booking_date"), Booking.status.label("status"), Booking.payment_status.label("payment_status"), Trek.name.label("trek_name"), Trek.start_date.label("start_date"), Trek.end_date.label("end_date")).join(Trek, Trek.id == Booking.trek_id).filter(Booking.trekker_id == user_id).all()
        return jsonify({"success": True, 
            "user": {"id": trekker.id, "name": trekker.name, "email": trekker.email, "contact": trekker.contact},
            "bookings": [{"id": booking.id, "booking_date": booking.booking_date.strftime("%d-%m-%Y"), "trek_name": booking.trek_name, "trek_dates": booking.start_date.strftime("%d-%m-%Y") + " to " + booking.end_date.strftime("%d-%m-%Y"), "status": booking.status, "payment_status": booking.payment_status} for booking in bookings]
        }), 200

@app.route("/api/trekker/history", methods=['GET'])
@jwt_required()
def trekker_history():
    user_id = int(get_jwt_identity())
    trekker = Trekker.query.get(user_id)
    if request.method == 'GET':
        bookings = db.session.query(Booking.id.label("id"), Booking.booking_date.label("booking_date"), Booking.status.label("status"), Booking.payment_status.label("payment_status"), Trek.name.label("trek_name"), Trek.start_date.label("start_date"), Trek.end_date.label("end_date")).join(Trek, Trek.id == Booking.trek_id).filter(Booking.trekker_id == user_id, Trek.end_date < today).all()
        return jsonify({"success": True, 
            "user": {"id": trekker.id, "name": trekker.name, "email": trekker.email, "contact": trekker.contact},
            "bookings": [{"id": booking.id, "booking_date": booking.booking_date.strftime("%d-%m-%Y"), "trek_name": booking.trek_name, "trek_dates": booking.start_date.strftime("%d-%m-%Y") + " to " + booking.end_date.strftime("%d-%m-%Y"), "status": booking.status, "payment_status": booking.payment_status} for booking in bookings]
        }), 200

@app.route("/api/trekker/profile", methods=["GET", "PUT"])
@jwt_required()
def trekker_profile():
    user_id = int(get_jwt_identity())
    trekker = Trekker.query.get(user_id)
    if not trekker:
        return jsonify({"success": False, "message": "Trekker not found."}), 404
    if request.method == "PUT":
        data = request.get_json()
        username = data.get("username")
        if username != trekker.username and Trekker.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "This username aldready exists."})
        trekker.username = username
        trekker.name = data.get("name", trekker.name)
        trekker.email = data.get("email", trekker.email)
        trekker.contact = data.get("contact", trekker.contact)
        trekker.password = data.get("password", trekker.password)
        db.session.commit()
    return jsonify({
        "success": True,
        "user": { "id": trekker.id, "name": trekker.name, "username": trekker.username, "email": trekker.email, "contact": trekker.contact, "status": trekker.status}
    }), 200

with app.app_context():
    db.create_all()
    admin = Admin.query.filter_by(username="Admin1").first()
    if admin is None:
        password_hash = generate_password_hash("1234")
        admin = Admin(username="Admin1", password=password_hash, email="admin@employex.com")
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)