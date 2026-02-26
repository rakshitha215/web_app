from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="hospital_db"
)

cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return render_template("index.html")

# Add Patient
@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]

        cursor.execute(
            "INSERT INTO Patient (Name, Age, Gender, Phone) VALUES (%s,%s,%s,%s)",
            (name, age, gender, phone)
        )
        db.commit()
        return redirect("/")
    return render_template("add_patient.html")

# Add Doctor
@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    cursor.execute("SELECT * FROM Department")
    departments = cursor.fetchall()

    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        dept_id = request.form["department"]

        cursor.execute(
            "INSERT INTO Doctor (Name, Specialization, DepartmentID) VALUES (%s,%s,%s)",
            (name, specialization, dept_id)
        )
        db.commit()
        return redirect("/")
    return render_template("add_doctor.html", departments=departments)

# Book Appointment
@app.route("/book", methods=["GET", "POST"])
def book():
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()

    cursor.execute("SELECT * FROM Doctor")
    doctors = cursor.fetchall()

    if request.method == "POST":
        patient = request.form["patient"]
        doctor = request.form["doctor"]
        date = request.form["date"]

        cursor.execute(
            "INSERT INTO Appointment (AppointmentDate, PatientID, DoctorID) VALUES (%s,%s,%s)",
            (date, patient, doctor)
        )
        db.commit()
        return redirect("/appointments")

    return render_template("book_appointment.html", patients=patients, doctors=doctors)

# View Appointments
@app.route("/appointments")
def appointments():
    cursor.execute("""
        SELECT a.AppointmentID, a.AppointmentDate,
               p.Name AS PatientName,
               d.Name AS DoctorName
        FROM Appointment a
        JOIN Patient p ON a.PatientID = p.PatientID
        JOIN Doctor d ON a.DoctorID = d.DoctorID
        ORDER BY a.AppointmentDate DESC
    """)
    data = cursor.fetchall()
    return render_template("appointments.html", appointments=data)

if __name__ == "__main__":
    app.run(debug=True)