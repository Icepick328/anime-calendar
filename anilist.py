import requests
import time

ANILIST_URL = "https://graphql.anilist.co"

QUERY = """
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    airingSchedules(notYetAired: true, sort: TIME) {
      airingAt
      episode
      media {
        id
        title {
          romaji
          english
        }
        genres
        siteUrl
        season
        seasonYear
        status
        coverImage {
          large
        }
      }
    }
  }
}
"""

def fetch_airing_schedule(pages=5):
    results = []

    for page in range(1, pages + 1):
        variables = {"page": page, "perPage": 50}

        response = requests.post(
            ANILIST_URL,
            json={"query": QUERY, "variables": variables},
        )

        data = response.json()["data"]["Page"]["airingSchedules"]

        if not data:
            break

        results.extend(data)
        time.sleep(0.2)

    return results
