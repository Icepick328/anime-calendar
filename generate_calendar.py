from anilist import fetch_airing_schedule
from calendar_builder import build_event, create_calendar
from config import LOOKAHEAD_DAYS
import datetime
import pytz
import os

def pick_title(media):
    return media["title"]["english"] or media["title"]["romaji"]

def is_dub(media):
    # heuristic: AniList doesn't reliably tag dub dates
    # we approximate using "has English title + popularity + streaming hints"
    return "english" in (media["title"]["english"] or "").lower()

def build_description(media):
    genres = ", ".join(media.get("genres", []))

    return f"""Genres: {genres}
AniList: {media['siteUrl']}
Season: {media.get('season', '')} {media.get('seasonYear', '')}
"""

def main():
    schedule = fetch_airing_schedule()

    sub_events = []
    dub_events = []

    now = datetime.datetime.utcnow()

    for item in schedule:
        media = item["media"]
        title = pick_title(media)

        event = build_event(
            title,
            item["episode"],
            item["airingAt"],
            build_description(media),
            media["siteUrl"]
        )

        # SUB calendar (always)
        sub_events.append(event)

        # DUB calendar (best-effort heuristic)
        if media.get("status") == "RELEASING" and media.get("coverImage"):
            dub_event = build_event(
                title + " (Dub Est.)",
                item["episode"],
                item["airingAt"] + 14 * 86400,  # typical 2-week delay guess
                build_description(media) + "\nDub: estimated delay ~2 weeks",
                media["siteUrl"]
            )
            dub_events.append(dub_event)

    sub_calendar = create_calendar(sub_events)
    dub_calendar = create_calendar(dub_events)

    os.makedirs("docs", exist_ok=True)

    with open("docs/sub.ics", "w") as f:
        f.writelines(sub_calendar.serialize_iter())

    with open("docs/dub.ics", "w") as f:
        f.writelines(dub_calendar.serialize_iter())


if __name__ == "__main__":
    main()
