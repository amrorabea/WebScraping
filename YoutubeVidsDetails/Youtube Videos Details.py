from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()

target = input("Search: ")
target = target.replace(" ", "+")
driver.get(f"YOUTUBE SEARCHED LINK GOES HERE")
driver.maximize_window()

cnt = 6000
i = 6
while i:
    driver.execute_script(f"Window.scrollBy(0, {cnt})", "")
    time.sleep(4)
    cnt += cnt
    i -= 1
time.sleep(2)

content = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")  # get all videos

Results = []

for i in range(len(content)):
    url = content[i].find_element(By.ID, "video-title").get_attribute("href")
    if url[24] == 'w':  # we check if the video is not a short and is not a none
        val = WebDriverWait(content[i], 5).until(
            EC.presence_of_element_located(
                (By.ID, "video-title")
            )
        )
        title = val.get_attribute("title")

        # the view in first 2 words, publish date is the rest
        val = WebDriverWait(content[i], 5).until(
            EC.presence_of_element_located(
                (By.ID, "metadata-line")
            )
        )
        views_publish = val.text.strip()

        val = WebDriverWait(content[i], 5).until(
            EC.presence_of_element_located(
                (By.XPATH, ".//span[@class='style-scope ytd-thumbnail-overlay-time-status-renderer']")
            )
        )
        duration = val.get_attribute('aria-label').strip()

        val = WebDriverWait(content[i], 10).until(
            EC.presence_of_element_located(
                (By.XPATH, ".//a[@class='yt-simple-endpoint style-scope yt-formatted-string']")
            )
        )
        channel = val.get_attribute("href")

        Results.append(  # Storing the results of each video, so we can use it later
            {"URL": str(url),
             "TITLE": str(title),
             "PUBLISH DATE": str(" ".join(views_publish.split()[2:])),
             "VIEWS": str(" ".join(views_publish.split()[:2])),
             "CHANNEL": str(channel),
             "DURATION": str(duration)
             }
        )

keys = list(Results[0].keys())  # getting the head of the File
with open('file.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, keys)
    writer.writeheader()
    for result in Results:
        writer.writerow(result)
    print("Database Updated!")

time.sleep(5)
driver.quit()
