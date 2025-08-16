import calendar
from datetime import datetime

from base import RoomsCrawler


class QuestomaniaCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://questomania.bg/bg/rooms/secrets-of-professor-lind/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1719754140#gid=1719754140",
            "room": "QuestMania-ТайнитенапрофесорЛинд",
        },
        {
            "url": "https://questomania.bg/bg/rooms/portal/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=145683450#gid=145683450",
            "room": "QuestMania - Портал",
        },
    ]

    NEXT_DAYS_SELECTOR = "button.next.week"

    def scrape_room(self):
        days = self.safe_find("[data-month]", return_element=True, multiple=True)
        for day_index, day in enumerate(days):
            date = self.safe_find(".day_header span", attr="innerText", search_element=day)

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
            entry = {
                "date": formatted_date,
            }

            available_times = self.safe_find('[itemprop="bookingTime"]', attr="innerText", search_element=day, multiple=True)

            for time in available_times:
                entry = {"date": formatted_date, "time": time, "available": True}
                self.entries.append(entry)


            not_available_times = self.safe_find("span[data-date]", return_element=True, search_element=day, multiple=True)

            for not_available_time in not_available_times:
                entry = {
                    "date": not_available_time.get_attribute("data-date"),
                    "time": not_available_time.get_attribute("innerText"),
                    "available": False,
                }
                self.entries.append(entry)


crawler = QuestomaniaCrawler("questomania")


if __name__ == "__main__":
    crawler.run()
