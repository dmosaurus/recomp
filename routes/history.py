from flask import Blueprint, render_template, g
from db import get_db
from models import get_all_workouts

bp = Blueprint("history", __name__)

@bp.before_request
def open_db(): g.db = get_db()

@bp.teardown_request
def close_db(e): g.db.close()

@bp.route("/history")
def index():
    return render_template("history.html", workouts=get_all_workouts(g.db))
