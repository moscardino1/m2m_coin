#routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from model import db, Participant, CentralBank, Transaction  # Adjust import here
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('routes.homepage'))
    else:
        return redirect(url_for('routes.login'))
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Check if the username already exists
        existing_user = Participant.query.filter_by(name=request.form['name']).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('routes.register'))

        # If the username is unique, proceed with registration
        hashed_password = generate_password_hash(request.form['password'])
        new_user = Participant(name=request.form['name'], password=hashed_password, coins=100)
        db.session.add(new_user)
        db.session.commit()

        # Add transaction for entering the system
        transaction = Transaction(timestamp=datetime.utcnow(), sender=new_user, receiver=new_user, amount=100, subject="entered the system")
        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for('routes.login'))
    return render_template('register.html')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message
    if request.method == 'POST':
        user = Participant.query.filter_by(name=request.form['name']).first()
        if user and check_password_hash(user.password, request.form['password']):
            if user.is_active:
                login_user(user)
                return redirect(url_for('routes.homepage'))
            else:
                error = "User is not active. Please contact the administrator."  # Set error message
        else:
            error = "Invalid username or password"  # Set error message
    return render_template('login.html', error=error)



@bp.route('/homepage', methods=['GET'])
@login_required
def homepage():
    active_participants = Participant.query.filter_by(is_active=True).all()
    central_bank = CentralBank.query.first()

    if central_bank:
        cb_coins = central_bank.coins
    else:
        cb_coins = 0

    total_activity = sum([participant.coins for participant in active_participants]) + cb_coins
    perc_user = current_user.coins / total_activity 
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()

    # Calculate the ratio of each participant's coins to the total activity
    participant_ratios = []
    for participant in active_participants:
        ratio = participant.coins / total_activity  
        participant_ratios.append(ratio)

    return render_template('homepage.html', perc_user=perc_user, participants=active_participants, central_bank=central_bank,
                           transactions=transactions, total_activity=total_activity, participant_ratios=participant_ratios)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form['name']
        profile_picture_url = request.form['profile_picture_url']
        current_user.profile_picture_url = profile_picture_url

        db.session.commit()
        return redirect(url_for('routes.homepage'))
    return render_template('profile.html')

@bp.route('/transact', methods=['GET', 'POST'])
@login_required
def transact():
    if request.method == 'POST':
        receiver = Participant.query.filter_by(name=request.form['receiver']).first()
        amount = int(request.form['coins'])  # Get the amount from the form data
        if receiver and current_user.coins >= amount:
            current_user.coins -= amount
            receiver.coins += amount
            transaction = Transaction(timestamp=datetime.utcnow(), sender=current_user, receiver=receiver, amount=amount, subject=request.form['subject'])
            db.session.add(transaction)
            db.session.commit()
        return redirect(url_for('routes.homepage'))
    return render_template('transact.html')


@bp.route('/redistribute-coins', methods=['POST'])
@login_required
def redistribute_coins():
    if current_user.coins == 0:
        return redirect(url_for('routes.homepage'))

    active_participants = Participant.query.filter_by(is_active=True).all()
    num_participants = len(active_participants)

    if num_participants == 0:
        return redirect(url_for('routes.homepage'))

    redistribution_amount = current_user.coins // (num_participants - 1)

    for participant in active_participants:
        if participant != current_user:  # Skip redistribution to the current user
            participant.coins += redistribution_amount

            # Log redistribution transaction for each participant
            transaction = Transaction(timestamp=datetime.utcnow(), sender=current_user, receiver=participant, amount=redistribution_amount, subject="Redistribution spot")
            db.session.add(transaction)

    current_user.coins = 0
    db.session.commit()

    return redirect(url_for('routes.homepage'))
@bp.route('/exit-system', methods=['POST'])
@login_required
def exit_system():
    if 'exit-system' in request.form:
        if current_user.coins > 0:
            active_participants = Participant.query.filter(Participant.is_active == True).all()
            num_participants = len(active_participants)
            
            if num_participants > 0:
                redistribution_amount = current_user.coins // (num_participants - 1)
                
                for participant in active_participants:
                    if participant != current_user:  # Skip redistribution to the current user
                        participant.coins += redistribution_amount

                        # Log redistribution transaction for each participant
                        transaction = Transaction(timestamp=datetime.utcnow(), sender=current_user, receiver=participant, amount=redistribution_amount, subject="Redistribution exit")
                        db.session.add(transaction)
                
                db.session.commit()

        current_user.is_active = False
        db.session.commit()
        logout_user()

    return redirect(url_for('routes.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))


@bp.route('/faq')
def faq():
    return render_template('faq.html')
