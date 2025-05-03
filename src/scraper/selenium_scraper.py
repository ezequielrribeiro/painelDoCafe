import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class SeleniumScraper:
    __url: str

    def __init__(self, loggingFile = None):
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

    def __setURL(self, url) -> None:
        """Set the site's url to scrape"""
        self.__url = url

    def __parseMethod(self, body) -> None:
        pass

    def __scrapeInit(self) -> None:
        """Inits driver, access url and waits body element to be ready"""
        # Navigate to the URL
        self.logger.info(f"Navigating to {self.__url}...")
        self.driver.get(self.__url)

        # Wait for the page to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException as e:
            self.logger.error("Timeout waiting for page to load")
            raise
        except WebDriverException as e:
            self.logger.error(f"WebDriver Error: {str(e)}")
            raise

    def __scrapeEnd(self) -> None:
        """Ends the scrape process"""
        self.logger.info("Ending scraping process...")
        self.driver.quit()

    def scrapeSite(self) -> None:
        """Scrape using the configured parse method"""
        try:
            self.__scrapeInit()
            body = self.driver.find_element(By.TAG_NAME, "body")
            self.__parseMethod(body)
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
            raise
        finally:
            self.__scrapeEnd()
