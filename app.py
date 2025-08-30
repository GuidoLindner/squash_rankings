from flask import Flask, render_template
import json, os, time

app = Flask(__name__)

RANKINGS_FILE = "rankings.json"

@app.route("/")
def index():
    rankings = {}
    last_updated = None

    if os.path.exists(RANKINGS_FILE):
        with open(RANKINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            rankings = data.get("rankings", {})
            timestamp = data.get("last_updated")
            if timestamp:
                last_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))

    return render_template("index.html", rankings=rankings, last_updated=last_updated)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
