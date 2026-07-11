from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__,template_folder='/Users/RDS/Desktop/TrekkingManagementApplication_24f2003258/templates')
app.secret_key = "trek_secret_key"

DATABASE = "database.db"


# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return render_template("1_home.html")


# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/login")
def login():
    return render_template("2_login.html")


# -----------------------------
# USER LOGIN
# -----------------------------
@app.route("/user_login", methods=["GET", "POST"])
def user_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:
            session["user"] = user["name"]
            return redirect(url_for("user_dashboard"))

    return render_template("2.1_login.html")


# -----------------------------
# STAFF LOGIN
# -----------------------------
@app.route("/staff_login", methods=["GET", "POST"])
def staff_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        staff = conn.execute(
            "SELECT * FROM staff WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if staff:
            session["staff"] = staff["name"]
            return redirect(url_for("staff_dashboard"))

    return render_template("2.2_login_staff.html")


# -----------------------------
# ADMIN LOGIN
# -----------------------------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if email == "admin@gmail.com" and password == "admin123":
            session["admin"] = "Admin"
            return redirect(url_for("admin_dashboard"))

    return render_template("2.3_login_admin.html")


# -----------------------------
# REGISTER
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        conn.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("user_login"))

    return render_template("3_register.html")


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("4_admin_dashboard.html")


# -----------------------------
# STAFF DASHBOARD
# -----------------------------
@app.route("/staff_dashboard")
def staff_dashboard():
    return render_template("4.1_staff_dashboard.html")


# -----------------------------
# USER DASHBOARD
# -----------------------------
@app.route("/user_dashboard")
def user_dashboard():
    return render_template("4.2_user_dashboard.html")


# -----------------------------
# ADD TREK
# -----------------------------
@app.route("/add_trek", methods=["GET", "POST"])
def add_trek():

    if request.method == "POST":

        name = request.form["name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        duration = request.form["duration"]
        slots = request.form["slots"]

        conn = get_db()

        conn.execute("""
            INSERT INTO treks
            (name,location,difficulty,duration,slots)
            VALUES(?,?,?,?,?)
        """, (name, location, difficulty, duration, slots))

        conn.commit()
        conn.close()

        return redirect(url_for("manage_treks"))

    return render_template("5_add_trek.html")


# -----------------------------
# MANAGE TREKS
# -----------------------------
@app.route("/manage_treks")
def manage_treks():

    conn = get_db()

    treks = conn.execute("SELECT * FROM treks").fetchall()

    conn.close()

    return render_template("6_manage_treks.html", treks=treks)


# -----------------------------
# MANAGE STAFF
# -----------------------------
@app.route("/manage_staff")
def manage_staff():

    conn = get_db()

    staff = conn.execute("SELECT * FROM staff").fetchall()

    conn.close()

    return render_template("7_manage_staff.html", staff=staff)


# -----------------------------
# MANAGE USERS
# -----------------------------
@app.route("/manage_users")
def manage_users():

    conn = get_db()

    users = conn.execute("SELECT * FROM users").fetchall()

    conn.close()

    return render_template("8_manage_users.html", users=users)


# -----------------------------
# ASSIGN STAFF
# -----------------------------
@app.route("/assign_staff", methods=["GET", "POST"])
def assign_staff():

    conn = get_db()

    if request.method == "POST":

        trek = request.form["trek"]
        staff = request.form["staff"]

        conn.execute(
            "INSERT INTO assignments(trek_id,staff_id) VALUES(?,?)",
            (trek, staff)
        )

        conn.commit()

    treks = conn.execute("SELECT * FROM treks").fetchall()
    staffs = conn.execute("SELECT * FROM staff").fetchall()

    conn.close()

    return render_template(
        "9_assign_staff.html",
        treks=treks,
        staffs=staffs
    )


# -----------------------------
# ASSIGNED TREKS
# -----------------------------
@app.route("/assigned_treks")
def assigned_treks():

    conn = get_db()

    data = conn.execute("""
    SELECT treks.name,
           treks.location,
           staff.name as staff_name
    FROM assignments
    JOIN treks
    ON assignments.trek_id = treks.id
    JOIN staff
    ON assignments.staff_id = staff.id
    """).fetchall()

    conn.close()

    return render_template("11_assigned_treks.html", data=data)


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)