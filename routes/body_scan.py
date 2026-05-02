import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from db import get_db
from models import insert_body_scan, get_latest_body_scan

bp = Blueprint("body_scan", __name__)

@bp.before_request
def open_db(): g.db = get_db()

@bp.teardown_request
def close_db(e): g.db.close()

@bp.route("/body-scan")
def index():
    return render_template("body_scan.html", scan=get_latest_body_scan(g.db))

@bp.route("/body-scan/upload", methods=["POST"])
def upload():
    f = request.files.get("pdf")
    if not f or not f.filename.endswith(".pdf"):
        flash("Please upload a PDF file.")
        return redirect(url_for("body_scan.index"))
    try:
        import pdfplumber
        with pdfplumber.open(f) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        data = _parse_ge_cs10g(text)
        data["date"] = request.form.get("date") or data.get("date", "")
        if not data.get("date"):
            flash("Could not detect scan date — please enter it manually.")
            return redirect(url_for("body_scan.index"))
        insert_body_scan(g.db, data)
        flash("Body scan uploaded.")
    except Exception as e:
        flash(f"Parse error: {e}")
    return redirect(url_for("dashboard.index"))

def _parse_ge_cs10g(text):
    def _num(pattern): m = re.search(pattern, text); return float(m.group(1)) if m else None
    def _int(pattern): m = re.search(pattern, text); return int(m.group(1))   if m else None
    return {
        "date":               _date(text),
        "weight_lb":          _num(r"Body Weight[\s\S]*?([\d.]+)\s*lb"),
        "lean_mass_lb":       _num(r"Lean Body Mass[\s\S]*?([\d.]+)\s*lb"),
        "skeletal_muscle_lb": _num(r"Skeletal Muscle[\s\S]*?([\d.]+)\s*lb"),
        "fat_mass_lb":        _num(r"Body Fat Mass[\s\S]*?([\d.]+)\s*lb"),
        "body_fat_pct":       _num(r"Body Fat\s*%[\s\S]*?([\d.]+)\s*%"),
        "visceral_fat":       _int(r"Visceral Fat Level[\s\S]*?(\d+)"),
        "waist_hip_ratio":    _num(r"Waist-Hip Ratio[\s\S]*?([\d.]+)"),
        "bone_mass_lb":       _num(r"Bone Mass[\s\S]*?([\d.]+)\s*lb"),
        "bmr":                _int(r"Basal Metabolic Rate[\s\S]*?(\d{4,5})"),
        "score":              _num(r"Score[\s\S]*?([\d.]+)\s*/\s*100"),
        "notes":              "GE CS10G · parsed from PDF",
    }

def _date(text):
    m = re.search(r"(\d{4})[/-](\d{2})[/-](\d{2})", text)
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"(\w+ \d{1,2},?\s+\d{4})", text)
    return m.group(1) if m else None
