from hub import app, api_bp, login_required, login_manager, request, redirect, login_user, logout_user, current_user, url_for, flash
from flask import render_template
from hub.model import User, db
from hub import request, generate_password_hash, check_password_hash
import requests
import json

@app.route('/')
@app.route('/home')
@login_required
def home():
    flash('This is a flashed message')
    return render_template('home.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('login')
    
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('home', user=user))  # Redirect to a different endpoint after login
        else:
            flash('Incorrect Login, Check your Username and Password before trying again')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/example')
def example():
    return(redirect(url_for('home')))


@app.route('/api', methods=['POST', 'GET'])
@login_required
def api():
    if request.method == 'POST':
        country = request.form['country'].title()
        print(country)
        url = 'http://127.0.0.1:5000/'
        response = requests.get(url + f'country/{country}')
        response_code = response.status_code
        response = response.text
        response = json.loads(response)
        response = json.dumps(response, indent=4)

        return render_template('api.html', response=response)

    return render_template('api.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@api_bp.route('/hello')
def hello():
    return 'Hello World'


app.register_blueprint(api_bp)