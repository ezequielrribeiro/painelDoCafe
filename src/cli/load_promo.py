from src.scraper.selenium_scraper import SeleniumScraper
from selenium.webdriver.common.by import By

class LoadPromoEncantos(SeleniumScraper):

    def __init__(self, loggingFile=None):
        super().__init__(loggingFile)
        self.setURL("https://loja.encantosdocafe.com.br/produtos?promotion=1&page=1")
        self.markdown = ''

    def _parseMethod(self, body) -> None:
        # get product names and prizes
        for a in body.find_elements(By.CLASS_NAME, 'product-link'):
            self.logger.info(f"product:{a.get_attribute('aria-label')}")



    # def scrape_and_save(self):
    #     """Scrape a website using Selenium and save its content as markdown."""
    #     try:
    #         # Create output directory if it doesn't exist
    #         output_path = Path(self.output_dir)
    #         output_path.mkdir(exist_ok=True)
            
    #         # Get domain name for filename
    #         domain = urlparse(self.url).netloc
    #         filename = f"{domain.replace('.', '_')}.md"
    #         filepath = output_path / filename
            
    #         # Navigate to the URL
    #         self.logger.info(f"Navigating to {self.url}...")
    #         self.driver.get(self.url)
            
    #         # Wait for the page to load
    #         try:
    #             WebDriverWait(self.driver, 10).until(
    #                 EC.presence_of_element_located((By.TAG_NAME, "body"))
    #             )
    #         except TimeoutException:
    #             self.logger.warning("Timeout waiting for page to load")
            
    #         # Get the main content
    #         body = self.driver.find_element(By.TAG_NAME, "body")
            
    #         # Convert to markdown
    #         self.logger.info("Converting to markdown...")
    #         markdown_content = html_to_markdown(body)
            
    #         # Save to file
    #         self.logger.info(f"Saving to {filepath}...")
    #         with open(filepath, 'w', encoding='utf-8') as f:
    #             f.write(f"# Content from {url}\n\n")
    #             f.write(markdown_content)
            
    #         self.logger.info(f"Successfully saved content to {filepath}")
    #         return True
            
    #     except WebDriverException as e:
    #         self.logger.error(f"WebDriver Error: {str(e)}")
    #         return False
    #     except Exception as e:
    #         self.logger.error(f"Error: {str(e)}")
    #         return False
    #     finally:
    #         if self.driver:
    #             self.driver.quit()

# def html_to_markdown(element):
#     """Convert HTML element to Markdown format."""
#     markdown = []
    
#     # Process headings
#     for level in range(1, 7):
#         for heading in element.find_elements(By.TAG_NAME, f'h{level}'):
#             markdown.append(f"{'#' * level} {heading.text}\n\n")
    
#     # Process paragraphs
#     for p in element.find_elements(By.TAG_NAME, 'p'):
#         markdown.append(f"{p.text}\n\n")
    
#     # Process lists
#     for ul in element.find_elements(By.TAG_NAME, 'ul'):
#         items = [f"- {li.text}\n" for li in ul.find_elements(By.TAG_NAME, 'li')]
#         markdown.append('\n' + ''.join(items) + '\n')
    
#     for ol in element.find_elements(By.TAG_NAME, 'ol'):
#         items = [f"{i+1}. {li.text}\n" for i, li in enumerate(ol.find_elements(By.TAG_NAME, 'li'))]
#         markdown.append('\n' + ''.join(items) + '\n')
    
#     # Process links
#     for a in element.find_elements(By.TAG_NAME, 'a'):
#         href = a.get_attribute('href')
#         text = a.text
#         markdown.append(f"[{text}]({href})")
    
#     # Process images
#     for img in element.find_elements(By.TAG_NAME, 'img'):
#         src = img.get_attribute('src')
#         alt = img.get_attribute('alt')
#         markdown.append(f"![{alt}]({src})")
    
#     # Join all markdown elements
#     markdown_text = ''.join(markdown)
    
#     # Clean up multiple newlines
#     markdown_text = re.sub(r'\n\s*\n', '\n\n', markdown_text)
    
#     return markdown_text.strip()

def main():
    promo = LoadPromoEncantos()
    promo.scrapeSite()

if __name__ == '__main__':
    main()