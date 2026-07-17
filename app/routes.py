from flask import Blueprint, render_template

# Blueprint for general/core pages (non-auth, non-review specific)
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@main_bp.route("/history")
def history():
    return render_template("history.html")


@main_bp.route("/settings")
def settings():
    return render_template("settings.html")