from selenium.common.exceptions import StaleElementReferenceException

from base import RoomsCrawler


class KeyroomsCrawler(RoomsCrawler):
    START_INFO = [
        {
            "url": "https://3keyrooms.com/detektivat-mashinata-na-vremeto/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=465218196#gid=465218196",
            "room": "3keyRooms-ДетективътиМашинатанавремето",
        },
        {
            "url": "https://3keyrooms.com/tainiat-bar-al-capone/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1060700587#gid=1060700587",
            "room": "3keyRooms - МаТРИК",
        },
        {
            "url": "https://3keyrooms.com/matrick/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=2122483622#gid=2122483622",
            "room": "3keyRooms - Тайният Бар на Ал Капоне",
        },
        {
            "url": "https://3keyrooms.com/boom-staia/",
            "shortcut": "https://docs.google.com/spreadsheets/d/165YWYhIfI6e1n_pv4uikid28HNpaZuyP6j7GIIJ9kMg/edit?gid=1389638403#gid=1389638403",
            "room": "3keyRooms - БУМ! Стаята",
        },
    ]

    def scrape_room(self):
        days_selector = "div.DOPBSPCalendar-day:not(.dopbsp-past-day)"
        days_els = self.safe_find(days_selector, return_element=True, multiple=True)
        
        processed_days = 0
        days_els = days_els[:self.max_days]
        for day_index, day in enumerate(days_els):
            if processed_days >= 7:
                break
            days_els = self.safe_find(days_selector, return_element=True, multiple=True)
            days_els = days_els[:self.max_days]
            self.make_click(days_els[day_index])
            self.sleep_random(5, 10)

            days_els = self.safe_find(days_selector, return_element=True, multiple=True)
            days_els = days_els[:self.max_days]
            try:
                date = days_els[day_index].get_attribute("id").split("_")[-1]
            except StaleElementReferenceException:
                self.logger.warning("StaleElementReferenceException")
                continue
            except IndexError:
                self.logger.warning("IndexError")

            time_els_selector = ".DOPBSPCalendar-hours div.DOPBSPCalendar-hour"
            time_els = self.safe_find(time_els_selector, return_element=True, multiple=True)

            if not time_els:
                days_els = self.safe_find(days_selector, return_element=True, multiple=True)
                self.make_click(days_els[day_index])
                self.sleep_random(12, 17)
                time_els = self.safe_find(time_els_selector, return_element=True, multiple=True)

            for time_el in time_els:
                time = time_el.get_attribute("id").split("_")[-1]

                is_available = time_el.get_attribute("class")
                if "dopbsp-available" in is_available:
                    is_available = True
                elif "dopbsp-booked" in is_available:
                    is_available = False
                else:
                    is_available = "unknown"
                entry = {
                    "date": date,
                    "time": time,
                    "available": is_available,
                }
                self.entries.append(entry)

            processed_days += 1


crawler = KeyroomsCrawler("keyrooms")


if __name__ == "__main__":
    crawler.run()
