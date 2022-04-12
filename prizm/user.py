import datetime
from flask import request,session,render_template,redirect,flash,Blueprint,url_for
from prizm import db
from prizm.models import User
from prizm.models import Transaction


bp = Blueprint("user",__name__,url_prefix="/user")



@bp.route('/userhome', methods=['POST','GET'])
def userhome():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    else:
        user_home_query = User.query.filter_by(id=session['user']).first()
        home_data = [user_home_query.full_name,user_home_query.balance]
        date = datetime.datetime.now()
        return render_template("user_home.html",home_data=home_data,date=date.strftime("%c"))



@bp.route('/history', methods=['POST','GET'])
def history_page():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    else:
        transaction_query  = Transaction.query.filter_by(user_id=session['user']).all()
        return render_template('history.html', transaction_query=transaction_query)


@bp.route('/send')
def send():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    else:
        return render_template('send.html')




@bp.route('/send_to_user', methods=["POST","GET"])
def send_to_user():
    if 'user' not in session:
        abort()
    else:
        recipient_email = request.form['recipient']
        amount_form = request.form['amount']
        amount_converted = int(amount_form)
        check_for_user = User.query.filter_by(email=recipient_email).first()
        if check_for_user:
            user_account_query = User.query.filter_by(id=session['user']).first()
            user_account_balance = user_account_query.balance

            if amount_converted > user_account_balance:
                print("insufficient funds")
                flash("insufficient funds")
                return redirect(url_for('user.send'))
            else:
                user_account_query.balance = user_account_query.balance - amount_converted
                check_for_user.balance = check_for_user.balance + amount_converted
                record_transaction = Transaction(sender=user_account_query.email,reciever=check_for_user.email,user_id=session['user'],date="now",amount=amount_converted,description=f"{user_account_query.email} sent {check_for_user.email} {amount_converted} dollars")
                db.session.add(record_transaction)
                db.session.flush()
                record_transaction_two = Transaction(sender=user_account_query.email,reciever=check_for_user.email,user_id=check_for_user.id,date="now",amount=amount_converted,description=f"{user_account_query.email} sent {check_for_user.email} {amount_converted} dollars")
                db.session.add(record_transaction_two)
                db.session.commit()
                print("sent")
                flash("Funds Successfully sent")
                return redirect(url_for('user.userhome'))
        else:
            flash("Error sending. Invalid recipient email")
            return redirect(url_for('user.send'))



@bp.route('/deposit', methods=['POST','GET'])
def deposit():
    if 'user' not in session:
        abort(403)
    else:
        try:
            deposit_form_amount = request.form['amount']
            converted_deposit = int(deposit_form_amount)
            get_user = User.query.filter_by(id=session['user']).first()
            get_user.balance = get_user.balance + converted_deposit
            record_transaction = Transaction(sender="Big Bank",reciever=get_user.email,user_id=session['user'],date="now",amount=converted_deposit,description="Deposit to account")
            db.session.add(record_transaction)
            db.session.commit()
            print("deposit test")
            flash("Deposit successful")
            return redirect(url_for('user.userhome'))
        except:
            flash("Error on deposit")
            return redirect(url_for('user.send'))


@bp.route('/account_settings', methods=['POST','GET'])
def account_settings():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    else:
        if request.method == 'POST':
            try:
                current_user_id = session['user']
                user_data_query = User.query.filter_by(id=current_user_id).first()
                db.session.delete(user_data_query)
                db.session.commit()
                session.clear()
                flash("Successfully deleted acccount")
                return redirect(url_for('auth.login'))
            except:
                flash("An error occured")
                return redirect(url_for('user.account_settings'))
        else:
            user_query = User.query.filter_by(id=session['user']).first()
            user_data = []
            user_name = user_query.full_name
            user_email = user_query.email
            user_account_number = user_query.account_number
            user_data.append(user_name)
            user_data.append(user_email)
            user_data.append(user_account_number)
            return render_template('account_page.html', user_data=user_data)
