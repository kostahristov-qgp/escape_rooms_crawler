from datetime import date, datetime

from base import RoomsCrawler


class Insight_roomsCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://insight-rooms.com/%d1%80%d0%b5%d0%b7%d0%b5%d1%80%d0%b2%d0%b0%d1%86%d0%b8%d0%b8/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1291627332#gid=1291627332",
            "room": "InsightRooms-InsightRooms",
        }
    ]

    def scrape_room(self):
        days_selector = ".datepick-days-cell:not(.datepick-unselectable)"
        days_els = self.safe_find(days_selector, return_element=True, multiple=True)

        dates = self.safe_find(days_selector, attr="class", multiple=True)
        dates = [date.split("sql_date_")[-1].split(" ")[0] for date in dates]

        fully_booked_today = self.safe_find(".datepick-today.datepick-unselectable", return_element=True)

        today = date.today()
        today_str = today.strftime("%Y-%m-%d")

        if fully_booked_today:
            entry = {"date": today_str, "available": False, "time": "full day"}
            self.entries.append(entry)

        days_els = days_els[: self.max_days]
        for day_index, day in enumerate(days_els):
            days_els = self.safe_find(days_selector, return_element=True, multiple=True)
            days_els = days_els[: self.max_days]
            self.make_click(days_els[day_index])
            self.sleep_random(4, 8)

            date_str = dates[day_index]

            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            weekday_num = date_obj.weekday()

            is_weekend = False
            if weekday_num in [5, 6]:
                is_weekend = True

            time_els = self.safe_find('[name="rangetime1"]>option[value]', return_element=True, multiple=True)

            for time_el in time_els:
                time = time_el.get_attribute("value").strip()

                time_txt = time_el.get_attribute("innerText").strip()

                only_wknd_txt = "Only Weekend"

                if only_wknd_txt in time_txt and not is_weekend:
                    continue

                is_available = time_el.get_attribute("disabled")
                if is_available is None:
                    is_available = True
                else:
                    is_available = False
                entry = {
                    "date": date_str,
                    "time": time,
                    "available": is_available,
                }
                self.entries.append(entry)


if __name__ == "__main__":
    crawler = Insight_roomsCrawler("insight_rooms")
    crawler.run()
