from flask import Flask, render_template
import importlib

app = Flask(__name__)

# List of country scripts (base names without _w)
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
        rankings = {"men": [], "women": []}

        # Try men's rankings
        try:
            men_module = importlib.import_module(f"scripts.{country}")
            rankings["men"] = men_module.get_top5()
        except Exception as e:
            print(f"Error loading men’s rankings for {country}: {e}")

        # Try women's rankings
        try:
            women_module = importlib.import_module(f"scripts.{country}_w")
            rankings["women"] = women_module.get_top5()
        except Exception as e:
            # It's normal some countries don’t have women’s rankings
            print(f"No women’s rankings for {country}")

        all_rankings[country] = rankings

    return render_template("index.html", rankings=all_rankings)

if __name__ == "__main__":
    app.run(debug=True)
