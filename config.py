import os

DB_PATH = os.environ.get("DATABASE_PATH", "data/recomp.db")

CAL_TARGET  = 2300
PRO_TARGET  = 165
CARB_TARGET = 185
FAT_TARGET  = 75

BASELINES = {
    "vo2_max": 43,
    "resting_hr": 69,
    "hrv_avg": 46,
    "zone2_pace": "11:30",
}

BODY_SCAN_DEFAULTS = {
    "date": "2026-04-28",
    "weight_lb": 161.2,
    "lean_mass_lb": 129.8,
    "skeletal_muscle_lb": 83.8,
    "fat_mass_lb": 31.4,
    "body_fat_pct": 19.5,
    "visceral_fat": 8,
    "waist_hip_ratio": 0.93,
    "bone_mass_lb": 6.4,
    "bmr": 1641,
    "score": 84.9,
    "notes": "GE CS10G · Apr 28 2026 · clothed 161.2 lb · baseline scan",
}

QUICK_FOODS = {
    "turkey":      {"food": "HEB Honey Smoked Turkey", "servingSize": 2,   "servingUnit": "oz",        "cal": 70,  "pro": 10,  "carb": 3,  "fat": 1.5, "sugar": 3,  "fiber": 0},
    "sourdough":   {"food": "Sourdough Bread",          "servingSize": 1,   "servingUnit": "slice",     "cal": 150, "pro": 5,   "carb": 29, "fat": 1,   "sugar": 0,  "fiber": 1},
    "cheddar":     {"food": "Tillamook Cheddar",         "servingSize": 1,   "servingUnit": "slice",     "cal": 110, "pro": 6,   "carb": 1,  "fat": 9,   "sugar": 0,  "fiber": 0},
    "skyr":        {"food": "Icelandic Skyr Yogurt (Lemon)", "servingSize": 1, "servingUnit": "container", "cal": 160, "pro": 11,  "carb": 12, "fat": 7,   "sugar": 9,  "fiber": 0},
    "banana":      {"food": "Banana (medium)",           "servingSize": 1,   "servingUnit": "piece",     "cal": 105, "pro": 1,   "carb": 27, "fat": 0,   "sugar": 14, "fiber": 3},
    "mandarin":    {"food": "Mandarin (small)",          "servingSize": 1,   "servingUnit": "piece",     "cal": 40,  "pro": 1,   "carb": 10, "fat": 0,   "sugar": 8,  "fiber": 1},
    "carrots":     {"food": "Baby Carrots",              "servingSize": 7,   "servingUnit": "oz",        "cal": 85,  "pro": 2,   "carb": 20, "fat": 0,   "sugar": 9,  "fiber": 5},
    "pbcrackers":  {"food": "PB Cracker Packet",         "servingSize": 1,   "servingUnit": "packet",    "cal": 190, "pro": 3,   "carb": 24, "fat": 9,   "sugar": 5,  "fiber": 1},
    "whey":        {"food": "Thorne Whey Protein Isolate", "servingSize": 1, "servingUnit": "scoop",     "cal": 100, "pro": 21,  "carb": 4,  "fat": 1,   "sugar": 2,  "fiber": 1},
    "cottage":     {"food": "Cottage Cheese 2%",         "servingSize": 0.5, "servingUnit": "cup",       "cal": 110, "pro": 14,  "carb": 5,  "fat": 3,   "sugar": 3,  "fiber": 0},
    "miraclewhip": {"food": "Miracle Whip",              "servingSize": 1,   "servingUnit": "tbsp",      "cal": 35,  "pro": 0,   "carb": 2,  "fat": 2,   "sugar": 1,  "fiber": 0},
}
