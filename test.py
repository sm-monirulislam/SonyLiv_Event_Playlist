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

        # ----------------------------
        # Time
        # ----------------------------
        now = datetime.now(BD_TIME)

        last_updated_playlist = now.strftime("%Y-%m-%d %H:%M:%S")
        last_updated_json = now.strftime("%I:%M:%S %p %d-%m-%Y")

        total_matches = len(matches)

        # Live Match Count
        live_match = sum(
            1 for m in matches
            if str(m.get("status", "")).lower() == "live"
        )

        # ----------------------------
        # JSON Output
        # ----------------------------
        output_json = {
            "name": "SonyLiv Match Data",
            "owner": "Monirul Islam",
            "telegram": "https://t.me/monirul_Islam_SM",
            "last_update_time": last_updated_json,
            "total_matches": total_matches,
            "live_match": live_match,
            "matches": matches
        }

        with open("sonyLiv_data.json", "w", encoding="utf-8") as f:
            json.dump(output_json, f, indent=4, ensure_ascii=False)

        print("✅ sonyLiv_data.json created")

        # ----------------------------
        # M3U Output
        # ----------------------------
        m3u = f"""#EXTM3U
#=================================
#  Developed by: Monirul Islam
#  Telegram: https://t.me/monirul_Islam_SM
#  Channel: https://t.me/sm_iptv_bd
#  Last Updated: {last_updated_playlist} (BD Time)
#  Channels Count: {total_matches}
#=================================

"""

        for match in matches:
            name = match.get("match_name", "Unknown Match")
            category = match.get("event_category", "Sports")
            logo = match.get("src", "")

            stream = (
                match.get("video_url")
                or match.get("dai_url")
                or match.get("pub_url")
            )

            if not stream:
                continue

            m3u += (
                f'#EXTINF:-1 tvg-logo="{logo}" '
                f'group-title="{category}",{name}\n'
            )
            m3u += f"{stream}\n\n"

        with open("sonyLiv_playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u)

        print("✅ sonyLiv_playlist.m3u created")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    fetch_and_generate()
