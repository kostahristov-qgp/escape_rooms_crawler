from datetime import date, datetime

from base import RoomsCrawler


class HorrorhouseCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://horrorhouse.bg/reserve-now/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=95380504#gid=95380504",
            "room": "HorrorHouse-HorrorHouse",
        }
    ]

    def scrape_room(self):
        days = self.safe_find("[data-date]:not(.prev-date)", return_element=True, multiple=True)

        booked_dates = self.safe_find("td.prev-date[data-date]", attr="data-date", multiple=True)

        booked_dates = sorted([saved_date for saved_date in booked_dates if datetime.strptime(saved_date, "%Y-%m-%d").date() >= date.today()])

        for booked_date in booked_dates[:self.max_days]:
            if datetime.strptime(booked_date, "%Y-%m-%d").date() >= date.today():
                entry = {"date": booked_date, "available": False, "time": "full day"}
                self.entries.append(entry)

        for day in days[: self.max_days]:
            self.make_click(day)
            self.sleep_random(12, 17)

            time_els = self.safe_find("button[data-timeslot]", return_element=True, multiple=True)

            for time_el in time_els:
                saved_date = time_el.get_attribute("data-date")
                time = time_el.get_attribute("data-timeslot")
                start_time, end_time = time.split("-")
                start_time = start_time[:2] + ":" + start_time[2:]
                end_time = end_time[:2] + ":" + end_time[2:]

                full_time = start_time + " - " + end_time
                is_available = time_el.get_attribute("disabled")
                if is_available is None:
                    is_available = True
                else:
                    is_available = False
                entry = {
                    "date": saved_date,
                    "time": full_time,
                    "available": is_available,
                }
                self.entries.append(entry)


crawler = HorrorhouseCrawler("horrorhouse")


if __name__ == "__main__":
    crawler.run()
