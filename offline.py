from base import RoomsCrawler


class OfflineCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://offline.bg/bg/rooms/hacker-room/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=137010675#gid=137010675",
            "room": "Offlinebg-СтаятанаХакера",
        },
        {
            "url": "https://offline.bg/bg/rooms/ancient-egypt/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1023585245#gid=1023585245",
            "room": "Offline bg - Древен Египет",
        },
    ]

    NEXT_DAYS_SELECTOR = ".change-week.next"

    def scrape_room(self):
        days = self.safe_find("#calendar table", return_element=True, multiple=True)
        for day in days:
            date = self.safe_find(".tdhead span", attr="innerText", search_element=day)

            date = "-".join(reversed(date.split("-")))

            time_els = self.safe_find("div.tips", return_element=True, search_element=day, multiple=True)

            for time_el in time_els:
                status = time_el.get_attribute("title")

                if status == "Свободен":
                    is_available = True
                elif status == "Зает" or status == "Запазен":
                    is_available = False
                elif status == "Изтекъл":
                    continue
                else:
                    is_available = "unknown"

                time = time_el.get_attribute("innerText").strip()

                entry = {
                    "date": date,
                    "time": time,
                    "available": is_available,
                }

                self.entries.append(entry)


if __name__ == "__main__":
    crawler = OfflineCrawler("offline")
    crawler.run()
