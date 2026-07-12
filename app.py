from flask import Flask , render_template ,redirect ,request 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "trek_secret_key"



# connecting to database 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"


db = SQLAlchemy(app)

    
# Creating Models 
class User(db.Model):
    __tablename__ ="users"
    user_id = db.Column(db.Integer , nullable = False , primary_key = True )
    name  = db.Column(db.String(50) , nullable = False)
    email = db.Column(db.String(50), nullable =False)
    password = db.Column (db.String(50), nullable = False)
    phone = db.Column (db.String(20),nullable = False )
    role = db.Column(db.String(10), nullable = False )
    status = db.Column(db.String(20),nullable =False )
    is_blacklisted = db.Column(db.Boolean , default = False )


class Trek(db.Model):
    __tablename__ = "treks"
    
    trek_id = db.Column(db.Integer, primary_key = True)
    trek_name = db.Column (db.String(50), nullable = False )
    location = db.Column(db.String(50), nullable = False )
    price = db.Column(db.Integer, nullable = False )
    duration = db.Column(db.String(30), nullable = False)
    difficulty = db.Column(db.String(10),nullable = False)
    total_seat = db.Column(db.Integer, nullable = False )
    available_seat = db.Column (db.Integer, nullable = False)
    status = db.Column (db.String , nullable = False , default = "open" )
    
    assigned_staff_id = db.Column(db.Integer,db.ForeignKey("users.user_id") )
    
    user = db.relationship("User", backref ="treks")


    
class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id  = db.Column(db.Integer , primary_key = True ) 
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id") , nullable = False)
    trek_id = db.Column(db.Integer,db.ForeignKey("treks.trek_id"), nullable = False)
    number_of_people = db.Column (db.Integer, nullable = False)
    booking_date = db.Column(db.Date , nullable = False)
    booking_status = db.Column(db.String(10), nullable = False)
    
    
    user_object = db.relationship("User", backref= "bookings")
    trek_object = db.relationship("Trek", backref = "bookings")


# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return render_template("1_home.html")

#register route 
@app.route("/register", methods =["GET","POST"])
def register():
    if request.method == "POST" :
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        role = request.form["role"]

        if role =="staff" :
            status = "pending"
        else :
            status ="approve"
            
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return "Email already registered!" 
    
        new_user = User(
            name = name ,
            email =  email ,
            phone = phone ,
            password = password , 
            role = role , 
            status = status ,
            is_blacklisted = False)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    
    return render_template("3_register.html")


# LOGIN PAGE
@app.route("/login/" ,methods =["GET","POST"] )
def login():
    if request.method == "POST" :
        email = request.form["email"]
        password = request.form["password"]

        selected_user = User.query.filter_by(email = email).first()
        
        if selected_user is not None :
            if selected_user.password == password :
                if(selected_user.role == "admin"):
                    return redirect("/admin_dashboard")
                elif(selected_user.role == "staff"):
                    return redirect("/staff_dashboard")
                else :
                    return redirect("/user_dashboard")
        
        
        
    return render_template("2.1_login.html")



@app.route("/staff_dashboard")
def staff_dashboard():
    return render_template("4.1_staff_dashboard.html")

@app.route("/user_dashboard")
def user_dashboard():
    return render_template("4.2_user_dashboard.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("4_admin_dashboard.html")


# Trek Creation 
@app.route("/add_trek", methods =["GET", "POST"])
def create_trek():
    if request.method == "POST" :
        trek_name = request.form["trek_name"]
        location = request.form["location"]
        price  = request.form["price"] 
        duration = request.form["duration"]
        total_seat = request.form["total_seat"]
        available_seat = total_seat 
        status = request.form["status"]
        assigned_staff_id = request.form["assigned_staff_id"]
        difficulty = request.form["difficulty"]
        
        
        new_trek = Trek(
            trek_name = trek_name, 
            location = location , 
            price = price , 
            duration = duration , 
            total_seat = total_seat, 
            available_seat = available_seat , 
            status = status , 
            assigned_staff_id = assigned_staff_id ,
            difficulty = difficulty
        )
        
        db.session.add(new_trek)
        db.session.commit()
        return redirect("/view_all_trek")
    
    
    return render_template("5_add_trek.html")
    

# manage staff
@app.route("/manage_staff")
def Manage_Staff():
    return render_template("7_manage_staff.html")

# manage users
@app.route("/manage_user")
def Manage_User():
    return render_template("8_manage_users.html")

@app.route()
















# Creating admin 

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role ="admin").first()
    if admin is None:
        new_admin = User(
            name = "admin" ,
            email = "admin@gmail.com",
            password = "admin123" , 
            phone = "456278346", 
            role ="admin",
            status = "approved",
            is_blacklisted = False )
    
        db.session.add(new_admin)
        db.session.commit()







if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
