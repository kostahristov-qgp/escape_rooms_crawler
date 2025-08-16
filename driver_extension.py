import logging
import os
import random
import shutil
import tempfile
from datetime import datetime
from time import sleep

from selenium.common.exceptions import (
    InvalidArgumentException,
    InvalidSessionIdException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
    ElementClickInterceptedException
)
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import Driver
from urllib3.exceptions import MaxRetryError, NewConnectionError, ReadTimeoutError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DriverExtension:
    """Extension class that equipped with chrome driver and useful methods."""

    USE_DRIVER = True
    headless = True
    uc = False

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        logs_dir = os.path.join(BASE_DIR, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("\n%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.SELENIUM_TMP_DIR = "selenium_tmp"
        self.cleanup_temp_directories()

    def init_driver(self):
        """Initialize driver."""
        # Ensure the directory exists
        os.makedirs(self.SELENIUM_TMP_DIR, exist_ok=True)
        temp_dir = self.create_temp_directory()
        self.driver: Chrome = Driver(uc=self.uc, locale="bg", locale_code="bg_BG", headless=self.headless, user_data_dir=temp_dir)
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)

    def quit_driver(self):
        """Quit driver."""
        try:
            self.driver.quit()
        except (WebDriverException, InvalidSessionIdException, NoSuchWindowException) as e:
            self.logger.warning(f"Could not close driver. Error: {e}")
        except Exception as e:
            self.logger.exception(f"Unexpected error: {e}")

    def make_click(self, element):
        """Make a js click on an element."""
        try:
            element.click()
        except Exception as e:
            self.sleep_random(1, 2)
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except (StaleElementReferenceException, ElementClickInterceptedException):
                self.logger.error(f"Failed to click on element. Error: {type(e).__name__}")
                self.save_screenshot_on_error(prefix="Failed to click on element")
            except Exception as e:
                self.logger.error(f"Failed to click on element. Unexpected Error: {e}")
                self.save_screenshot_on_error(prefix="Failed to click on element, Unexpected Error")

    def safe_find(self, search_selector: str, attr=None, default="", wait_time=0, search_element=None, multiple=False, return_element=False):
        """Safely find an element(s) by XPath or CSS and get its attribute or the element(s) itself.
        Args:
            search_selector: XPath or CSS selector.
            attr: Optional attribute to get from the element(s). Default is text.
            default: Default value to return if the element(s) are not found.
            wait_time: Maximum wait time in seconds.
            search_element: Element to search within. Defaults to the driver.
            multiple: Whether to return a list of elements.
            return_element: Whether to return the web element(s) themselves."""
        if search_element is None:
            search_element = self.driver

        if search_selector.startswith(("//", "/", "./", ".//")):
            search_method = By.XPATH
        else:
            search_method = By.CSS_SELECTOR
        try:
            if multiple:
                condition = EC.presence_of_all_elements_located((search_method, search_selector))
            else:
                condition = EC.presence_of_element_located((search_method, search_selector))
            self.close_modals()
            element = WebDriverWait(search_element, wait_time).until(condition)

            if return_element:
                return element
            else:
                if multiple:
                    value = [e.get_attribute(attr) if attr else e.text for e in element]
                    return value
                else:
                    value = element.get_attribute(attr) if attr else element.text
                    return value.strip() if value else default
        except (TimeoutException, StaleElementReferenceException, NoSuchWindowException):
            if multiple:
                return []
            else:
                return default
        except (
            TimeoutError,
            ReadTimeoutError,
            MaxRetryError,
            NewConnectionError,
        ) as e:
            self.logger.warning(f"{type(e).__name__}: Reloading driver...")
            self.save_screenshot_on_error(e, prefix=f"safe_find_{self.driver.current_url}")
        except (InvalidSessionIdException, WebDriverException) as e:
            self.logger.warning(f"{type(e).__name__}: Reloading driver...")

    def load_html(self, html: str, wait_time=3, retry=False):
        """Load html with selenium.
        Args:
            driver:selenium driver.
            html: target html link.
            wait_time: average wait time(+- 20%) in seconds after page is loaded.
        """
        try:
            self.driver.get(html)
            WebDriverWait(self.driver, 100).until(lambda d: d.execute_script("return document.readyState") == "complete")
            sleep(random.uniform(wait_time * 0.8, wait_time * 1.2))
            self.close_modals()
        except (
            TimeoutError,
            ReadTimeoutError,
            MaxRetryError,
            NewConnectionError,
            TimeoutException,
        ) as e:
            self.logger.warning(f"{type(e).__name__}: when fetching {html}  Reloading driver...")
            self.save_screenshot_on_error(e, prefix=f"load_html_{html}")
        except (InvalidSessionIdException, WebDriverException) as e:
            self.logger.warning(f"{type(e).__name__}: when fetching {html}  Reloading driver...")

            if not retry:
                self.reload_driver()
                self.load_html(html, wait_time=wait_time, retry=True)  # only one retry
            else:
                self.logger.error(f"Retry failed: could not fetch {html}")
        except InvalidArgumentException:
            self.logger.warning(f"Invalid URL: {html}")
        except Exception as e:
            self.logger.warning(f"Unexpected error when fetching  {html} : {e}", exc_info=True)
            self.save_screenshot_on_error(e, prefix=f"load_html_{html}")

    def save_screenshot_on_error(self, exc="", prefix="error"):
        """Save screenshot with timestamp, prefix, and exception type into ./errors directory."""
        screenshots_dir = os.path.join(BASE_DIR, "errors")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exc_name = type(exc).__name__
        if exc_name == "str":
            exc_name = ""
        filename = f"{prefix}_{exc_name}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)

        try:
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath.split('/')[-1]}")
        except Exception as e:
            self.logger.warning(f"Failed to save screenshot: {e}")

    def sleep_random(self, min: float = 1.0, max: float = 2.0):
        """Randomly sleep for a while."""
        sleep(random.uniform(min, max))

    def reload_driver(self):
        """Reloading driver after error"""
        self.quit_driver()
        sleep(random.uniform(60, 90))
        self.init_driver()

    def close_modals(self):
        """Closing possible extension tabs"""
        if self.driver.current_url.startswith("chrome-extension") and len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def cleanup_temp_directories(self):
        """Remove all files and directories in the custom Selenium temp folder. As selenium creates temp directories on each run
        it is better to clean them up so that we don't run out of disk space."""
        if os.path.exists(self.SELENIUM_TMP_DIR):
            for item in os.listdir(self.SELENIUM_TMP_DIR):
                try:
                    item_path = os.path.join(self.SELENIUM_TMP_DIR, item)
                    if os.path.isdir(item_path):
                        try:
                            shutil.rmtree(item_path)  # Remove subdirectories
                        except FileNotFoundError:
                            pass
                    elif os.path.isfile(item_path):
                        os.remove(item_path)  # Remove files
                except PermissionError:
                    pass

        os.makedirs(self.SELENIUM_TMP_DIR, exist_ok=True)

    def create_temp_directory(self):
        """Create a new temporary directory for Selenium."""
        return tempfile.mkdtemp(dir=self.SELENIUM_TMP_DIR)
