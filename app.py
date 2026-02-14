from pathlib import Path
import json

from flask import Flask, render_template

BASE_DIR = Path(__file__).resolve().parent
LINKS_FILE = BASE_DIR / "links.json"

app = Flask(__name__)


def load_links() -> list[dict]:
    """Load link configuration from links.json.

    The file is a list of objects with at least:
    - label: Text shown on the button
    - url:   Target URL
    - description (optional): Smaller text under the label
    - order (optional): For manual ordering; lower comes first
    """
    try:
        with LINKS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return sorted(data, key=lambda item: item.get("order", 0))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


@app.route("/")
def index():
    links = load_links()
    page_title = "Rhythmic AI: Links"
    tagline = "Follow the flow of Rhythmic AI."
    return render_template("index.html", links=links, page_title=page_title, tagline=tagline)


if __name__ == "__main__":  # For local debugging only
    app.run(host="0.0.0.0", port=8000, debug=True)
