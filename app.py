from flask import Flask, render_template, request, session, redirect, flash
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'super-secret-key'         # setting secret-key for login
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# users = [['Ayaan','ayaanpg@gmail.com','Ayaan123',1],['Einstein','einstein123@gmail.com','Einstein234']]

# class admin(db.Model):        # creating the class for admin database
#     sno = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(20),nullable=False)

class user(db.Model):        # creating the class for user database
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20),nullable=False)
    is_an_admin = db.Column(db.Integer,nullable=False)

class activity_details(db.Model):        #creating the class for activity database
    sno = db.Column(db.Integer,primary_key=True)
    event_name = db.Column(db.String(20),nullable=False)
    event_description = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    venue = db.Column(db.String(20), nullable=False)
    number_of_expected_participants = db.Column(db.Integer, nullable=False)
    
status = {
    -1 : "Rejected",
    0 : "Pending",
    1: "Accepted"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if 'user' in session and session['user'] == 'ayaanpg@gmail.com':       # checking if user is already in session
        # posts = my_posts.query.all()
        return render_template('events.html')
        
    if request.method == 'POST':
        username = request.form.get("email")
        userpass = request.form.get("password")
        print(username)
        print(type(userpass))
        if username == 'ayaanpg@gmail.com' and userpass == '123':       # validating the login info
            session['user'] = username      # adding user into the session
            # posts = my_posts.query.all()
            return render_template('loggedin.html')
        else:
            return redirect('/login')   # redirecting back to login page if login fails
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user')     # remove the user from the session
    return redirect('/login')

@app.route("/events_page")
def events_page():
    events = activity_details.query.all()
    print('user' in session)
    if 'user' in session and session['user'] == 'ayaanpg@gmail.com':   # checking if user is already in session
        admin_log_in = 1
    else:
        admin_log_in = 0
    # events = activity_details.query.order_by(activity_details.time_slot.desc())
    return render_template("events.html", events = events, status=status, admin_log_in = admin_log_in)

@app.route("/request_event")
def request_event():
    if request.method == 'POST':
        event_name = request.form.get('event_name')     
        event_description = request.form.get('event_description')
        date = request.form.get('date')
        venue = request.form.get('venue')
        number_of_expected_participants = request.form.get('number_of_expected_participants')
        entry = my_contacts(name=name,event_name=event_name,event_description=event_description,start=datetime.time(hour=10,minute=30),end=datetime.time(hour=12,minute=30),status=0,venue=venue,number_of_expected_participants=number_of_expected_participants)
        db.session.add(entry)      # making the database entry
        db.session.commit()
    return render_template('RequestAnEvent.html')

if __name__ == '__main__':
    app.run(debug=True)
