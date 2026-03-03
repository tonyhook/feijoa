from kernel.clarification import Clarification, ClarificationOption
from kernel.result import Result
from kernel.tool import Tool
from tools.imdb import get_release_dates, search_movie, search_movies
from tools.movies_anywhere import get_release_date as ma_get_release_date


class MovieReleaseDateTool(Tool):

    def dry_run(self, **kwargs) -> Result:
        return Result(ok = True, output = {})

    def run(self, **kwargs) -> Result:
        title = kwargs.get("title", "")
        imdb_id = kwargs.get("imdb_id")   # pre-resolved from clarification
        year = kwargs.get("year")

        if imdb_id:
            # User already chose — skip search, use resolved movie directly
            movie = {"id": imdb_id, "title": title, "year": year}
        else:
            # Check for ambiguity: multiple movies with the exact same title
            candidates = search_movies(title)

            if len(candidates) > 1:
                return Result(
                    ok = True,
                    output = {},
                    clarification = Clarification(
                        question = f"Multiple movies named '{title}' found. Which one do you mean?",
                        options = [
                            ClarificationOption(label = f"{m['title']} ({m['year']})", data = m)
                            for m in candidates
                        ],
                    ),
                )

            movie = candidates[0] if candidates else search_movie(title)
            if not movie:
                return Result(ok = False, output = {"answer": f"Could not find '{title}' on IMDB."})

        confirmed_title = movie["title"]
        confirmed_year = movie["year"]

        # Rule 1: try Movies Anywhere first
        date = ma_get_release_date(confirmed_title, confirmed_year)
        if date:
            return Result(ok = True, output = {"answer": date})

        # Rule 2 & 3: fall back to IMDB — US date, then earliest worldwide
        dates = get_release_dates(movie["id"])
        date = dates.get("US") or dates.get("earliest")
        if not date:
            return Result(ok = False, output = {"answer": f"Release date not found for '{confirmed_title}'."})

        return Result(ok = True, output = {"answer": date})
