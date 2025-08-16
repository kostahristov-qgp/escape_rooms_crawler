import calendar
from datetime import datetime

from base import RoomsCrawler


class RobCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://www.rob.bg/rezerviray-chas",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=473169029#gid=473169029",
            "room": "RobBG-ПерфектниятБанковОбир",
        }
    ]

    NEXT_DAYS_SELECTOR = '.flex.items-center.justify-between svg:has(path[d^="M0.9392"])'

    TIME_SLOTS_SELECTOR = "div.flex.flex-col.py-4.text-center.font-semibold.rounded.cursor-pointer span"

    def scrape_room(self):
        days = self.safe_find("div.flex.flex-col.space-y-8.mt-14.items-stretch", return_element=True, multiple=True)

        all_times = self.safe_find(
            self.TIME_SLOTS_SELECTOR,
            attr="innerText",
            multiple=True,
        )

        all_times = list(set(all_times))

        for day_index, day in enumerate(days):
            date = self.safe_find("div.flex.flex-col.space-y-1", attr="innerText", search_element=day)

            date = date.replace("\n", " ").strip()

            today = datetime.today()

            if day_index == 0:
                day_in_month = int(date.split(" ")[-1])
                month = today.month
                year = today.year
            else:
                days_in_month = calendar.monthrange(year, month)[1]
                day_in_month = day_in_month + 1
                if day_in_month > days_in_month:
                    day_in_month = 1
                    if month == 12:
                        year += 1
                        month = 1
                    else:
                        month += 1
            date_obj = datetime(year, month, day_in_month)
            formatted_date = date_obj.strftime("%Y-%m-%d")

            times = self.safe_find(
                self.TIME_SLOTS_SELECTOR,
                attr="innerText",
                search_element=day,
                multiple=True,
            )

            processed_times = []

            for time in times:
                entry = {"date": formatted_date, "time": time, "available": True}
                processed_times.append(time)
                self.entries.append(entry)

            not_processed_times = list(set(all_times) - set(processed_times))

            if day_index == 0:
                past_times = self.safe_find(
                    '[class="flex flex-col py-4 text-center font-semibold rounded transition-all duration-300 uppercase border-2 border-transparent text-[#49BE81] bg-[#125337] cursor-not-allowed!"]',
                    attr="innerText",
                    multiple=True,
                )
                for time in not_processed_times:
                    entry = {"date": formatted_date, "time": time, "available": False}
                    if time in past_times:
                        entry["available"] = True
                    self.entries.append(entry)
            else:
                for time in not_processed_times:
                    entry = {"date": formatted_date, "time": time, "available": False}
                    self.entries.append(entry)


if __name__ == "__main__":
    crawler = RobCrawler("rob")
    crawler.run()
