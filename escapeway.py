from base import RoomsCrawler


class EscapewayCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://escapeway.bg/bg/rooms/crystal-skull/book",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=807795492#gid=807795492",
            "room": "EscapeWay-КристалниятЧереп",
        }
    ]

    NEXT_DAYS_SELECTOR = ".change-week.next"

    def scrape_room(self):
        days = self.safe_find("tr#calendar tbody", return_element=True, multiple=True)

        for day in days:
            date = self.safe_find("span.thead-date", attr="innerText", search_element=day)

            date = "-".join(reversed(date.split("-")))

            time_els = self.safe_find('div[itemprop="bookingTime"]', return_element=True, search_element=day, multiple=True)

            for time_el in time_els:
                status = time_el.get_attribute("data-time-slot-status")

                if status == "free":
                    is_available = True
                elif status == "booked":
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


if __name__ == "__main__":
    crawler = EscapewayCrawler("escapeway")
    crawler.run()
