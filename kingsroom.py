from base import RoomsCrawler


class KingsroomCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://kingsroom.bg/bg/rooms/it/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1059200691#gid=1059200691",
            "room": "KingsRoom-IT",
        },
        {
            "url": "https://kingsroom.bg/bg/rooms/salem/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=73772255#gid=73772255",
            "room": "KingsRoom - Salem's Loot",
        },
    ]

    NEXT_DAYS_SELECTOR = 'a.next.next-week'

    def scrape_room(self):
        days = self.safe_find("#calendar table", return_element=True, multiple=True)
        for day in days:
            date = self.safe_find(".table-title span", attr="innerText", search_element=day)

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


crawler = KingsroomCrawler("kingsroom")


if __name__ == "__main__":
    crawler.run()
