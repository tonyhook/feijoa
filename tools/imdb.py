import re
import requests
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

_DATE_RE = re.compile(r"[A-Z][a-z]+ \d{1,2}, \d{4}")


def _parse_date(text: str) -> str | None:
    m = _DATE_RE.search(text)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(0), "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def _fetch_suggestions(title: str) -> list[dict]:
    url = f"https://v2.sg.media-imdb.com/suggestion/{title[0].lower()}/{quote(title)}.json"
    r = requests.get(url, headers = HEADERS, timeout = 10)
    r.raise_for_status()
    return [
        {"id": x["id"], "title": x["l"], "year": x.get("y")}
        for x in r.json().get("d", [])
        if x.get("qid") == "movie"
    ]


def search_movie(title: str) -> dict | None:
    """Returns the single best IMDB match for a title."""
    movies = _fetch_suggestions(title)
    return movies[0] if movies else None


def search_movies(title: str) -> list[dict]:
    """
    Returns all IMDB movies whose title exactly matches the query (case-insensitive).
    Used to detect ambiguity (e.g. 'Moana' matching both 2016 and 2026 versions).
    """
    query_lower = title.strip().lower()
    return [m for m in _fetch_suggestions(title) if m["title"].lower() == query_lower]


def get_release_dates(movie_id: str) -> dict:
    """
    Scrapes IMDB releaseinfo page for a movie by IMDB ID.
    Returns dict with keys:
      "US"       - US theatrical release date (YYYY-MM-DD), or None
      "earliest" - earliest worldwide release date (YYYY-MM-DD), or None
    """
    url = f"https://www.imdb.com/title/{movie_id}/releaseinfo"
    r = requests.get(url, headers = HEADERS, timeout = 10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select('[data-testid="list-item"]')

    # Collect all (country, date, qualifier) tuples
    entries: list[tuple[str, str, str]] = []
    for item in items:
        parts = [p.strip() for p in item.get_text(" | ", strip = True).split("|")]
        if len(parts) < 2:
            continue
        country = parts[0]
        date = _parse_date(parts[1])
        if not date:
            continue
        qualifier = parts[2] if len(parts) > 2 else ""
        entries.append((country, date, qualifier))

    # US theatrical: no qualifier = wide release; fall back to any US date
    us_wide = [date for country, date, q in entries if country == "United States" and not q]
    us_any  = [date for country, date, q in entries if country == "United States"]
    us_date = min(us_wide) if us_wide else (min(us_any) if us_any else None)

    all_dates = [date for _, date, _ in entries]
    earliest = min(all_dates) if all_dates else None

    return {"US": us_date, "earliest": earliest}
