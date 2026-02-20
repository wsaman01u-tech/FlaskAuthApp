from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "mysecretkey123"

# ── Create database and table when app starts ──
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            email    TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ── Home Page ──
@app.route('/')
def home():
    return render_template('home.html')

# ── Register Page ──
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # Get data from form
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # ── THIS IS THE BUG FIX: Check if fields are empty ──

        if name == '':
            flash('Name is required.', 'danger')
            return render_template('register.html')

        if email == '':
            flash('Email is required.', 'danger')
            return render_template('register.html')

        if password == '':
            flash('Password is required.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')

        # ── Check if email already exists in database ──
        conn = sqlite3.connect('users.db')
        user = conn.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone()

        if user:
            flash('This email is already registered. Please login.', 'danger')
            conn.close()
            return render_template('register.html')

        # ── All checks passed: save user to database ──
        hashed_password = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        conn.commit()
        conn.close()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    # If GET request, just show the form
    return render_template('register.html')


# ── Login Page ──
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if email == '' or password == '':
            flash('Email and password are required.', 'danger')
            return render_template('login.html')

        conn = sqlite3.connect('users.db')
        user = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        conn.close()

        # user[3] is the password column
        if user and check_password_hash(user[3], password):
            session['user_name'] = user[1]  # user[1] is name
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Wrong email or password.', 'danger')
            return render_template('login.html')

    return render_template('login.html')


# ── Dashboard Page ──
@app.route('/dashboard')
def dashboard():
    if 'user_name' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# ── Logout ──
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ── Run the app ──
if __name__ == '__main__':
    init_db()
    app.run(debug=True)