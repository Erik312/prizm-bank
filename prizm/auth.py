import bcrypt
from flask import Blueprint,render_template,redirect,request,session,flash,url_for
from flask_wtf import FlaskForm
from prizm import db
from prizm.models import User
from prizm.models import Transaction




bp = Blueprint('auth', __name__,url_prefix="/auth")


#sign up route
@bp.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == "POST":
        if 'user' in session:
            return redirect(url_for('user.userhome'))
        else:
            print("huh")
            new_signup_name = request.form['full_name']
            new_signup_email = request.form['email']
            new_signup_password = request.form['password']
            b = new_signup_password.encode('utf-8')
            hashed_pw = bcrypt.hashpw(b,bcrypt.gensalt(12))

            print("validating..")
            check_existing_email = User.query.filter_by(email=new_signup_email).first()
            if check_existing_email:
                print("email already exist")
                flash("Error on signup")
                return redirect(url_for('auth.signup'))
            else:
                print("creating")
                new_user = User(new_signup_name,new_signup_email,hashed_pw.decode("utf-8"))
                db.session.add(new_user)
                db.session.flush()
                signup_log = Transaction(sender=new_user.email,reciever=new_user.email,user_id=new_user.id,date="now",amount=0,description=f"{new_user.email} account creation.")
                
                db.session.add(signup_log)
                db.session.commit()
                print("Success")
                flash("Account created successfully. Please login")
                return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')








#login route
@bp.route('/login',methods=['POST','GET'])
def login():
    if 'user' in session:
        return redirect('/user_home')
    else:
        if request.method == 'POST':
            print("time to work")
            login_user_email = request.form['email']
            login_password = request.form['password']
            print("checking for user")

            check_for_user = User.query.filter_by(email=login_user_email).first()
            b = login_password.encode('utf-8')
            if check_for_user:
                if bcrypt.checkpw(b,check_for_user.password.encode('utf-8')):
                    session['user'] = check_for_user.id
                    print("1")
                    return redirect(url_for("user.userhome"))
                else:
                    flash("Incorrect email or password")
                    return redirect(url_for("auth.login"))
            else:
                flash("Incorrect email or password")
                return redirect(url_for("auth.login"))

        else:
            return render_template('login.html')












#logout route
@bp.route('/logout', methods=['POST','GET'])
def logout():

    session.clear()

    return redirect(url_for('home.home'))
