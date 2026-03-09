import re
from datetime import datetime
users = {}
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
password_pattern = r"^(?=.*[A-Z])(?=.*\d).{8,}$"
name = input("Enter Name: ")
email = input("Enter Email: ")
password = input("Enter Password: ")
dob = input("Enter Date of Birth (YYYY-MM-DD): ")
if not re.match(email_pattern, email):
    print("Invalid Email Format")
    exit()

if not re.match(password_pattern, password):
    print("Password must contain at least 8 characters, 1 uppercase letter, and 1 digit")
    exit()

dob_date = datetime.strptime(dob, "%Y-%m-%d")

today = datetime.today()
age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))


users[email] = {
    "name": name,
    "password": password,
    "dob": dob,
    "age": age
}

print("\nRegistered Users:")
for email, details in users.items():
    print(f"Email: {email}")
    print(f"Name: {details['name']}")
    print(f"Password: {details['password']}")
    print(f"DOB: {details['dob']}")
    print(f"Age: {details['age']}")
    print("----------------------")
