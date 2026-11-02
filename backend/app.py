import email
from flask_cors import CORS
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import Staff, Trekker, Trek, Booking, Admin, db
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
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role", "")
    if not email or not password or not role:
        return jsonify({"success": False, "message": "All fields are required."}), 400
    if role == "Admin":
        user = Admin.query.filter_by(email=email).first()
    elif role == "Staff":
        user = Staff.query.filter_by(email=email).first()
    elif role == "Trekker":
        user = Trekker.query.filter_by(email=email).first()
    else:
        return jsonify({"success": False, "message": "Invalid role."}), 400
    if not user:
        return jsonify({"success": False, "message": "No user."}), 401
    if not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "Invalid email or password."}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({"success": True, "message": "Login successful.", "role": role, "token": token}), 200

@app.route("/api/admin-dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    user_id = int(get_jwt_identity())
    admin = Admin.query.get(user_id)
    total_treks = Trek.query.count()
    total_staffs = Staff.query.count()
    total_trekkers = Trekker.query.count()
    total_bookings = Booking.query.count()
    bookings = Booking.query.all()
    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404
    return jsonify({
        "success": True,
        "user": {"id": admin.id, "username": admin.username, "email": admin.email},
        "total_treks": total_treks,
        "total_staffs": total_staffs,
        "total_trekkers": total_trekkers,
        "total_bookings": total_bookings,
        "bookings": [{"id": booking.id, "trekker_id": booking.trekker_id, "trek_id": booking.trek_id, "booking_date": booking.booking_date.strftime("%Y-%m-%d"), "payment_status": booking.payment_status, "status": booking.status} for booking in bookings]
    }), 200

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
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        contact = data.get("contact", "").strip()
        experience = data.get("experience", "").strip()
        specialization = data.get("specialization", "").strip()
        if not name or not email or not password or not contact:
            return jsonify({"success": False, "message": "All fields are required."}), 400
        existing_staff = Staff.query.filter_by(email=email).first()
        if existing_staff:
            return jsonify({"success": False, "message": "Staff with this email already exists."}), 400
        password_hash = generate_password_hash(password)
        new_staff = Staff(name=name, email=email, password=password_hash, contact=contact, experience=experience, specialization=specialization)
        db.session.add(new_staff)
        db.session.commit()
        return jsonify({"success": True, "message": "Staff added successfully."}), 201

@app.route("/api/staff-dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():
    user_id = int(get_jwt_identity())
    staff = Staff.query.get(user_id)
    if not staff:
        return jsonify({"success": False, "message": "Staff not found."}), 404
    return jsonify({"success": True, "user": {"id": staff.id, "name": staff.name, "email": staff.email, "contact": staff.contact, "experience": staff.experience, "specialization": staff.specialization, "status": staff.status}}), 200

@app.route("/api/trekker-registration", methods=["POST"])
def trekker_registration():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    confirmPassword = data.get("confirmPassword", "")
    contact = data.get("contact", "").strip()
    if not name or not email or not password or not confirmPassword or not contact:
        return jsonify({"success": False, "message": "All fields are required."}), 400
    if password != confirmPassword:
        return jsonify({"success": False, "message": "Passwords do not match."}), 400
    existing_trekker = Trekker.query.filter_by(email=email).first()
    if existing_trekker:
        return jsonify({"success": False, "message": "Trekker with this email already exists."}), 400
    password_hash = generate_password_hash(password)
    new_trekker = Trekker(name=name, email=email, password=password_hash, contact=contact)
    db.session.add(new_trekker)
    db.session.commit()
    return jsonify({"success": True, "message": "Trekker registered successfully."}), 200

@app.route("/api/trekker-dashboard", methods=["GET"])
@jwt_required()
def trekker_dashboard():
    user_id = int(get_jwt_identity())
    trekker = Trekker.query.get(user_id)
    if not trekker:
        return jsonify({"success": False, "message": "Trekker not found."}), 404
    return jsonify({"success": True, "user": {"id": trekker.id, "name": trekker.name, "email": trekker.email, "contact": trekker.contact}}), 200

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