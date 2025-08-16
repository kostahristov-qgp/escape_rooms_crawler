from base import RoomsCrawler


class GamecastlebgCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://gamecastlebg.com/bg/rooms/the-collector-and-the-mission-impossible/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=626292984#gid=626292984",
            "room": "GameCastle-КолекционерътиМисиятане/възможна",
        },
        {
            "url": "https://gamecastlebg.com/bg/rooms/magic-school/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=382350253#gid=382350253",
            "room": "GameCastle - Magic School",
        },
    ]

    NEXT_DAYS_SELECTOR = 'a.next-week.next'

    def scrape_room(self):
        days = self.safe_find("tr#calendar table", return_element=True, multiple=True)

        for day in days:
            date = self.safe_find("td.table-titel span", attr="innerText", search_element=day)

            date = "-".join(reversed(date.split(".")))

            time_els = self.safe_find('th[itemprop="bookingTime"]', return_element=True, search_element=day, multiple=True)

            for time_el in time_els:
                status = time_el.get_attribute("title")

                if status == "Свободен":
                    is_available = True
                elif status == "Запазен":
                    is_available = False
                else:
                    is_available = "unknown"

                time = time_el.get_attribute("innerText").strip()

                entry = {
                    "date": date,
                    "time": time,
                    "available": is_available,
                }

                self.entries.append(entry)


crawler = GamecastlebgCrawler("gamecastlebg")


if __name__ == "__main__":
    crawler.run()
