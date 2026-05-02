import sqlite3
import os
from config import DB_PATH, BODY_SCAN_DEFAULTS

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            duration_min REAL, distance_mi REAL, avg_hr INTEGER, max_hr INTEGER,
            calories INTEGER, zone2_min REAL, avg_pace TEXT, effort INTEGER,
            notes TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER REFERENCES workouts(id) ON DELETE CASCADE,
            name TEXT, sets TEXT, reps TEXT, weight_lbs TEXT
        );
        CREATE TABLE IF NOT EXISTS nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL, meal_type TEXT NOT NULL, food TEXT NOT NULL,
            serving_size TEXT, serving_unit TEXT,
            calories REAL, protein_g REAL, carbs_g REAL, fat_g REAL,
            sugar_g REAL, fiber_g REAL, notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS body_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL, weight_lb REAL, lean_mass_lb REAL,
            skeletal_muscle_lb REAL, fat_mass_lb REAL, body_fat_pct REAL,
            visceral_fat INTEGER, waist_hip_ratio REAL, bone_mass_lb REAL,
            bmr INTEGER, score REAL, notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()
    seed_db(db)
    db.close()

def seed_db(db):
    if db.execute("SELECT COUNT(*) FROM workouts").fetchone()[0] == 0:
        cur = db.execute(
            "INSERT INTO workouts (date,type,duration_min,distance_mi,avg_hr,max_hr,calories,zone2_min,avg_pace,effort,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            ("2026-04-22","Zone 2 Run",63,4.68,133,154,596,34,"13:33",5,
             "First workout back. Cardiac drift to Zone 3 in miles 2-4. Had to slow to 2.8 mph to manage HR. Zone 2 baseline pace: ~11:30 min/mi.")
        )
        db.commit()
    if db.execute("SELECT COUNT(*) FROM body_scans").fetchone()[0] == 0:
        s = BODY_SCAN_DEFAULTS
        db.execute(
            "INSERT INTO body_scans (date,weight_lb,lean_mass_lb,skeletal_muscle_lb,fat_mass_lb,body_fat_pct,visceral_fat,waist_hip_ratio,bone_mass_lb,bmr,score,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (s["date"],s["weight_lb"],s["lean_mass_lb"],s["skeletal_muscle_lb"],s["fat_mass_lb"],
             s["body_fat_pct"],s["visceral_fat"],s["waist_hip_ratio"],s["bone_mass_lb"],s["bmr"],s["score"],s["notes"])
        )
        db.commit()
