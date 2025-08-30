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
    "Austria": {
        "men": "https://www.squash.or.at/ranglisten/ranking/",
        "women": "https://www.squash.or.at/ranglisten/ranking/"
    },
    "Belarus": {
        "men": "https://rankedin.com/en/ranking/10950?rankingType=1&ageGroup=1" 
        # No women’s rankings link
    },
    "Bulgaria": {
        "men": "https://rankedin.com/en/organisation/ranking/9707"
        # No women's ranking link
    },
    "Czechia": {
        "men": "https://czechsquash.cz/zebricek/dospeli/muzi/#zebricek",
        "women": "https://czechsquash.cz/zebricek/dospeli/zeny/#zebricek"
    },
    "Denmark": {
        "men": "https://www.squashportalen.dk/reports/dk-rankings",
        "women": "https://www.squashportalen.dk/reports/dk-rankings"
    },
    "England": {
        "men": "https://app.squashlevels.com/players?ranking=-1&club=all&county=all&country=1&show=last6m&matchtype=all&playercat=all&playertype=all&filter_reset=0",
        "women": "https://app.squashlevels.com/players?ranking=-1&club=all&county=all&country=1&show=last6m&matchtype=all&playercat=all&playertype=2&filter_reset=0"
    },
    "Estonia": {
        "men": "https://squash.ee/edetabelid/",
        "women": "https://squash.ee/edetabelid/#n-liiga"
    },
    "Finland": {
        "men": "https://clublocker.com/organizations/10142/rankings/9/current/2/0",
        "women": "https://clublocker.com/organizations/10142/rankings/9/current/1/0"
    },
    "France": {
        "men": "https://www.squashnet.fr/classements",
        "women": "https://www.squashnet.fr/classements"
    },
    "Germany": {
        "men": "https://www.squash-liga.com/bundesliga/rangliste/herren.html",
        "women": "https://www.squash-liga.com/bundesliga/rangliste/damen.html"
    },
    "Hungary": {
        "men": "https://verseny.squash.hu/ranklist/man",
        "women": "https://verseny.squash.hu/ranklist/woman"
    },
    "Ireland": {
        "men": "https://www.squashireland.ie/tournaments-competitions/rankings/",
        "women": "https://www.squashireland.ie/tournaments-competitions/rankings/"
    },
    "Italy": {
        "men": "https://www.federsquash.it/attivita-federale/classifiche-federali/ranking-maschile/ranking.html",
        "women": "https://www.federsquash.it/attivita-federale/classifiche-federali/ranking-femminile/ranking.html"
    },
    "Latvia": {
        "men": "https://www.squash.lv/rankings?utf8=%E2%9C%93&rank_type=M&player_name=",
        "women": "https://www.squash.lv/rankings?utf8=%E2%9C%93&rank_type=F&player_name="
    },
    "Lithuania": {
        "men": "https://squash.lt/reitingas/",
        "women": "https://squash.lt/reitingas/"
    },
    "Luxembourg": {
        "men": "https://www.fsl.lu/index.php/ranking/rankings-2024-2025/",
        "women": "https://www.fsl.lu/index.php/ranking/rankings-2024-2025/"
    },
    "Netherlands": {
        "men": "https://sbn.squashlevels.com/speelsterkte_ranking",
        "women": "https://sbn.squashlevels.com/speelsterkte_ranking?page=sbn_rankings&asof=1754002800&county=all&playercat=all&playertype=2&filter_reset=0"
    },
    "Norway": {
        "men": "https://rankedin.com/nl/organisation/ranking/115/norges-squashforbund",
        "women": "https://rankedin.com/nl/organisation/ranking/115/norges-squashforbund?rankingType=2&ageGroup=13&week=35&year=2025"
    },
    "Poland": {
        "men": "https://bo5.pl/ranking/pzsq/open",
        "women": "https://bo5.pl/ranking/pzsq/damski"
    },
    "Portugal": {
        "men": "https://fnsquash.pt/home-2/competicao/ranking-nacional-masculino/",
        "women": "https://fnsquash.pt/home-2/competicao/ranking-nacional-feminino/"
    },
    "Romania": {
        "men": "https://frsquash.ro/clasament-2/punctaj-seniori/",
        "women": "https://frsquash.ro/clasament-2/punctaj-seniori/"
    },
    "Russia": {
        "men": "https://russiansquash.ru/rating/",
        "women": "https://russiansquash.ru/rating/"
    },
    "Serbia": {
        "men": "http://skvos.rs/rngl/rngl-muskarci/",
        "women": "http://skvos.rs/rngl-zene/"
    },
    "Slovakia": {
        "men": "https://www.squashtour.sk/rebricek/dospeli/muzi/#zebricek",
        "women": "https://www.squashtour.sk/rebricek/dospeli/zeny/#zebricek"
    },
    "Slovenia": {
        "men": "https://squash.si/slovenska-jakostna-lestvica/lestvica-m/",
        "women": "https://squash.si/slovenska-jakostna-lestvica/lestvica-m/"
    },
    "Spain": {
        "men": "https://realfederaciondesquash.com/rankings/",
        "women": "https://realfederaciondesquash.com/rankings/"
    },
    "Sweden": {
        "men": "https://squash.se/ranking/?_gl=1*1x5fiup*_ga*MjEwMjkxNTcwOS4xNzUzNjMyMjE5*_ga_QVHD4R1NQ5*czE3NTM2MzIyMTkkbzEkZzAkdDE3NTM2MzIyMTkkajYwJGwwJGgw",
        "women": "https://squash.se/ranking/?_gl=1*1x5fiup*_ga*MjEwMjkxNTcwOS4xNzUzNjMyMjE5*_ga_QVHD4R1NQ5*czE3NTM2MzIyMTkkbzEkZzAkdDE3NTM2MzIyMTkkajYwJGwwJGgw"
    },
    "Switzerland": {
        "men": "https://my.squash.ch/ranking",
        "women": "https://my.squash.ch/ranking"
    },
    "Ukraine": {
        "men": "https://squash.ua/en/rejting",
        "women": "https://squash.ua/en/rejting"
    },
    "Wallonia": {
        "men": "https://www.sportyhq.com/ranking/group/2005",
        "women": "https://www.sportyhq.com/ranking/group/2004"
    },
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
