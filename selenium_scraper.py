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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_driver():
    """Set up and return a configured Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Add user agent to mimic a real browser
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
        raise

def html_to_markdown(element):
    """Convert HTML element to Markdown format."""
    markdown = []
    
    # Process headings
    for level in range(1, 7):
        for heading in element.find_elements(By.TAG_NAME, f'h{level}'):
            markdown.append(f"{'#' * level} {heading.text}\n\n")
    
    # Process paragraphs
    for p in element.find_elements(By.TAG_NAME, 'p'):
        markdown.append(f"{p.text}\n\n")
    
    # Process lists
    for ul in element.find_elements(By.TAG_NAME, 'ul'):
        items = [f"- {li.text}\n" for li in ul.find_elements(By.TAG_NAME, 'li')]
        markdown.append('\n' + ''.join(items) + '\n')
    
    for ol in element.find_elements(By.TAG_NAME, 'ol'):
        items = [f"{i+1}. {li.text}\n" for i, li in enumerate(ol.find_elements(By.TAG_NAME, 'li'))]
        markdown.append('\n' + ''.join(items) + '\n')
    
    # Process links
    for a in element.find_elements(By.TAG_NAME, 'a'):
        href = a.get_attribute('href')
        text = a.text
        markdown.append(f"[{text}]({href})")
    
    # Process images
    for img in element.find_elements(By.TAG_NAME, 'img'):
        src = img.get_attribute('src')
        alt = img.get_attribute('alt')
        markdown.append(f"![{alt}]({src})")
    
    # Join all markdown elements
    markdown_text = ''.join(markdown)
    
    # Clean up multiple newlines
    markdown_text = re.sub(r'\n\s*\n', '\n\n', markdown_text)
    
    return markdown_text.strip()

def scrape_and_save(url, output_dir='output'):
    """Scrape a website using Selenium and save its content as markdown."""
    driver = None
    try:
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Get domain name for filename
        domain = urlparse(url).netloc
        filename = f"{domain.replace('.', '_')}.md"
        filepath = output_path / filename
        
        # Initialize WebDriver
        logger.info("Initializing WebDriver...")
        driver = setup_driver()
        
        # Navigate to the URL
        logger.info(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for the page to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            logger.warning("Timeout waiting for page to load")
        
        # Get the main content
        body = driver.find_element(By.TAG_NAME, "body")
        
        # Convert to markdown
        logger.info("Converting to markdown...")
        markdown_content = html_to_markdown(body)
        
        # Save to file
        logger.info(f"Saving to {filepath}...")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Content from {url}\n\n")
            f.write(markdown_content)
        
        logger.info(f"Successfully saved content to {filepath}")
        return True
        
    except WebDriverException as e:
        logger.error(f"WebDriver Error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()

def main():
    parser = argparse.ArgumentParser(description='Scrape a website using Selenium and save its content as markdown.')
    parser.add_argument('url', help='URL of the website to scrape')
    parser.add_argument('-o', '--output', default='output', help='Output directory (default: output)')
    
    args = parser.parse_args()
    scrape_and_save(args.url, args.output)

if __name__ == '__main__':
    main() 