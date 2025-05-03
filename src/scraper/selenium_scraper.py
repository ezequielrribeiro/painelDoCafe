import argparse
import logging
from pathlib import Path
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import re

class SeleniumScraper:

    def __init__(self, url, loggingFile = None):
        self.url = url
        logging.basicConfig(filename=loggingFile, level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._setup_driver()

    def _setup_driver(self) -> None:
        """Set up and return a configured Chrome WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # Add user agent to mimic a real browser
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Initialize WebDriver
        self.logger.info("Initializing WebDriver...")
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
            raise

    def setURL(self, url) -> None:
        self.url = url

    def scrapeInit(self) -> None:
        # Navigate to the URL
        self.logger.info(f"Navigating to {self.url}...")
        self.driver.get(self.url)

        # Wait for the page to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            self.logger.warning("Timeout waiting for page to load")

    def scrapeEnd(self) -> None:
        self.driver.quit()