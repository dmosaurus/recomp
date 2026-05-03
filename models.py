from datetime import date as date_type
from config import CAL_TARGET, PRO_TARGET, CARB_TARGET, FAT_TARGET

# ── Workouts ───────────────────────────────────────────────────────────────────

def get_all_workouts(db):
    rows = db.execute("SELECT w.*, GROUP_CONCAT(e.name||'|'||e.sets||'|'||e.reps||'|'||e.weight_lbs, ';;') AS ex_str FROM workouts w LEFT JOIN exercises e ON e.workout_id=w.id GROUP BY w.id ORDER BY w.date DESC, w.id DESC").fetchall()
    return [_enrich(dict(r)) for r in rows]

def insert_workout(db, data):
    cur = db.execute(
        "INSERT INTO workouts (date,type,duration_min,distance_mi,avg_hr,max_hr,calories,zone2_min,avg_pace,effort,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (data.get("date"), data.get("type"), _f(data,"duration_min"), _f(data,"distance_mi"),
         _i(data,"avg_hr"), _i(data,"max_hr"), _i(data,"calories"), _f(data,"zone2_min"),
         data.get("avg_pace"), _i(data,"effort"), data.get("notes",""))
    )
    db.commit()
    return cur.lastrowid

def insert_exercises(db, workout_id, exercises):
    db.executemany(
        "INSERT INTO exercises (workout_id,name,sets,reps,weight_lbs) VALUES (?,?,?,?,?)",
        [(workout_id, e.get("name"), e.get("sets"), e.get("reps"), e.get("weight_lbs")) for e in exercises]
    )
    db.commit()

def get_weekly_summary(db):
    today = str(date_type.today())
    rows = db.execute("SELECT * FROM workouts WHERE date >= date(?, '-6 days') ORDER BY date DESC", (today,)).fetchall()
    return {"count": len(rows), "last": dict(rows[0]) if rows else None, "week": [dict(r) for r in rows]}

def get_workouts_for_chart(db):
    cardio = db.execute("SELECT date,avg_hr,distance_mi,calories FROM workouts WHERE type LIKE '%Run%' OR type LIKE '%Interval%' OR type='Active Recovery' ORDER BY date").fetchall()
    strength = db.execute("SELECT w.date, e.weight_lbs FROM workouts w JOIN exercises e ON e.workout_id=w.id WHERE e.name LIKE '%Deadlift%' ORDER BY w.date").fetchall()
    return {
        "labels":          [r["date"][5:] for r in cardio],
        "hr":              [r["avg_hr"] or 0 for r in cardio],
        "dist":            [r["distance_mi"] or 0 for r in cardio],
        "cal":             [r["calories"] or 0 for r in cardio],
        "dl_labels":       [r["date"][5:] for r in strength],
        "dl_vals":         [float(r["weight_lbs"] or 0) for r in strength],
    }

# ── Nutrition ──────────────────────────────────────────────────────────────────

def get_nutrition_for_date(db, day):
    return [dict(r) for r in db.execute("SELECT * FROM nutrition WHERE date=? ORDER BY created_at", (day,)).fetchall()]

def get_daily_totals(db, day):
    rows = get_nutrition_for_date(db, day)
    totals = {k: round(sum(r.get(k) or 0 for r in rows), 1) for k in ("calories","protein_g","carbs_g","fat_g","sugar_g","fiber_g")}
    totals["remaining_cal"] = max(0, CAL_TARGET - int(totals["calories"]))
    totals["pro_gap"]       = max(0, round(PRO_TARGET - totals["protein_g"], 1))
    totals["cal_pct"]  = min(100, round(totals["calories"]  / CAL_TARGET  * 100))
    totals["pro_pct"]  = min(100, round(totals["protein_g"] / PRO_TARGET  * 100))
    totals["carb_pct"] = min(100, round(totals["carbs_g"]   / CARB_TARGET * 100))
    totals["fat_pct"]  = min(100, round(totals["fat_g"]     / FAT_TARGET  * 100))
    totals["over_cal"] = totals["calories"] > CAL_TARGET
    return totals

def insert_nutrition(db, data):
    db.execute(
        "INSERT INTO nutrition (date,meal_type,food,serving_size,serving_unit,calories,protein_g,carbs_g,fat_g,sugar_g,fiber_g,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (data["date"], data["meal_type"], data["food"], data.get("serving_size"), data.get("serving_unit"),
         _f(data,"calories"), _f(data,"protein_g"), _f(data,"carbs_g"), _f(data,"fat_g"),
         _f(data,"sugar_g"), _f(data,"fiber_g"), data.get("notes",""))
    )
    db.commit()

def delete_nutrition(db, entry_id):
    db.execute("DELETE FROM nutrition WHERE id=?", (entry_id,))
    db.commit()

def update_nutrition(db, entry_id, data):
    db.execute(
        "UPDATE nutrition SET date=?,meal_type=?,food=?,serving_size=?,serving_unit=?,calories=?,protein_g=?,carbs_g=?,fat_g=?,sugar_g=?,fiber_g=?,notes=? WHERE id=?",
        (data["date"], data["meal_type"], data["food"], data.get("serving_size"), data.get("serving_unit"),
         _f(data,"calories"), _f(data,"protein_g"), _f(data,"carbs_g"), _f(data,"fat_g"),
         _f(data,"sugar_g"), _f(data,"fiber_g"), data.get("notes",""), entry_id)
    )
    db.commit()

def get_saved_foods(db):
    return [dict(r) for r in db.execute("SELECT * FROM saved_foods ORDER BY created_at DESC").fetchall()]

def save_food(db, data):
    db.execute(
        "INSERT INTO saved_foods (food,serving_size,serving_unit,calories,protein_g,carbs_g,fat_g,sugar_g,fiber_g) VALUES (?,?,?,?,?,?,?,?,?)",
        (data["food"], data.get("serving_size"), data.get("serving_unit"),
         _f(data,"calories"), _f(data,"protein_g"), _f(data,"carbs_g"),
         _f(data,"fat_g"), _f(data,"sugar_g"), _f(data,"fiber_g"))
    )
    db.commit()

def delete_saved_food(db, food_id):
    db.execute("DELETE FROM saved_foods WHERE id=?", (food_id,))
    db.commit()

# ── Body Scans ─────────────────────────────────────────────────────────────────

def get_latest_body_scan(db):
    row = db.execute("SELECT * FROM body_scans ORDER BY date DESC LIMIT 1").fetchone()
    return dict(row) if row else None

def insert_body_scan(db, data):
    db.execute(
        "INSERT INTO body_scans (date,weight_lb,lean_mass_lb,skeletal_muscle_lb,fat_mass_lb,body_fat_pct,visceral_fat,waist_hip_ratio,bone_mass_lb,bmr,score,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (data["date"], _f(data,"weight_lb"), _f(data,"lean_mass_lb"), _f(data,"skeletal_muscle_lb"),
         _f(data,"fat_mass_lb"), _f(data,"body_fat_pct"), _i(data,"visceral_fat"),
         _f(data,"waist_hip_ratio"), _f(data,"bone_mass_lb"), _i(data,"bmr"), _f(data,"score"), data.get("notes",""))
    )
    db.commit()

# ── Helpers ────────────────────────────────────────────────────────────────────

def _f(d, k): return float(d[k]) if d.get(k) not in (None, "") else None
def _i(d, k): return int(d[k])   if d.get(k) not in (None, "") else None

def _enrich(row):
    ex_str = row.pop("ex_str", None)
    row["exercises"] = []
    if ex_str:
        for part in ex_str.split(";;"):
            cols = part.split("|")
            if len(cols) == 4:
                row["exercises"].append({"name": cols[0], "sets": cols[1], "reps": cols[2], "weight_lbs": cols[3]})
    return row
