from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# ==========================================
# Flask App Configuration
# ==========================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "your_secret_key_here"

# ==========================================
# Database Configuration
# ==========================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "database", "database.db")

print("Database Path:", db_path)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==========================================
# User Model
# ==========================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def __repr__(self):
        return f"<User {self.username}>"

# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================================
# Login Page
# ==========================================

@app.route("/login")
def login():
    return render_template("login.html")

# ==========================================
# Register Page
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        print("=" * 50)
        print("Username:", username)
        print("Email:", email)

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            print("❌ Email already exists!")
            return "Email already exists! Please use another email."

        # Hash password
        hashed_password = generate_password_hash(password)

        print("Password Hash:", hashed_password)

        # Create user object
        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        # Save user
        db.session.add(new_user)
        db.session.commit()

        print("✅ User inserted successfully!")

        # Print all users
        users = User.query.all()
        print("Current Users:")
        for user in users:
            print(user.id, user.username, user.email)

        return redirect(url_for("login"))

    return render_template("register.html")

# ==========================================
# Create Database
# ==========================================

with app.app_context():
    db.create_all()

# ==========================================
# Run Flask
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)