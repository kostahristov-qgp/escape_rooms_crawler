from base import RoomsCrawler


class EndorphingamesCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://endorphingames.bg/bg/rooms/blue-lab/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=2067870407#gid=2067870407",
            "room": "ЕндорфинГеймс-СинятаЛаборатория",
        }
    ]

    NEXT_DAYS_SELECTOR = "a.next-week.text-right"

    DATES_TABLE_SELECTOR = "table.table"

    AVAILABLE_SLOTS_SELECTOR = 'th[data-time-slot-status="free"]'
    BOOKED_SLOTS_SELECTOR = 'th[data-time-slot-status="booked"]'
    DISABLED_SLOTS_SELECTOR = 'th[data-time-slot-status="blocked"]'

    DATE_SELECTOR = "td.table-titel"

    AVAILABLE_SLOTS_ATTR = BOOKED_SLOTS_ATTR = DISABLED_SLOTS_ATTR = DATE_ATTR = "innerText"

    def correct_date(self, date):
        date = date.split(" ")[-1]
        date = "-".join(reversed(date.split(".")))
        date = date.strip()
        return date

    def scrape_room(self):
        dates_table = self.safe_find(self.DATES_TABLE_SELECTOR, return_element=True, multiple=True)

        for td in dates_table:
            date = self.safe_find(self.DATE_SELECTOR, attr=self.DATE_ATTR, search_element=td)
            date = self.correct_date(date)
            if not date:
                continue
            available = self.safe_find(self.AVAILABLE_SLOTS_SELECTOR, attr=self.AVAILABLE_SLOTS_ATTR, search_element=td, multiple=True)
            booked = self.safe_find(self.BOOKED_SLOTS_SELECTOR, attr=self.BOOKED_SLOTS_ATTR, search_element=td, multiple=True)
            disabled = self.safe_find(self.DISABLED_SLOTS_SELECTOR, attr=self.DISABLED_SLOTS_ATTR, search_element=td, multiple=True)

            entry = {
                "date": date,
            }

            for item in available:
                entry = {"date": date, "time": item, "available": True}
                self.entries.append(entry)

            for item in booked:
                entry = {"date": date, "time": item, "available": False, "disabled": False}
                self.entries.append(entry)

            for item in disabled:
                entry = {"date": date, "time": item, "available": False, "disabled": True}
                self.entries.append(entry)

    def get_disabled_slots(self):
        unique_entries = []  # keep unique entries across all iterations
        for x in range(5):
            self.scrape_room()

            # check if new unique entries were added
            has_new, unique_entries = self.has_new_unique_entries(unique_entries)
            if not has_new:
                break

            next_button = self.safe_find(self.NEXT_DAYS_SELECTOR, return_element=True)
            if next_button:
                self.make_click(next_button)
                self.sleep_random(5, 10)

        self.entries = unique_entries


if __name__ == "__main__":
    crawler = EndorphingamesCrawler("endorphingames")
    crawler.run()
