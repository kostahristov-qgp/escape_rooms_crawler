import json
import re
from datetime import date

from curl_cffi import requests
from jsonpath_ng import parse

from base import RoomsCrawler


class BioxcapeCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://bioxcape.com/play/2025-03-12",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=2027603972#gid=2027603972",
            "room": "Bioxcape-ОбразователнаЕскейпСтая",
        }
    ]

    USE_DRIVER = False

    def scrape_room(self):
        today = date.today()
        date_str = today.strftime("%Y-%m-%d")

        base_url = "https://bioxcape.com/play/"
        url = base_url + date_str

        response = requests.get(url, impersonate="chrome")

        html_string = response.text

        match = re.search(r"window\.__remixContext\s*=\s*({.*?});</script>", html_string, re.DOTALL)
        if match:
            data = json.loads(match.group(1))

        jsonpath_expr = parse("$..timeslots")
        timeslots = [match.value for match in jsonpath_expr.find(data)][0]

        for timeslot in timeslots:
            slots = timeslot["slots"]
            for slot in slots:
                is_available = slot["available"]
                datetime_str = slot["link"]
                date_str, time = datetime_str.split("/")

                entry = {
                    "date": date_str,
                    "time": time,
                    "available": is_available,
                }

                self.entries.append(entry)


if __name__ == "__main__":
    crawler = BioxcapeCrawler("bioxcape")
    crawler.run()
