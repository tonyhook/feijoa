from tools.llm import ask_llm


def extract_movie_title(user_query: str) -> str | None:
    """
    Returns the movie title if the query is asking about a movie release date,
    otherwise returns None.
    Uses LLM for both intent detection and title extraction in one shot.
    """
    prompt = f"""Extract the movie title if the user is asking about a movie's release date, OR if the user typed only a movie title with no other context.
Return NONE if the user is asking about something else (e.g. plot, reviews, cast, quality) or if no movie is mentioned.
Return ONLY the movie title or NONE.

Examples:
- "Moana" → Moana
- "When is Moana 2 released?" → Moana 2
- "Moana release date" → Moana
- "Is Moana a good film?" → NONE
- "Who directed Moana?" → NONE
- "What is the capital of France?" → NONE

Query: {user_query}"""
    ans = ask_llm(prompt).strip()
    return None if ans.upper() == "NONE" else ans
