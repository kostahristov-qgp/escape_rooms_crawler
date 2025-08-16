from datetime import datetime
from zoneinfo import ZoneInfo

from base import RoomsCrawler


class SawroomCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://sawroom.bg/therevenge.html",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1764578027#gid=1764578027",
            "room": "SawRoom-TheRevenge",
        },
        {
            "url": "https://sawroom.bg/gameover.html",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=639674829#gid=639674829",
            "room": "SawRoom - Game Over",
        },
    ]

    def scrape_room(self):
        btn = self.safe_find("#keyhowl-reservation-form>button", return_element=True)

        self.make_click(btn)
        self.sleep_random(10, 20)

        booked_days = self.safe_find("button.keyhowl-reservation-form-cache-1irg3fc[disabled]", attr="data-timestamp", multiple=True)

        current_timestamp = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        for booked_day in booked_days:
            try:
                booked_day_timestampt = int(booked_day) / 1000
                if booked_day_timestampt > current_timestamp:
                    booked_date = datetime.fromtimestamp(booked_day_timestampt, tz=ZoneInfo("Europe/Sofia")).strftime("%Y-%m-%d")
                    entry = {"date": booked_date, "available": False}
                    self.entries.append(entry)
            except ValueError:
                pass

        days = self.safe_find(
            ".MuiButtonBase-root.MuiPickersDay-root:not(.Mui-disabled), .MuiPickersDay-today:not(.Mui-disabled)", return_element=True, multiple=True
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


if __name__ == "__main__":
    crawler = SawroomCrawler("sawroom")
    crawler.run()
