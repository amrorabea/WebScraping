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

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# LOGIN FIRST
try:
    driver.get("GROUP LINK GOES HERE")
    driver.maximize_window()
    time.sleep(5)
    email_ = driver.find_element(By.XPATH, ".//input[@type='email']")
    email_.send_keys(email)
    password_ = driver.find_element(By.XPATH, ".//input[@type='password']")
    password_.send_keys(password)
    login = driver.find_element(By.XPATH, ".//button[@type='submit']")
    login.click()
    print("Logged in!")
except:
    print("Logging in error")
    quit()

time.sleep(5)
Results = []

NumOfScrolls = 100
while NumOfScrolls:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(3)
    NumOfScrolls -= 1
time.sleep(2)

urls = driver.find_elements(By.XPATH, ".//a[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f']")

for url in urls:
    Results.append({"Name": url.text.strip(), "URL": url.get_attribute("href")})

keys = list(Results[0].keys())  # getting the head of the File
with open('file.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, keys)
    writer.writeheader()
    for result in Results:
        writer.writerow(result)
    print("Database Updated!")

time.sleep(5)
driver.quit()
