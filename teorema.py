from base import RoomsCrawler


class TeoremaCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://www.teorema.bg/%d0%b5%d1%81%d0%ba%d0%b5%d0%b9%d0%bf-%d1%81%d1%82%d0%b0%d1%8f-%d1%82%d1%80%d0%be%d1%82%d0%b8%d0%bb/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1511940191#gid=1511940191",
            "room": "Теорема-Атлантида",
        },
        {
            "url": "https://www.teorema.bg/%d0%b5%d1%81%d0%ba%d0%b5%d0%b9%d0%bf-%d1%81%d1%82%d0%b0%d1%8f-%d0%b0%d1%82%d0%bb%d0%b0%d0%bd%d1%82%d0%b8%d0%b4%d0%b0/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1065228150#gid=1065228150",
            "room": "Теорема - Тротил",
        },
    ]

    def scrape_room(self):
        days = self.safe_find("[data-date]:not(.prev-date)", return_element=True, multiple=True)

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
    crawler = TeoremaCrawler("teorema")
    crawler.run()
