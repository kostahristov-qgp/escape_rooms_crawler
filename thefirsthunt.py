from selenium.webdriver.support.ui import Select

from base import RoomsCrawler


class ThefirsthuntCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://thefirsthunt.bg/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=2107781132#gid=2107781132",
            "room": "TheFirstHunt-TheFirstHunt",
        },
    ]

    def scrape_room(self):
        dropdown = self.safe_find("select.ahbfield_service", return_element=True)
        if not dropdown:
            self.logger.warning("No dropdown to select number of visitors found")
            return
        Select(dropdown).select_by_value("120")
        self.sleep_random(3, 5)
        days_selector = "[data-month]"
        days = self.safe_find(days_selector, return_element=True, multiple=True)

        days = days[: self.max_days]
        for day_index, day in enumerate(days):
            days = self.safe_find(days_selector, return_element=True, multiple=True)
            days = days[: self.max_days]
            self.make_click(days[day_index])
            self.sleep_random(7, 12)

            time_els = self.safe_find(".availableslot>a[d]", return_element=True, multiple=True)

            for time_el in time_els:
                date = time_el.get_attribute("d")
                time = time_el.get_attribute("innerText")

                entry = {
                    "date": date,
                    "time": time,
                    "available": True,
                }

                self.entries.append(entry)

            not_available_slots = self.safe_find(".slots>div[h1]", attr="innerText", multiple=True)

            for slot in not_available_slots:
                entry = {
                    "date": date,
                    "time": slot,
                    "available": False,
                }

                self.entries.append(entry)


if __name__ == "__main__":
    crawler = ThefirsthuntCrawler("thefirsthunt")
    crawler.run()
