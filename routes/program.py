from flask import Blueprint, render_template

bp = Blueprint("program", __name__)

@bp.route("/program")
def index():
    return render_template("program.html")
