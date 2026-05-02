from flask import Blueprint, render_template, jsonify, g
from db import get_db
from models import get_workouts_for_chart

bp = Blueprint("progress", __name__)

@bp.before_request
def open_db(): g.db = get_db()

@bp.teardown_request
def close_db(e): g.db.close()

@bp.route("/progress")
def index():
    return render_template("progress.html")

@bp.route("/api/chart-data")
def chart_data():
    return jsonify(get_workouts_for_chart(g.db))
