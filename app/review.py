from flask import Blueprint, render_template

review_bp = Blueprint("review", __name__)

@review_bp.route("/review")
def review():
    return render_template("review.html")

@review_bp.route("/result")
def result():
    return render_template("result.html")