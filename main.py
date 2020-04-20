from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse



app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/fenixmcs_user'
app.config['SQLALCHEMY_TRACK_MODIFCATIONS']=False

login_manager = LoginManager(app)
login_manager.login_view = "login"

app.secret_key = '123'

from models import Stats, User, LoginForm, SignupForm
 
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

#SELECT plan_users.uuid, COUNT(plan_kills.id) as kills FROM plan_kills INNER JOIN plan_users WHERE plan_kills.killer_uuid = plan_users.uuid GROUP BY plan_users.uuid ORDER BY COUNT(plan_kills.id) DESC LIMIT 0, 25
@app.route('/stats', methods=['GET'])
def stats():
    stats = Stats.get_all()
    return render_template("stats.html", data = stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    print(form.email.data)
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash(u'Something wents wrong', 'danger')
    return render_template('login.html', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            password_confirm = form.password_confirm.data
            
            # Comprobamos que no hay ya un usuario con ese email
            user = User.get_by_email(email)
            if user is not None:
                flash(u'Email already registered', 'danger')
            else:
                #Verificamos si password == password
                if password == password_confirm:
                    # Creamos el usuario y lo guardamos
                    user = User(email=email)
                    user.set_password(password)
                    user.save()
                    # Dejamos al usuario logueado
                    next_page = request.args.get('next', None)
                    if not next_page or url_parse(next_page).netloc != '':
                        next_page = url_for('sign_up')
                    flash(u'Successfully registered', 'success')
                    return redirect(next_page)
                else:
                    flash(u'Check your passwords', 'danger')
                    return redirect(url_for('sign_up'))
    return render_template("signup.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))