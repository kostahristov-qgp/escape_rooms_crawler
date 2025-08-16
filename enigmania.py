from datetime import datetime
from zoneinfo import ZoneInfo

from base import RoomsCrawler


class EnigmaniaCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://www.enigmania.bg/bg_BG/experiment#bookvisit",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=13112530#gid=13112530",
            "room": "Енигмания-Vodoo",
        },
        {
            "url": "https://www.enigmania.bg/bg_BG/voodoo#bookvisit",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1258727861#gid=1258727861",
            "room": "Енигмания - Експеримента",
        },
    ]

    NEXT_DAYS_SELECTOR = ".right_arrow"

    def scrape_room(self):
        timestamp_els = self.safe_find("li[data-stamp]:not(.passed)", return_element=True, multiple=True)

        for timestamp_el in timestamp_els:
            timestamp_class = timestamp_el.get_attribute("class")
            if "booked_time" in timestamp_class:
                is_available = False
            elif "free_time" in timestamp_class:
                is_available = True

            timestamp = timestamp_el.get_attribute("data-stamp")

            dt = datetime.fromtimestamp(int(timestamp), tz=ZoneInfo("Europe/Sofia"))
            date = dt.strftime("%Y-%m-%d")
            time = dt.strftime("%H:%M")

            entry = {
                "date": date,
                "time": time,
                "available": is_available,
            }

            self.entries.append(entry)


crawler = EnigmaniaCrawler("enigmania")


if __name__ == "__main__":
    crawler.run()
