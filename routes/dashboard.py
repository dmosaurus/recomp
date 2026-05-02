from flask import Blueprint, render_template, g
from db import get_db
from models import get_weekly_summary, get_latest_body_scan
from config import BASELINES

bp = Blueprint("dashboard", __name__)

@bp.before_request
def open_db(): g.db = get_db()

@bp.teardown_request
def close_db(e): g.db.close()

@bp.route("/")
def index():
    return render_template("dashboard.html",
        summary=get_weekly_summary(g.db),
        scan=get_latest_body_scan(g.db),
        baselines=BASELINES,
    )
