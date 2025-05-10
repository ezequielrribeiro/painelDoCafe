from src.scraper.selenium_scraper import SeleniumScraper
from selenium.webdriver.common.by import By

class LoadPromos:

    __products: dict[str, list[dict]]

    def __init__(self):
        self.__products = {}
        self.__scraper = SeleniumScraper()
        self.__markdown = ''

    def scrapePromos(self) -> None:
        self._scrapePromoEncantos()
        self.__scraper.scrapeEnd()
        self.__convertPromoToMarkdown()

    def __convertPromoToMarkdown(self) -> None:
        # Convert products dictionary to markdown format
        for product_manufacturer, product_list in self.__products.items():
            self.__markdown = f"## {product_manufacturer}\n\n"
            for product in product_list:
                self.__markdown += f"### {product['name']}\n\n"
                self.__markdown += f"- preço: ~~{product['original_price']}~~ {product['discount_price']}\n\n\n\n"
                self.__markdown += f"{product['description']}\n\n\n\n"
                self.__markdown += f"- URL: [{product['link']}]({product['link']})\n\n"
                self.__markdown += "---\n\n"

    def getPromosMarkdown(self) -> str:
        return self.__markdown

    def _scrapePromoEncantos(self) -> None:
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

def main():
    promo = LoadPromos()
    promo.scrapePromos()

if __name__ == '__main__':
    main()