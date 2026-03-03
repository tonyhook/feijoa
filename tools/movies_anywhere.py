import re
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


_DATE_RE = re.compile(r"[A-Z][a-z]+ \d{1,2}, \d{4}")


def _make_slug(title: str, year: int) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    return f"{slug}-{year}"


def _parse_date(text: str) -> str | None:
    m = _DATE_RE.search(text)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(0), "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def get_release_date(title: str, year: int) -> str | None:
    """
    Tries to find the movie on Movies Anywhere and return its release date (YYYY-MM-DD).
    Returns None if the movie is not listed or the page times out.
    """
    slug = _make_slug(title, year)
    url = f"https://moviesanywhere.com/movie/{slug}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until = "load", timeout = 10000)
            page.wait_for_timeout(1000)

            body_text = page.inner_text("body")
            browser.close()

            if "Release Date:" not in body_text:
                return None

            idx = body_text.index("Release Date:")
            snippet = body_text[idx + len("Release Date:"):].strip().split("\n")[0].strip()
            return _parse_date(snippet)

    except PlaywrightTimeout:
        return None
