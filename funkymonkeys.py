from datetime import datetime

from base import RoomsCrawler


class FunkymonkeysCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://funkymonkeys.bg/escape-rooms/rebellion/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1370185569#gid=1370185569",
            "room": "FunkyMonkeys-Бунт",
        },
        {
            "url": "https://funkymonkeys.bg/escape-rooms/ghost-hunters/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=494183711#gid=494183711",
            "room": "FunkyMonkeys - Ловци на Духове",
        },
        {
            "url": "https://funkymonkeys.bg/escape-rooms/tears-and-sorrow/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1609034048#gid=1609034048",
            "room": "FunkyMonkeys - Сълзи и Скръб",
        },
        {
            "url": "https://funkymonkeys.bg/escape-rooms/the-cube-and-the-teleport/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1454593323#gid=1454593323",
            "room": "FunkyMonkeys - Кубът и Телепортът",
        },
    ]

    def scrape_room(self):
        days = self.safe_find("div[data-date]:not(.prev-date)", return_element=True, multiple=True)

        booked_dates = self.safe_find("[data-date].prev-date:not(.today)", attr="data-date", multiple=True)

        for booked_date in booked_dates:
            if datetime.strptime(booked_date, "%Y-%m-%d") > datetime.today():
                entry = {"date": booked_date, "available": False}
                self.entries.append(entry)

        for day in days[: self.max_days]:
            self.make_click(day)
            self.sleep_random(15, 20)

            time_els = self.safe_find("button[data-timeslot]", return_element=True, multiple=True)

            for time_el in time_els:
                date = time_el.get_attribute("data-date")
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
                    "date": date,
                    "time": full_time,
                    "available": is_available,
                }
                self.entries.append(entry)


if __name__ == "__main__":
    crawler = FunkymonkeysCrawler("funkymonkeys")
    crawler.run()
