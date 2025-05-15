from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import os
import re

# Setup Selenium with improved options
options = Options()
options.add_argument("--headless=new")  # Modern headless mode
options.add_argument("--disable-dev-shm-usage")  # Prevent crashes
options.add_argument("--no-sandbox")  # Linux compatibility
driver = webdriver.Chrome(options=options)

# Main URL
base_url = "https://cbc.radio-canada.ca/en/vision/governance/journalistic-standards-and-practices"

# Step 1: Get all titles from the main page
print("Step 1: Extracting subpage links...")
driver.get(base_url)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "h3.policy-title"))
)

soup = BeautifulSoup(driver.page_source, "html.parser")
titles = soup.find_all("h3", class_="policy-title")

def slugify(title):
    title = re.sub(r'[^\w\s-]', '', title)
    return re.sub(r'[-\s]+', '-', title.strip().lower())

unique_titles = sorted(set(title.text.strip() for title in titles))
subpage_links = [f"{base_url}/{slugify(title)}" for title in unique_titles]
print(f"Found {len(subpage_links)} subpages")

# Step 2: Scrape each subpage with proper content handling
print("\nStep 2: Scraping subpages...")
scraped_data = []

for idx, url in enumerate(subpage_links):
    try:
        print(f"  ({idx+1}/{len(subpage_links)}) Processing: {url}")
        driver.get(url)
        
        # Wait for core content to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.panel-body"))
        )
        
        # Try expanding sections if button exists
        try:
            expand_button = driver.find_element(By.XPATH, "//button[contains(., 'Expand all sections')]")
            driver.execute_script("arguments[0].scrollIntoView();", expand_button)
            expand_button.click()
            print("    ➕ Expanded sections")
            time.sleep(1)  # Allow animation
        except:
            pass
        
        # Scroll to trigger lazy-loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        
        # Parse content
        page_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract title
        title = page_soup.find("h1").get_text(strip=True) if page_soup.find("h1") else "Untitled"
        
        # Extract content from panel bodies
        content_sections = []
        for panel in page_soup.select("div.panel-body"):
            section_text = []
            for element in panel.find_all(["p", "li"]):  # Include list items
                text = element.get_text(" ", strip=True)
                if text:
                    section_text.append(text)
            if section_text:
                content_sections.append("\n".join(section_text))
        
        full_content = "\n\n".join(content_sections)
        
        scraped_data.append({
            "url": url,
            "title": title,
            "content": full_content
        })
        
        print(f"    ✅ Scraped: {title} ({len(full_content)} chars)")

    except Exception as e:
        print(f"    ❌ Failed: {str(e)[:100]}...")
        scraped_data.append({
            "url": url,
            "title": "SCRAPE FAILED",
            "content": ""
        })

driver.quit()

# Step 3: Save results
print("\nStep 3: Saving data...")
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'cbc_guidelines.json')

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(scraped_data, f, ensure_ascii=False, indent=2)

print(f"✅ Done! Saved {len(scraped_data)} records to:\n{output_path}")
