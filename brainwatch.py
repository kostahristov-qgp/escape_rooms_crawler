from base import RoomsCrawler


class BrainwatchCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://brain-watch.org/BG-%D0%A0%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%B0%D1%86%D0%B8%D0%B8.html",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1795845312#gid=1795845312",
            "room": "BrainWatch-Bornazium",
        }
    ]

    DATES_TABLE_SELECTOR = "table.table td"
    BTN_LVL_1_SELECTOR = 'form[method="POST"]>a'
    AVAILABLE_SLOTS_SELECTOR = "a"
    DATE_SELECTOR = "span"
    NOT_AVAILABLE_SLOTS_SELECTOR = ".//div/div[text()]"

    NEXT_DAYS_SELECTOR = 'button[id="Next" i]'

    NEXT_BUTTON_PRESSES_NUM = 30
    NEXT_BUTTON_PRESS_WAIT_TIME = 3

    def correct_date(self, date):
        day, month, year = date.split("-")
        full_date = year + "-" + month + "-" + day
        return full_date

    def scrape_room(self):
        btn_lvl_1 = self.safe_find(self.BTN_LVL_1_SELECTOR, return_element=True)
        if btn_lvl_1:
            self.make_click(btn_lvl_1)
            self.sleep_random(9, 15)

        dates_table = self.safe_find(self.DATES_TABLE_SELECTOR, return_element=True, multiple=True)

        for td in dates_table:
            date = self.safe_find(self.DATE_SELECTOR, attr="innerText", search_element=td)

            full_date = self.correct_date(date)

            available = self.safe_find(self.AVAILABLE_SLOTS_SELECTOR, attr="innerText", search_element=td, multiple=True)

            for item in available:
                entry = {"date": full_date, "time": item, "available": True}
                self.entries.append(entry)

            not_available = self.safe_find(self.NOT_AVAILABLE_SLOTS_SELECTOR, attr="innerText", search_element=td, multiple=True)

            for item in not_available:
                entry = {"date": full_date, "time": item, "available": False}
                self.entries.append(entry)


if __name__ == "__main__":
    crawler = BrainwatchCrawler("brainwatch")
    crawler.run()
