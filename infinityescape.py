from base import RoomsCrawler


class InfinityescapeCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://infinityescape.bg/the-secret-chamber",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=0#gid=0",
            "room": "InfinityEscape-ТайнатаСтая",
        },
        {
            "url": "https://infinityescape.bg/muggle",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1262372774#gid=1262372774",
            "room": "Infinity Escape - Мъгъл",
        },
        {
            "url": "https://infinityescape.bg/iron-throne",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=893595648#gid=893595648",
            "room": "Infinity Escape - Железният Трон",
        },
    ]

    def scrape_room(self):
        btn = self.safe_find("#keyhowl-reservation-form>button", return_element=True)
        self.make_click(btn)
        self.sleep_random(10, 20)

        days = self.safe_find(
            "button.keyhowl-reservation-form-cache-zsvzxq:not(.Mui-disabled), .MuiPickersDay-today:not(.Mui-disabled)",
            return_element=True,
            multiple=True,
        )

        for day in days[: self.max_days]:
            self.make_click(day)
            self.sleep_random(5, 10)

            time_els = self.safe_find('button[id][type="button"].MuiButton-root', return_element=True, multiple=True)

            date = self.safe_find('[role="separator"] div.MuiTypography-root.MuiTypography-body1', attr="textContent")
            date = date.split("г.")[0].strip().split(" ")[-1]
            day_num, month, year = date.split(".")
            date = "20" + year + "-" + month + "-" + day_num

            for time_el in time_els:
                time = time_el.get_attribute("textContent").strip()

                is_available = time_el.get_attribute("disabled")
                if is_available is None:
                    is_available = True
                else:
                    is_available = False
                entry = {
                    "date": date,
                    "time": time,
                    "available": is_available,
                }
                self.entries.append(entry)


crawler = InfinityescapeCrawler("infinityescape")


if __name__ == "__main__":
    crawler.run()
