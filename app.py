from flask import Flask
from db import init_db
from routes import all_blueprints
from config import QUICK_FOODS

app = Flask(__name__)
app.secret_key = "recomp-secret-change-in-prod"

for bp in all_blueprints:
    app.register_blueprint(bp)

@app.context_processor
def inject_globals():
    return {"quick_foods": QUICK_FOODS}

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
