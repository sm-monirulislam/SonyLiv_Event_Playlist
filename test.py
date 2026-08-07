import json
import requests
from datetime import datetime, timedelta, timezone

API_URL = "https://raw.githubusercontent.com/drmlive/sliv-live-events/refs/heads/main/sonyliv.json"

# Bangladesh Time (UTC+6)
BD_TIME = timezone(timedelta(hours=6))


def fetch_and_generate():
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()

        matches = data.get("matches", [])
        processed_matches = []

        # Process matches
        for match in matches:
            item = dict(match)

            # Convert isLive -> status
            is_live = item.pop("isLive", False)
            item["status"] = "Live" if is_live else "Upcoming"

            # Rename video_url -> stream_link
            item["stream_link"] = item.pop("video_url", "")

            # Remove unwanted fields
            item.pop("dai_url", None)
            item.pop("pub_url", None)

            processed_matches.append(item)

        # Bangladesh Time
        now = datetime.now(BD_TIME)

        playlist_time = now.strftime("%Y-%m-%d %H:%M:%S")
        json_time = now.strftime("%I:%M:%S %p %d-%m-%Y")

        total_matches = len(processed_matches)
        live_match = sum(
            1 for match in processed_matches
            if match["status"] == "Live"
        )

        # ==========================
        # JSON FILE
        # ==========================
        json_output = {
            "name": "SonyLiv Match Data",
            "owner": "Monirul Islam",
            "telegram": "https://t.me/monirul_Islam_SM",
            "last_update_time": json_time,
            "total_matches": total_matches,
            "live_match": live_match,
            "matches": processed_matches
        }

        with open("sonyLiv_data.json", "w", encoding="utf-8") as f:
            json.dump(json_output, f, indent=4, ensure_ascii=False)

        print("✅ sonyLiv_data.json created.")

        # ==========================
        # M3U PLAYLIST (Only Live Matches)
        # ==========================
        playlist = f"""#EXTM3U
#=================================
#  Developed by: Monirul Islam
#  Telegram: https://t.me/monirul_Islam_SM
#  Channel: https://t.me/sm_iptv_bd
#  Last Updated: {playlist_time} (BD Time)
#  Channels Count: {live_match}
#=================================

"""

        for match in processed_matches:

            # Only Live Matches
            if match["status"] != "Live":
                continue

            stream = match.get("stream_link", "")

            if not stream:
                continue

            name = match.get("match_name", "Unknown Match")
            category = match.get("event_category", "Sports")
            logo = match.get("src", "")

            playlist += (
                f'#EXTINF:-1 tvg-id="{match.get("contentId","")}" '
                f'tvg-name="{name}" '
                f'tvg-logo="{logo}" '
                f'group-title="{category}",{name}\n'
            )
            playlist += f"{stream}\n\n"

        with open("sonyLiv_playlist.m3u", "w", encoding="utf-8") as f:
            f.write(playlist)

        print("✅ sonyLiv_playlist.m3u created.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    fetch_and_generate()
