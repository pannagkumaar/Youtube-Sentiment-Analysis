import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import time

def scrape_youtube_comments(url):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") 
    options.add_argument("--mute-audio")

   

    driver=webdriver.Chrome(options=options)
   
    
    driver.get(url)
    time.sleep(2)
    
    # Uncomment the below 2 lines if you dont want the file to have the video title as name @harshith
    # Get video title from the page title
    video_title = driver.title.split(" - YouTube")[0]
    # Remove invalid characters from filename
    video_title = re.sub(r'[<>:"/\\|?*]', '', video_title)
    
    # Uncomment below 2 lines if you don't want the title to be separated by underscores@harshith
    video_title = ["_" if x == " " else x for x in video_title]
    video_title = "".join(video_title)


    
    pause_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))
    pause_button.click()
    time.sleep(1)

   
    last_height = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

   
    usernames = driver.find_elements(By.CSS_SELECTOR, "#author-text > span")
    comments = driver.find_elements(By.CSS_SELECTOR, "#content-text")

    
    data = {'Username': [username.text for username in usernames],
            'Comment': [comment.text for comment in comments]}
    df = pd.DataFrame(data)

    # Replace with whatever name you want @harshith
    output_file = f"{video_title}_comments.xlsx"
    df.to_excel(output_file, index=False)

    
    driver.quit()

    print(f"Comments scraped successfully and saved to '{output_file}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python file.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    scrape_youtube_comments(url)
