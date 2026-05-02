from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from datetime import date
from db import get_db
from models import insert_workout, insert_exercises

bp = Blueprint("log", __name__)

@bp.before_request
def open_db(): g.db = get_db()

@bp.teardown_request
def close_db(e): g.db.close()

@bp.route("/log")
def index():
    return render_template("log.html", today=str(date.today()))

@bp.route("/log/cardio", methods=["POST"])
def save_cardio():
    insert_workout(g.db, {
        "date":         request.form.get("date"),
        "type":         request.form.get("type", "Zone 2 Run"),
        "duration_min": request.form.get("duration_min"),
        "distance_mi":  request.form.get("distance_mi"),
        "avg_hr":       request.form.get("avg_hr"),
        "max_hr":       request.form.get("max_hr"),
        "calories":     request.form.get("calories"),
        "zone2_min":    request.form.get("zone2_min"),
        "avg_pace":     request.form.get("avg_pace"),
        "effort":       request.form.get("effort"),
        "notes":        request.form.get("notes"),
    })
    flash("Workout saved.")
    return redirect(url_for("history.index"))

@bp.route("/log/strength", methods=["POST"])
def save_strength():
    wid = insert_workout(g.db, {
        "date":  request.form.get("date"),
        "type":  request.form.get("type", "Upper Strength"),
        "notes": request.form.get("notes"),
    })
    names    = request.form.getlist("exercise_name[]")
    sets_l   = request.form.getlist("exercise_sets[]")
    reps_l   = request.form.getlist("exercise_reps[]")
    weights  = request.form.getlist("exercise_weight[]")
    exercises = [
        {"name": n, "sets": s, "reps": r, "weight_lbs": w}
        for n, s, r, w in zip(names, sets_l, reps_l, weights) if n.strip()
    ]
    if exercises:
        insert_exercises(g.db, wid, exercises)
    flash("Workout saved.")
    return redirect(url_for("history.index"))
