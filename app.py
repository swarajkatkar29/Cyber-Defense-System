from flask import Flask, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

app.secret_key = "cybersecret"

@app.route('/')
def home():
    return '''
    <h1>Cyber Secure Login</h1>

    <h2>Register</h2>

    <form method="POST" action="/register">
        Username:
        <input type="text" name="username"><br><br>

        Password:
        <input type="password" name="password"><br><br>

        <input type="submit" value="Register">
    </form>

    <hr>

    <h2>Login</h2>

    <form method="POST" action="/login">
        Username:
        <input type="text" name="username"><br><br>

        Password:
        <input type="password" name="password"><br><br>

        <input type="submit" value="Login">
    </form>
    '''

@app.route('/register', methods=['POST'])
def register():

    username = request.form['username']
    password = request.form['password']

    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )

    conn.commit()
    conn.close()

    return "<h1>User Registered Successfully</h1>"

@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result and check_password_hash(result[0], password):

        session['user'] = username

        return redirect('/dashboard')

    return "<h1>Invalid Credentials</h1>"

@app.route('/dashboard')
def dashboard():

    if 'user' in session:

        return f'''
        <h1>Welcome {session['user']}</h1>

        <h2>Cybersecurity Dashboard</h2>

        <a href="/logout">Logout</a>
        '''

    return redirect('/')

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
