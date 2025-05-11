from src.scraper.selenium_scraper import SeleniumScraper
from selenium.webdriver.common.by import By
import json
import os
from datetime import datetime

class LoadPromos:

    __products: dict[str, list[dict]]
    __CACHE_FILE = "promo_cache.json"

    def __init__(self):
        self.__products = {}
        self.__scraper = SeleniumScraper()
        self.__markdown = ''
        self.__load_from_cache()

    def __save_to_cache(self) -> None:
        """Save products data to cache file with timestamp."""
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'products': self.__products
        }
        with open(self.__CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def __load_from_cache(self) -> None:
        """Load products data from cache file if it exists."""
        if os.path.exists(self.__CACHE_FILE):
            try:
                with open(self.__CACHE_FILE, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    self.__products = cache_data['products']
            except (json.JSONDecodeError, KeyError):
                self.__products = {}

    def scrapePromos(self) -> None:
        self._scrapePromoEncantos()
        self._scrapePromoDutra()
        self.__scraper.scrapeEnd()
        self.__convertPromoToMarkdown()
        self.__save_to_cache()

    def __convertPromoToMarkdown(self) -> None:
        # Convert products dictionary to markdown format
        for product_manufacturer, product_list in self.__products.items():
            self.__markdown += f"## {product_manufacturer}\n\n"
            for product in product_list:
                self.__markdown += f"### {product['name']}\n\n"
                self.__markdown += f"- preço: ~~{product['original_price']}~~ {product['discount_price']}\n\n\n\n"
                self.__markdown += f"{product['description']}\n\n\n\n"
                self.__markdown += f"- URL: [{product['link']}]({product['link']})\n\n"
                self.__markdown += "---\n\n"

    def getPromosMarkdown(self) -> str:
        return self.__markdown

    def _scrapePromoEncantos(self) -> None:
        if 'Encantos do Café' in self.__products:
            return

        body = self.__scraper.scrapeSite("https://loja.encantosdocafe.com.br/produtos?promotion=1&page=1")

        # Initialize the list for Encantos do Café products
        self.__products['Encantos do Café'] = []

        # get product names and prizes
        for a in body.find_elements(By.CLASS_NAME, 'product-link'):
            # ignore elements with blank prices and discounts
            if a.find_element(By.CLASS_NAME, 'discount').text == '':
                continue
            # Create a dictionary with product info
            product_info = {
                'name': a.get_attribute('aria-label'),
                'original_price': a.find_element(By.CLASS_NAME, 'discount').text,
                'discount_price': a.find_element(By.CLASS_NAME, 'price').text,
                'link': a.get_attribute('href')
            }
            # Add to products list
            self.__products['Encantos do Café'].append(product_info)
        
        # get product description
        for product in self.__products['Encantos do Café']:
            body_a = self.__scraper.scrapeSite(product['link'])
            product['description'] = body_a.find_element(By.CLASS_NAME, 'product-description-item').text

    def _scrapePromoDutra(self) -> None:
        if 'Café Dutra' in self.__products:
            return

        body = self.__scraper.scrapeSite("https://loja.cafedutra.com.br/product-category/kits-presentes/")
        # Initialize the list for Dutra products
        self.__products['Café Dutra'] = []
        
        # get product names and prizes
        for li in body.find_elements(By.CLASS_NAME, 'product_cat-kits-presentes'):
            # ignore elements with blank prices and discounts
            # if li.find_element(By.CLASS_NAME, 'woocommerce-loop-product__title').text == '':
                # continue
            # Create a dictionary with product info
            product_info = {
                'name': li.find_element(By.CLASS_NAME, 'woocommerce-loop-product__title').text,
                'original_price': li.find_element(By.TAG_NAME, 'del').text,
                'discount_price': li.find_element(By.TAG_NAME, 'bdi').text,
                'link': li.find_element(By.TAG_NAME, 'a').get_attribute('href')
            }
            # Add to products list
            self.__products['Café Dutra'].append(product_info)
        
        # get product description
        for product in self.__products['Café Dutra']:
            body_a = self.__scraper.scrapeSite(product['link'])
            product['description'] = body_a.find_element(By.CLASS_NAME, 'elementor-tab-content').get_dom_attribute('innerText')

def main():
    promo = LoadPromos()
    promo.scrapePromos()

if __name__ == '__main__':
    main()