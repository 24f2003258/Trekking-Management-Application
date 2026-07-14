from flask import Flask , render_template ,redirect ,request ,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
                session["user_id"] = selected_user.user_id
                session["role"] = selected_user.role
                session["name"] = selected_user.name
                if(selected_user.role == "admin"):
                    return redirect("/admin_dashboard")
                elif(selected_user.role == "staff"):
                    return redirect("/staff_dashboard")
                else :
                    return redirect("/user_dashboard")
        
        
        
    return render_template("2.1_login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/staff_dashboard")
def staff_dashboard():
    if session.get("role") != "staff":
        return "Cann't Access UnAuthorized !"
    return render_template("4.1_staff_dashboard.html")

@app.route("/user_dashboard")
def user_dashboard():
    if (session.get("role") != "user" ):
        return "Cann't Access UnAuthorized !"
    return render_template("4.2_user_dashboard.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    if (session.get("role") != "admin" ):
        return "Cann't Access UnAuthorized !"
    return render_template("4_admin_dashboard.html")



@app.route("/viewAllUsers")
def viewAllUsers():
    AllUsers = User.query.filter_by(role="user").all()
    
    return render_template("viewAllUsers.html" ,all_users = AllUsers)



@app.route("/viewAllStaffs")
def viewAllStaff():
    allStaffs = User.query.filter_by(role="staff")
    return render_template("viewAllUsers.html",all_users = allStaffs )

@app.route("/pendingStaffs")
def viewAllPendingStaffs():
    allPendingStaffs = User.query.filter_by(role = "staff",status ="pending")
    return render_template("viewAllUsers.html",all_users = allPendingStaffs )

@app.route("/blacklistedStaffs")
def blacklistedStaffs():
    blacklistedStaffs = User.query.filter_by(role = "staff",is_blacklisted =True)
    return render_template("viewAllUsers.html",all_users = blacklistedStaffs )

@app.route("/blacklistedUsers")
def blacklistedUsers():
    blacklistedUsers = User.query.filter_by(role = "user",is_blacklisted =True)
    return render_template("viewAllUsers.html",all_users = blacklistedUsers )


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
        return redirect("/viewTreks")
    
    
    return render_template("5_add_trek.html")
    

@app.route("/viewTreks")
def viewTrek():
    viewAllTrek = Trek.query.all()
    return render_template("14_View_Treks.html", Treks = viewAllTrek)

@app.route("/openTreks")
def openTreks():
    openTreks = Trek.query.filter_by(status ="open").all()
    return render_template("14_View_Treks.html",Treks = openTreks)
    
@app.route("/closeTreks")
def closeTreks():
    closeTreks = Trek.query.filter_by(status ="close").all()
    return render_template("14_View_Treks.html",Treks = closeTreks)

@app.route("/completedTreks")
def completedTreks():
    completedTreks = Trek.query.filter_by(status ="completed").all()
    return render_template("14_View_Treks.html",Treks = completedTreks)


@app.route("/editTrek/<int:trek_id>" ,methods =["GET","POST"])
def editTrek(trek_id):
    selected_trek = Trek.query.filter_by(trek_id = trek_id).first()
        
    if request.method == "POST":
        selected_trek.trek_name = request.form["trek_name"]
        selected_trek.location = request.form["location"]
        selected_trek.price  = request.form["price"] 
        selected_trek.duration = request.form["duration"]
        selected_trek.total_seat = request.form["total_seat"]
        selected_trek.available_seat = selected_trek.total_seat 
        selected_trek.status = request.form["status"]
        selected_trek.assigned_staff_id = request.form["assigned_staff_id"]
        selected_trek.difficulty = request.form["difficulty"]
        
        db.session.commit()
        return redirect("/viewTreks")
    
    return render_template("editTrek.html" , trek = selected_trek )


@app.route("/available_treks")
def availableTrek():
    openTreks = Trek.query.filter_by(status ="open").all()
    return render_template("availableTrek.html",Treks = openTreks)

@app.route("/manage_treks")
def manage_treks():
    return render_template("6_manage_treks.html")


# manage staff
@app.route("/approve_staff")
def manage_staff():
    return render_template("7_manage_staff.html")

# manage users
@app.route("/approveStaff/<int:staffId>")
def approveStaff(staffId):
    selectedStaff = User.query.filter_by( id = staffId).first()
     
    selectedStaff.status = "approve"
    db.session.commit()
    return redirect("s")

@app.route("/assign_staff")
def assign_staff():
    return render_template("9_assign_staff.html")

@app.route("/assigned_trek")
def assigned_trek():
    staffId = session.get("user_id")
    if staffId is None : 
        return redirect("/login/")
    
    allTreks = Trek.query.filter_by(assigned_staff_id = staffId).all()
    return render_template("10_assigned_treks.html" , assigned_trek = allTreks)


@app.route("/book_trek/<int:trek_id>", methods =["GET","POST"])
def bookTrek(trek_id):
    selectTrek = Trek.query.filter_by(trek_id = trek_id).first()
    
    if request.method == "POST":
        
        user_id = session.get("user_id") 
        print(user_id)
        
        if user_id is None : 
            return redirect("/login/")
        
        bookedSeat =int( request.form["people"])
        selectTrek.available_seat -= bookedSeat 
        
        Book = Booking(
            user_id = user_id ,
            trek_id = selectTrek.trek_id ,
            number_of_people = bookedSeat,
            booking_date = datetime.today().date(),
            booking_status  = "confirmed"
        )
        db.session.add(Book)
        db.session.commit()
        return redirect("/myBookings")
    else :
        return render_template("bookTrek.html" ,booking = selectTrek)



    
@app.route("/myBookings")
def myBooking():
    userId = session.get("user_id")
    
    if userId is None : 
        return redirect("/login/")
    
    myBooking = Booking.query.filter_by(user_id = userId).all()
    print(myBooking)
    return render_template("booking.html", bookings = myBooking)


@app.route("/view_participants/<int:trekId>")
def viewParticiants(trekId):
    
    allParticipants = Booking.query.filter_by(trek_id = trekId).all()
    
    return render_template("viewParticipants.html",participants = allParticipants )
    







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
























@app.route("/check_session")
def check_session():

    return f"""
    User ID : {session.get('user_id')} <br>
    Name : {session.get('name')} <br>
    Role : {session.get('role')}
    """






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
