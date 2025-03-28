from flask import Flask, request, render_template, redirect, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, create_refresh_token,
    get_jwt, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
)
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect, generate_csrf

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret' # chave secreta para assinar tokens - JWT
app.config['JWT_TOKEN_LOCATION'] = ['cookies'] # os tokens são armazenados em cookies
app.config['JWT_COOKIE_SECURE'] = False  
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['SECRET_KEY'] = 'outra-chave-secreta' # chave para segurança dos formulários Flask
app.config['WTF_CSRF_CHECK_DEFAULT'] = False


db = SQLAlchemy(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app) # proteção contra CSRF


@app.context_processor
def inject_csrf_token():
    return {'csrf_token': generate_csrf()}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


with app.app_context():
    db.create_all()


def print_database():
    users = User.query.all()
    print("\n=== DADOS DO BANCO ===")
    for user in users:
        print(f"ID: {user.id}, Nome: {user.name}, Email: {user.email}")
    print("=====================\n")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash("Email já registrado!", "danger")
            return redirect('/register')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Conta criada com sucesso! Faça login.", "success")
        print_database()  # Mostra dados após registro
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember_me') == 'on'

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            
            response = redirect('/dashboard')
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            
            # Mostra informações do login e dados do banco
            print("\n=== LOGIN REALIZADO ===")
            print(f"Usuário logado: {user.name} ({user.email})")
            print_database()
            
            if remember_me:
                app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
            else:
                app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
                
            flash("Login realizado com sucesso!", "success")
            return response
        else:
            flash("Credenciais inválidas!", "danger")
            return redirect('/login')

    return render_template('login.html')

@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    return render_template('dashboard.html', user=user)

@app.route('/logout', methods=['POST'])
def logout():
    response = redirect('/login')
    unset_jwt_cookies(response)
    flash("Você foi deslogado com sucesso.", "success")
    return response

if __name__ == '__main__':
    app.run(debug=True)