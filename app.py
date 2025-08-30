from flask import Flask, render_template
import importlib
import os, time, threading

app = Flask(__name__)

COUNTRIES = [
    "Austria", "Belarus", "Bulgaria", "Czechia", "Denmark", "England", "Estonia",
    "Finland", "France", "Germany", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russia",
    "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "Wallonia"
]

RANKING_LINKS = {
    # Keep your existing RANKING_LINKS dictionary here...
}

# ---- CACHE ----
CACHE = {"rankings": {}, "last_updated": None}
CACHE_TTL = 60 * 60  # 1 hour

def fetch_all_rankings():
    all_rankings = {}

    for country in COUNTRIES:
        rankings = {"men": [], "women": []}

        try:
            men_module = importlib.import_module(f"scripts.{country}")
            rankings["men"] = men_module.get_top5()
        except Exception as e:
            print(f"Error loading men’s rankings for {country}: {e}")

        try:
            women_module = importlib.import_module(f"scripts.{country}_w")
            rankings["women"] = women_module.get_top5()
        except Exception as e:
            print(f"No women’s rankings for {country}")

        links = RANKING_LINKS.get(country, {})
        all_rankings[country] = {
            "men": rankings["men"],
            "women": rankings["women"],
            "men_link": links.get("men"),
            "women_link": links.get("women"),
        }

    return all_rankings

def refresh_cache_periodically():
    """Background thread that refreshes rankings every CACHE_TTL seconds."""
    while True:
        try:
            print("Refreshing rankings in background...")
            CACHE["rankings"] = fetch_all_rankings()
            CACHE["last_updated"] = time.time()
        except Exception as e:
            print(f"Error refreshing rankings: {e}")
        time.sleep(CACHE_TTL)

@app.route("/")
def index():
    return render_template(
        "index.html",
        rankings=CACHE["rankings"],
        last_updated=time.strftime(
            "%Y-%m-%d %H:%M:%S", time.gmtime(CACHE["last_updated"])
        )
    )

if __name__ == "__main__":
    # --- Preload rankings at startup ---
    print("Fetching initial rankings before serving...")
    CACHE["rankings"] = fetch_all_rankings()
    CACHE["last_updated"] = time.time()

    # --- Start background refresh thread ---
    t = threading.Thread(target=refresh_cache_periodically, daemon=True)
    t.start()

    # --- Start Flask server ---
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
