from flask import Flask, render_template, request, session, redirect, flash
from flask_login import current_user, logout_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'super-secret-key'         # setting secret-key for login
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


class admin(db.Model):        # creating the class for admin database
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20),nullable=False)

class user(db.Model):        # creating the class for user database
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20),nullable=False)

class activity_details(db.Model):        #creating the class for activity database
    sno = db.Column(db.Integer,primary_key=True)
    event_name = db.Column(db.String(20),nullable=False)
    event_description = db.Column(db.String(120), nullable=False)
    time_slot = db.Column(db.DateTime,nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    username = db.Column(db.String(20),nullable=False)
    place = db.Column(db.String(20), nullable=False)
    number_of_expected_paricipants = db.Column(db.Integer, nullable=False)
    
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
    # if 'user' in session and session['user'] == 'ayaanpg@gmail.com':       # checking if user is already in session
        # posts = my_posts.query.all()
        # return render_template('loggedin.html')
        
    if current_user.is_authenticated:
        admin_log_in = 1
        user_query = db.session.filter_by(email = current_user.username).first() is not None
        if user_query:
            admin_log_in = 0
        return render_template('events.html',admin_log_in=admin_log_in)
        
    if request.method == 'POST':
        username = request.form.get("email")
        userpass = request.form.get("password")
        print(username)
        print(type(userpass))
        user_query = db.session.filter_by(email = current_user.username).first() is not None
        admin_query = db.session.filter_by(email = current_user.username).first() is not None
        admin_log_in = 1
        if user_query:
            admin_log_in = 0
        if admin_query or user_query:
            current_user.username = username      # adding user into the session
            current_user.userpass = userpass
            # posts = my_posts.query.all()
            return render_template('events.html', admin_log_in=admin_log_in)
        # elif username == 'ayaanpg@gmail.com' and userpass == '123':       # validating the login info
        #     return redirect('/login')   # redirecting back to login page if login fails
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    flash(f"User logged out")
    # session.pop('user')     # remove the user from the session
    return redirect('/login')

@login_required
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

if __name__ == '__main__':
    app.run(debug=True)
