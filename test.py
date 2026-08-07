import json
import requests


def fetch_and_generate():
    api_url = "https://raw.githubusercontent.com/drmlive/sliv-live-events/refs/heads/main/sonyliv.json"

    try:
        # API theke data fetch kora
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        matches = data.get("matches", [])

        # 1. Output JSON File Make Kora
        with open("matches.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print("✅ 'matches.json' file successfully created!")

        # 2. M3U Playlist File Make Kora
        m3u_content = "#EXTM3U\n\n"

        for match in matches:
            match_name = match.get("match_name", "Unknown Match")
            category = match.get("event_category", "Sports")
            logo = match.get("src", "")
            # Streaming link (video_url / dai_url / pub_url)
            stream_url = (
                match.get("video_url")
                or match.get("dai_url")
                or match.get("pub_url")
            )

            if stream_url:
                # M3U Header Entry
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}", {match_name}\n'
                m3u_content += f"{stream_url}\n\n"

        with open("playlist.m3u8", "w", encoding="utf-8") as m3u_file:
            m3u_file.write(m3u_content)
        print("✅ 'playlist.m3u8' file successfully created!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from API: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    fetch_and_generate()
