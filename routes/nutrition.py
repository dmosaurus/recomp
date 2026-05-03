from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from datetime import date
from db import get_db
from models import get_nutrition_for_date, get_daily_totals, insert_nutrition, delete_nutrition, update_nutrition, get_saved_foods, save_food, delete_saved_food
from config import QUICK_FOODS, CAL_TARGET, PRO_TARGET, CARB_TARGET, FAT_TARGET

bp = Blueprint("nutrition", __name__)

@bp.before_request
def open_db(): g.db = get_db()

@bp.teardown_request
def close_db(e): g.db.close()

@bp.route("/nutrition")
def index():
    day = request.args.get("date", str(date.today()))
    return render_template("nutrition.html",
        day=day,
        entries=get_nutrition_for_date(g.db, day),
        totals=get_daily_totals(g.db, day),
        meal_types=["Breakfast","Lunch","Dinner","Snack","Pre-Workout","Post-Workout","Supplement"],
        targets={"cal": CAL_TARGET, "pro": PRO_TARGET, "carb": CARB_TARGET, "fat": FAT_TARGET},
        saved_foods=get_saved_foods(g.db),
    )

@bp.route("/nutrition", methods=["POST"])
def save():
    insert_nutrition(g.db, {
        "date":        request.form.get("date", str(date.today())),
        "meal_type":   request.form.get("meal_type", "Snack"),
        "food":        request.form.get("food"),
        "serving_size":  request.form.get("serving_size"),
        "serving_unit":  request.form.get("serving_unit"),
        "calories":    request.form.get("calories"),
        "protein_g":   request.form.get("protein_g"),
        "carbs_g":     request.form.get("carbs_g"),
        "fat_g":       request.form.get("fat_g"),
        "sugar_g":     request.form.get("sugar_g"),
        "fiber_g":     request.form.get("fiber_g"),
        "notes":       request.form.get("notes"),
    })
    flash("Food logged.")
    return redirect(url_for("nutrition.index", date=request.form.get("date", str(date.today()))))

@bp.route("/nutrition/delete", methods=["POST"])
def delete():
    day = request.form.get("date", str(date.today()))
    delete_nutrition(g.db, request.form.get("id"))
    flash("Entry removed.")
    return redirect(url_for("nutrition.index", date=day))

@bp.route("/nutrition/update", methods=["POST"])
def update():
    day = request.form.get("date", str(date.today()))
    update_nutrition(g.db, request.form.get("id"), {
        "date": day, "meal_type": request.form.get("meal_type", "Snack"),
        "food": request.form.get("food"), "serving_size": request.form.get("serving_size"),
        "serving_unit": request.form.get("serving_unit"), "calories": request.form.get("calories"),
        "protein_g": request.form.get("protein_g"), "carbs_g": request.form.get("carbs_g"),
        "fat_g": request.form.get("fat_g"), "sugar_g": request.form.get("sugar_g"),
        "fiber_g": request.form.get("fiber_g"), "notes": request.form.get("notes"),
    })
    flash("Entry updated.")
    return redirect(url_for("nutrition.index", date=day))

@bp.route("/nutrition/pin", methods=["POST"])
def pin():
    day = request.form.get("date", str(date.today()))
    save_food(g.db, {
        "food": request.form.get("food"), "serving_size": request.form.get("serving_size"),
        "serving_unit": request.form.get("serving_unit"), "calories": request.form.get("calories"),
        "protein_g": request.form.get("protein_g"), "carbs_g": request.form.get("carbs_g"),
        "fat_g": request.form.get("fat_g"), "sugar_g": request.form.get("sugar_g"),
        "fiber_g": request.form.get("fiber_g"),
    })
    flash("Saved to quick add.")
    return redirect(url_for("nutrition.index", date=day))

@bp.route("/nutrition/unpin", methods=["POST"])
def unpin():
    day = request.form.get("date", str(date.today()))
    delete_saved_food(g.db, request.form.get("id"))
    flash("Removed from quick add.")
    return redirect(url_for("nutrition.index", date=day))
