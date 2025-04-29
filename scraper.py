import argparse
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
from urllib.parse import urlparse
import logging
import chardet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_encoding(content):
    """Detect the encoding of the content."""
    result = chardet.detect(content)
    return result['encoding']

def get_webpage_content(url, headers):
    """Fetch webpage content with proper encoding handling."""
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    # Try to get encoding from response headers
    encoding = response.encoding
    
    # If no encoding in headers, detect it
    if not encoding or encoding.lower() == 'iso-8859-1':
        encoding = detect_encoding(response.content)
    
    # Decode content with detected encoding
    try:
        content = response.content.decode(encoding)
    except UnicodeDecodeError:
        # If decoding fails, try utf-8
        try:
            content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            # If still fails, try latin1 as last resort
            content = response.content.decode('latin1')
    
    return content

def html_to_markdown(html_content):
    """Convert HTML content to Markdown format."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Convert headings
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        level = int(h.name[1])
        h.replace_with(f"{'#' * level} {h.get_text()}\n\n")
    
    # Convert paragraphs
    for p in soup.find_all('p'):
        p.replace_with(f"{p.get_text()}\n\n")
    
    # Convert lists
    for ul in soup.find_all('ul'):
        items = [f"- {li.get_text()}\n" for li in ul.find_all('li')]
        ul.replace_with('\n' + ''.join(items) + '\n')
    
    for ol in soup.find_all('ol'):
        items = [f"{i+1}. {li.get_text()}\n" for i, li in enumerate(ol.find_all('li'))]
        ol.replace_with('\n' + ''.join(items) + '\n')
    
    # Convert links
    for a in soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text()
        a.replace_with(f"[{text}]({href})")
    
    # Convert images
    for img in soup.find_all('img'):
        src = img.get('src', '')
        alt = img.get('alt', '')
        img.replace_with(f"![{alt}]({src})")
    
    # Get clean text
    text = soup.get_text()
    
    # Clean up multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()

def scrape_and_save(url, output_dir='output'):
    """Scrape a website and save its content as markdown."""
    try:
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Get domain name for filename
        domain = urlparse(url).netloc
        filename = f"{domain.replace('.', '_')}.md"
        filepath = output_path / filename
        
        # Headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Fetch the webpage with proper encoding handling
        logger.info(f"Fetching {url}...")
        content = get_webpage_content(url, headers)
        
        # Convert to markdown
        logger.info("Converting to markdown...")
        markdown_content = html_to_markdown(content)
        
        # Save to file with UTF-8 encoding
        logger.info(f"Saving to {filepath}...")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Content from {url}\n\n")
            f.write(markdown_content)
        
        logger.info(f"Successfully saved content to {filepath}")
        return True
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            logger.error("Access forbidden (403). The website might be blocking automated requests.")
            logger.error("Try using a different User-Agent or adding more headers.")
        else:
            logger.error(f"HTTP Error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Scrape a website and save its content as markdown.')
    parser.add_argument('url', help='URL of the website to scrape')
    parser.add_argument('-o', '--output', default='output', help='Output directory (default: output)')
    
    args = parser.parse_args()
    scrape_and_save(args.url, args.output)

if __name__ == '__main__':
    main() 