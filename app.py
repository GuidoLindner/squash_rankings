from flask import Flask, render_template
import importlib
import os

app = Flask(__name__)

# List of country scripts
COUNTRIES = [
    "Austria", "Belarus", "Bulgaria", "Czechia", "Denmark", "England", "Estonia",
    "Finland", "France", "Germany", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Netherlands", "Norway", "Poland", "Romania", "Russia",
    "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "Wallonia"
]

@app.route("/")
def index():
    all_rankings = {}

    for country in COUNTRIES:
        try:
            module = importlib.import_module(f"scripts.{country}")
            # Each scraper should have a function `get_top5()` returning a list of dicts:
            # [{"rank": 1, "name": "Player Name", "points": 1234}, ...]
            top5 = module.get_top5()
            all_rankings[country] = top5
        except Exception as e:
            print(f"Error loading {country}: {e}")
            all_rankings[country] = []

    return render_template("index.html", rankings=all_rankings)

if __name__ == "__main__":
    app.run(debug=True)
