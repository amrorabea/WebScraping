from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import keyboard

email = ""
password = ""

driver = webdriver.Chrome()

# LOGIN FIRST
try:
    driver.get("https://www.linkedin.com/home")
    email_ = driver.find_element(By.XPATH, ".//input[@autocomplete='username']")
    email_.send_keys(email)
    password_ = driver.find_element(By.XPATH, ".//input[@autocomplete='current-password']")
    password_.send_keys(password)
    login = driver.find_element(By.XPATH, ".//button[@type='submit']")
    login.click()
    print("Logged in!")
except:
    print("Logging in error")

target = input("Search:")
target = target.replace(" ", "%20")
driver.get(f"https://www.linkedin.com/jobs/search/?currentJobId=3816341368&keywords={target}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true")
driver.maximize_window()

time.sleep(2)

numOfPages = 3
Results = []

for page in range(numOfPages):
    jobs = driver.find_element(By.XPATH, ".//ul[@class='scaffold-layout__list-container']")
    urls = jobs.find_elements(By.TAG_NAME, "a")
    for url in urls:
        Results.append({"URL": url.get_attribute("href")})
    path = f".//li[@class='artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view']"
    button = driver.find_elements(By.XPATH, path)
    if len(button) < page + 1:
        break
    button[page].click()
    time.sleep(4)

keys = list(Results[0].keys())  # getting the head of the File
with open('file.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, keys)
    writer.writeheader()
    for result in Results:
        writer.writerow(result)
    print("Database Updated!")

time.sleep(5)
driver.quit()
