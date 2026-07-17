import os
import tempfile

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.services.analyzer import analyze_file

review_bp = Blueprint("review", __name__)


def allowed_file(filename):
    """Check whether uploaded file is allowed."""
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in current_app.config["ALLOWED_EXTENSIONS"]


# ---------------------------------------------------------
# Review Page
# ---------------------------------------------------------

@review_bp.route("/review")
@login_required
def review():
    return render_template("review.html")


# ---------------------------------------------------------
# Upload Python File
# ---------------------------------------------------------

@review_bp.route("/review/upload", methods=["POST"])
@login_required
def upload_file():

    if "code_file" not in request.files:
        flash("Please choose a file.", "danger")
        return redirect(url_for("review.review"))

    file = request.files["code_file"]

    if file.filename == "":
        flash("No file selected.", "warning")
        return redirect(url_for("review.review"))

    if not allowed_file(file.filename):
        flash("Only .py, .pyw and .zip files are allowed.", "danger")
        return redirect(url_for("review.review"))

    filename = secure_filename(file.filename)

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    try:
        analysis = analyze_file(filepath)

        return render_template(
            "result.html",
            filename=filename,
            analysis=analysis,
        )

    except Exception as e:
        flash(f"Analysis failed: {e}", "danger")
        return redirect(url_for("review.review"))


# ---------------------------------------------------------
# Paste Python Code
# ---------------------------------------------------------

@review_bp.route("/review/paste", methods=["POST"])
@login_required
def paste_code():

    code = request.form.get("code", "").strip()

    if not code:
        flash("Please paste some Python code.", "warning")
        return redirect(url_for("review.review"))

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".py",
        mode="w",
        encoding="utf-8",
    )

    temp.write(code)
    temp.close()

    try:
        analysis = analyze_file(temp.name)

        return render_template(
            "result.html",
            filename="Pasted Code",
            analysis=analysis,
        )

    except Exception as e:
        flash(f"Analysis failed: {e}", "danger")
        return redirect(url_for("review.review"))

    finally:
        try:
            os.remove(temp.name)
        except Exception:
            pass