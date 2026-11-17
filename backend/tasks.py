from celery_worker import celery
from app import app
from models import db, Trekker, Staff, Booking, Trek
import csv
import os
from datetime import datetime, timedelta
import csv
import io
from flask_mail import Message
from app import app, mail


@celery.task
def daily_reminder_email():
    with app.app_context():
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        applications = db.session.query(Booking, Trekker, Trek).join(Trekker, Trekker.id == Booking.trekker_id).join(Trek, Trek.id == Booking.trek_id).filter(Trek.start_date == tomorrow, Booking.status == "Confirmed").all()
        print("Tomorrow:", tomorrow)
        print("Matching bookings:", len(applications))
        for booking, trekker, trek in applications:
            msg = Message(
            subject="Reminder: Your Trek is Tomorrow!",
            recipients=[trekker.email],
            body=f"""
Hello {trekker.name},

This is a reminder that your trek "{trek.name}" is scheduled for tomorrow.

Trek Details:
Booking ID: {booking.id}
Trek Name: {trek.name}
Location: {trek.location}
Start Date: {trek.start_date.strftime("%d-%m-%Y")}
End Date: {trek.end_date.strftime("%d-%m-%Y")}

Please make sure you are prepared and arrive on time.

Thank you for choosing Treknologia!

Regards,
Team Treknologia
                """
            )
            mail.send(msg)
        return "Daily reminders completed."
    
def generate_monthly_report():
    popular_treks = db.session.query(Trek.id, Trek.name, db.func.count(Booking.id).label("total_bookings")).join(Booking, Booking.trek_id == Trek.id).group_by(Trek.id).order_by(db.func.count(Booking.id).desc()).limit(5).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Treks", Trek.query.count()])
    writer.writerow(["Total Bookings", Booking.query.count()])
    writer.writerow(["Popular treks", [trek.name for trek in popular_treks]])
    output.seek(0)
    return output

@celery.task
def monthly_report():
    with app.app_context():
        csv_file = generate_monthly_report()
        msg = Message(subject="Treknologia - Monthly Report", recipients=["25f1002209@ds.study.iitm.ac.in"])
        msg.body = "Please find the monthly placement report attached."
        msg.attach("Monthly_Report.csv", "text/csv", csv_file.getvalue().encode("utf-8"))
        mail.send(msg)
        return "Monthly report emailed."

@celery.task
def export_history(trekker_id):
    with app.app_context():
        trekker = Trekker.query.get(trekker_id)
        bookings = db.session.query(Booking, Trek, Trekker).join(Trek, Trek.id == Booking.trek_id).join(Trekker, Trekker.id == Booking.trekker_id).filter(Booking.trekker_id == trekker_id).all()
        os.makedirs("exports", exist_ok=True)
        filename = f"exports/trekker_{trekker_id}.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Booking ID", "Trek Name", "Booking Date", "Trek Dates", "Payment Status"])
            for booking, trek, trekker in bookings:
                writer.writerow([booking.id, trek.name, booking.booking_date.strftime("%d-%m-%Y"), trek.start_date.strftime("%d-%m-%Y") + " to " + trek.end_date.strftime("%d-%m-%Y"), booking.payment_status])
        msg = Message(subject="Treknologia - Trek History", recipients=[trekker.email])
        msg.body = (
            f"Hello {trekker.name},\n\n"
            "Your trek history report is attached.\n\n"
            "Regards,\n"
            "Treknologia"
        )
        with open(filename, "rb") as file:
            msg.attach(os.path.basename(filename), "text/csv", file.read())
        mail.send(msg)
        print(f"{filename} generated and emailed.")
        return filename