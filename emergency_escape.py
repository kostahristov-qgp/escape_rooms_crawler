import re
from datetime import date, datetime

from base import RoomsCrawler


class Emergency_escapeCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://emergency-escape.com/room/nasledstvoto-na-masonite",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=660700199#gid=660700199",
            "room": "EmergencyEscape-НаследствотонаМасоните",
        },
        {
            "url": "https://emergency-escape.com/room/istoria-na-igrachkite",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=726272445#gid=726272445",
            "room": "EmergencyEscape - История на Играчките",
        },
    ]

    NEXT_DAYS_SELECTOR = 'span.date-navigation-right[aria-disabled="false"]'

    AVAILABLE_SLOTS_SELECTOR = ".table-calendar-day td.free"
    DISABLED_SLOTS_SELECTOR = '//*[@class="table-calendar-day"]//*[@class="reserved"][not(text()=" ПО ЗАПИТВАНЕ")]'

    DATES_SELECTOR = ".table-calendar-main th"
    DATES_TABLE_SELECTOR = ".table-calendar-day"

    DATES_ATTR = AVAILABLE_SLOTS_ATTR = DISABLED_SLOTS_ATTR = "innerText"

    def scrape_room(self):
        date_times_table = self.safe_find(self.DATES_TABLE_SELECTOR, return_element=True, multiple=True)
        dates = self.safe_find(self.DATES_SELECTOR, attr=self.DATES_ATTR, multiple=True)

        dates = [self.correct_date(date) for date in dates if date.strip()]

        all_disabled_slots = self.safe_find(self.DISABLED_SLOTS_SELECTOR, attr=self.DISABLED_SLOTS_ATTR, multiple=True)
        all_available_slots = self.safe_find(self.AVAILABLE_SLOTS_SELECTOR, attr=self.AVAILABLE_SLOTS_ATTR, multiple=True)

        all_times = list(set(all_disabled_slots + all_available_slots))

        all_times = [time for time in all_times if re.match(r"\d{2}:\d{2}", time)]

        all_times.sort(key=lambda x: datetime.strptime(x, "%H:%M"))

        for day_index, td in enumerate(date_times_table):
            saved_date = dates[day_index]

            if datetime.strptime(saved_date, "%Y-%m-%d").date() < date.today():
                continue

            all_day_slots = self.safe_find("td", attr="innerText", search_element=td, multiple=True)
            all_day_slots_classes = self.safe_find("td", attr="class", search_element=td, multiple=True)

            for item_index, item in enumerate(all_day_slots):
                entry = None
                if re.match(r"\d{2}:\d{2}", item) and "free" in all_day_slots_classes[item_index]:
                    entry = {"date": saved_date, "time": item, "available": True}
                elif "ПО ЗАПИТВАНЕ" in item:
                    entry = {"date": saved_date, "time": all_times[item_index], "available": False, "disabled": True}
                elif "ЗАПАЗЕН" in item:
                    entry = {"date": saved_date, "time": all_times[item_index], "available": False, "disabled": False}

                if entry:
                    self.entries.append(entry)

    def correct_date(self, date):
        date = date.split("\n")[-1].split(" ")[0].strip()
        date = "-".join(reversed(date.split(".")))
        date = date.strip()
        return date


crawler = Emergency_escapeCrawler("emergency_escape")


if __name__ == "__main__":
    crawler.run()
