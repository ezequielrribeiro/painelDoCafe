from src.scraper.selenium_scraper import SeleniumScraper
from selenium.webdriver.common.by import By

class LoadPromos:

    __products: list[dict]

    def __init__(self):
        self.__products = []
        self.scraper = SeleniumScraper()
        self.markdown = ''

    def scrapePromos(self) -> None:
        self._scrapePromoEncantos()
        self.scraper.scrapeEnd()

    def _scrapePromoEncantos(self) -> None:
        body = self.scraper.scrapeSite("https://loja.encantosdocafe.com.br/produtos?promotion=1&page=1")
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
            self.__products.append(product_info)
        
        # get product description
        for product in self.__products:
            body_a = self.scraper.scrapeSite(product['link'])
            product['description'] = body_a.find_element(By.CLASS_NAME, 'product-description-item').text
        
        print(self.__products)

def main():
    promo = LoadPromos()
    promo.scrapePromos()

if __name__ == '__main__':
    main()