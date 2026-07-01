from anilist import fetch_airing_schedule
from calendar_builder import build_event, create_calendar
import os

def pick_title(media):
    return media["title"]["english"] or media["title"]["romaji"]

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

        sub_events.append(event)

        # Dub (estimated)
        dub_events.append(
            build_event(
                title + " (Dub Est.)",
                item["episode"],
                item["airingAt"] + 14 * 86400,
                build_description(media),
                media["siteUrl"]
            )
        )

    os.makedirs("docs", exist_ok=True)

    sub_calendar = create_calendar(sub_events)
    dub_calendar = create_calendar(dub_events)

    with open("docs/sub.ics", "w", encoding="utf-8") as f:
        f.write(sub_calendar.serialize())

    with open("docs/dub.ics", "w", encoding="utf-8") as f:
        f.write(dub_calendar.serialize())

if __name__ == "__main__":
    main()
