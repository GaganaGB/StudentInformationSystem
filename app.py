from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "student-management-demo-key"

# Temporary storage
students = []
users = {}
next_id = 1


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Student Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not name or not email or not password:
            flash("All fields are required.")
            return redirect(url_for("register"))

        if email in users:
            flash("Email is already registered.")
            return redirect(url_for("register"))

        users[email] = {
            "name": name,
            "password": generate_password_hash(password)
        }

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


# Student Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = users.get(email)

        if user and check_password_hash(user["password"], password):
            session["email"] = email
            session["name"] = user["name"]
            return redirect(url_for("student_list"))

        flash("Invalid email or password.")

    return render_template("login.html")


# View and Add Student Information
@app.route("/students", methods=["GET", "POST"])
def student_list():
    global next_id

    if "email" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"].strip()
        course = request.form["course"].strip()
        email = request.form["email"].strip().lower()

        if name and course and email:
            students.append({
                "id": next_id,
                "name": name,
                "course": course,
                "email": email
            })

            next_id += 1
            flash("Student added successfully.")
            return redirect(url_for("student_list"))

        flash("Please fill in all student fields.")

    return render_template(
        "students.html",
        students=students,
        name=session.get("name")
    )


# Delete Student Information
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    if "email" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))

    students[:] = [
        student for student in students
        if student["id"] != student_id
    ]

    flash("Student deleted successfully.")
    return redirect(url_for("student_list"))


# Student Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("index"))


# Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)
