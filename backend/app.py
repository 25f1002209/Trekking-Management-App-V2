from flask import Flask
from models import Staff, Trekker, Trek, Booking, Admin, db
from datetime import date, datetime

today = date.today()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123xyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.create_all()
    admin = Admin.query.filter_by(username="Admin1").first()
    if admin is None:
        admin = Admin(username="Admin1", password="1234", email="admin@employex.com")
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)