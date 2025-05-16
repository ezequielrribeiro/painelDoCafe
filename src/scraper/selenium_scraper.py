import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
import re

class SeleniumScraper:

    def __init__(self, loggingFile = None, chrome_options = None):
        self.__chrome_options = chrome_options
        logging.basicConfig(filename=loggingFile, level=logging.INFO)
        self._logger = logging.getLogger(__name__)
        self._setup_driver()

    def _setup_driver(self) -> None:
        """Set up and return a configured Chrome WebDriver."""
        if self.__chrome_options == None:
            self.__chrome_options = Options()
            self.__chrome_options.add_argument('--headless')  # Run in headless mode
            self.__chrome_options.add_argument('--no-sandbox')
            self.__chrome_options.add_argument('--disable-dev-shm-usage')
            self.__chrome_options.add_argument('--disable-gpu')
            self.__chrome_options.add_argument('--window-size=1920,1080')

        # Add user agent to mimic a real browser
        self.__chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Initialize WebDriver
        self._logger.info("Initializing WebDriver...")
        try:
            self._driver = webdriver.Chrome(options=self.__chrome_options)
        except Exception as e:
            self._logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
            raise

    def _scrape_init(self) -> None:
        """Inits driver, access url and waits body element to be ready"""
        # Wait for the page to load
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException as e:
            self._logger.error("Timeout waiting for page to load")
            raise
        except WebDriverException as e:
            self._logger.error(f"WebDriver Error: {str(e)}")
            raise

    def scrape_end(self) -> None:
        """Ends the scrape process"""
        self._logger.info("Ending scraping process...")
        self._driver.quit()

    def scrape_site(self, url: str, find_element_by: str = By.TAG_NAME, find_element_value: str = "body") -> WebElement:
        """Scrape a specific site using the provided parse function"""
        try:
            self._logger.info(f"Navigating to {url}...")
            self._driver.get(url)
            self._scrape_init()
            return self._driver.find_element(find_element_by, find_element_value)
        except Exception as e:
            self._logger.error(f"Error during scraping: {str(e)}")
            raise
