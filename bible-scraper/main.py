import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Dictionary to store the number of chapters for each book
books = {
    "GEN": 50, "EXO": 40, "LEV": 27, "NUM": 36, "DEU": 34, "JOS": 24, "JDG": 21, "RUT": 4,
    "1SA": 31, "2SA": 24, "1KI": 22, "2KI": 25, "1CH": 29, "2CH": 36, "EZR": 10, "NEH": 13,
    "EST": 10, "JOB": 42, "PSA": 150, "PRO": 31, "ECC": 12, "SNG": 8, "ISA": 66, "JER": 52,
    "LAM": 5, "EZK": 48, "DAN": 12, "HOS": 14, "JOL": 3, "AMO": 9, "OBA": 1, "JON": 4, "MIC": 7,
    "NAM": 3, "HAB": 3, "ZEP": 3, "HAG": 2, "ZEC": 14, "MAL": 4, "MAT": 28, "MRK": 16, "LUK": 24,
    "JHN": 21, "ACT": 28, "ROM": 16, "1CO": 16, "2CO": 13, "GAL": 6, "EPH": 6, "PHP": 4, "COL": 4,
    "1TH": 5, "2TH": 3, "1TI": 6, "2TI": 4, "TIT": 3, "PHM": 1, "HEB": 13, "JAS": 5, "1PE": 5,
    "2PE": 3, "1JN": 5, "2JN": 1, "3JN": 1, "JUD": 1, "REV": 22
}

def generate_bible_urls(books):
    base_url = "https://www.bible.com/bible/149/"
    urls = []
    
    for key, value in books.items():
        for i in range(1, value + 1):
            url = f"{base_url}{key}.{i}.RVR1960"
            urls.append((key, i, url))
    
    return urls

def scrape_text(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ChapterContent_chapter__uvbXo")))
    elements = driver.find_elements(By.CLASS_NAME, "ChapterContent_chapter__uvbXo")
    text = ' '.join([element.text for element in elements])
    return text

def main():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    bible_data = {}
    urls = generate_bible_urls(books)
    
    for book, chapter, url in urls:
        print(f"Scraping {book} Chapter {chapter}...")
        text = scrape_text(driver, url)
        
        if book not in bible_data:
            bible_data[book] = {}
        bible_data[book][chapter] = text
        
        time.sleep(3)  # Avoid overloading the server
    
    driver.quit()
    
    with open("bible_data.json", "w", encoding="utf-8") as f:
        json.dump(bible_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
