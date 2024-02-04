from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from model import db, Participant, CentralBank, Transaction  # Adjust import here
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('routes', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'])
        new_user = Participant(name=request.form['name'], password=hashed_password, coins=100)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Participant.query.filter_by(name=request.form['name']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('routes.homepage'))
    return render_template('login.html')


@bp.route('/homepage', methods=['GET'])
@login_required
def homepage():
    participants = Participant.query.all()
    central_bank = CentralBank.query.all()
    cb_activity = sum([central_bank.coins for central_bank in central_bank])
    total_activity = sum([participant.coins for participant in participants],cb_activity)

    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return render_template('homepage.html', participants=participants, central_bank=central_bank, transactions=transactions,total_activity=total_activity,cb_activity=cb_activity)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form['name']
        db.session.commit()
        return redirect(url_for('routes.homepage'))
    return render_template('profile.html')

@bp.route('/transact', methods=['GET', 'POST'])
@login_required
def transact():
    if request.method == 'POST':
        receiver = Participant.query.filter_by(name=request.form['receiver']).first()
        if receiver and current_user.coins >= int(request.form['coins']):
            current_user.coins -= int(request.form['coins'])
            receiver.coins += int(request.form['coins'])
            transaction = Transaction(timestamp=datetime.utcnow(), sender_id=current_user.id, receiver_id=receiver.id, subject=request.form['subject'])
            db.session.add(transaction)
            db.session.commit()
        return redirect(url_for('routes.homepage'))
    return render_template('transact.html')

@bp.route('/redistribute', methods=['POST'])
@login_required
def redistribute():
    if current_user.id != 1:  # Assuming the central bank's ID is 1
        return redirect(url_for('routes.homepage'))
    participants = Participant.query.all()
    total_activity = sum([p.activity for p in participants])
    for participant in participants:
        participant.coins += (participant.activity / total_activity) * CentralBank.query.first().coins
        participant.activity = 0
    CentralBank.query.first().coins = 0
    db.session.commit()
    return redirect(url_for('routes.homepage'))

@bp.route('/exit', methods=['POST'])
@login_required
def exit():
    CentralBank.query.first().coins += current_user.coins
    current_user.coins = 0
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('routes.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))