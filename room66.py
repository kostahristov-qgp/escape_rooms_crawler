from base import RoomsCrawler


class Room66Crawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://room66.bg/rooms/book/room_66.html#reservation",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1203099936#gid=1203099936",
            "room": "Room66-Room66I",
        },
        {
            "url": "https://room66.bg/rooms/book/room_66_II.html#reservation",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=136412082#gid=136412082",
            "room": "Room66 - Room 66 II",
        },
        {
            "url": "https://room66.bg/rooms/book/izkustven_intelekt.html#reservation",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1451829396#gid=1451829396",
            "room": "Room66 - Изкуствен Интелект",
        },
    ]
    NEXT_DAYS_SELECTOR = ".next.text-left"

    def scrape_room(self):
        days = self.safe_find("#calendar table", return_element=True, multiple=True)

        for day in days:
            date = self.safe_find("span.thead-date", attr="innerText", search_element=day)

            date = "-".join(reversed(date.split("-")))

            time_els = self.safe_find('.//div[contains(@class, "tips")]', return_element=True, search_element=day, multiple=True)

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
    crawler = Room66Crawler("room66")
    crawler.run()
