from base import RoomsCrawler


class MystCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://www.myst.bg/rezerviray-chas",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1345809462#gid=1345809462",
            "room": "MYST-ТайнатанаКриптос",
        }
    ]

    NEXT_DAYS_SELECTOR = ".is-padded-mobile.text-right>a[href]:has(svg)"

    def scrape_room(self):
        date_times_table = self.safe_find("tbody tr", return_element=True, multiple=True)

        dates = self.safe_find("thead td", attr="innerText", multiple=True)
        dates = [date.split("\n")[0] for date in dates]
        dates = ["-".join(reversed(date.split("."))) for date in dates]
        all_available_slots = self.safe_find("tbody td:not(.is-booked)", attr="innerText", multiple=True)
        all_times = list(set(all_available_slots))

        for td in date_times_table:
            time = None
            all_times = self.safe_find("td", return_element=True, search_element=td, multiple=True)

            available_times = self.safe_find("td:not(.is-booked):not(.is-passed)", attr="innerText", multiple=True, search_element=td)

            for item_index, item in enumerate(all_times):
                time = item.get_attribute("innerText").strip()
                availability = item.get_attribute("class").strip()
                if "is-passed" in availability:
                    available = False
                    disabled = True
                    entry = {"date": dates[item_index], "time": time, "available": available, "disabled": disabled}
                else:
                    available = True
                    entry = {
                        "date": dates[item_index],
                        "time": time,
                        "available": available,
                    }

                if "is-booked" in availability or 'is-passed"' in availability:
                    entry["available"] = False
                    if len(available_times) > 0:
                        entry["time"] = available_times[-1]

                self.entries.append(entry)


if __name__ == "__main__":
    crawler = MystCrawler("myst")
    crawler.run()
