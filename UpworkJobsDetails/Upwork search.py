from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()

target = input("Search:")
target = target.replace(" ", "%20")
driver.get(f"https://www.upwork.com/nx/search/jobs/?nbs=1&q={target}&sort=recency")
time.sleep(10)
content = driver.find_elements(By.XPATH, ".//article[@class='job-tile cursor-pointer px-md-4 air3-card air3-card-list px-4x']")

Results = []


def replacement(Element):
    Element = Element.replace("Less than ", "<")
    Element = Element.replace("More than ", ">")
    Element = Element.replace("not_sure", "-")
    return Element


for element in content:

    title = WebDriverWait(element, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//h2[@class='h5 mb-0 mr-2 job-tile-title']")
        )
    ).text

    url = element.find_element(By.XPATH, ".//a[@data-test='UpLink']").get_attribute("href")

    post_date = element.find_element(By.XPATH, ".//small[@class='text-light mb-1']").text
    post_date = post_date[7:]
    description = element.find_element(By.XPATH, ".//p[@class='mb-0']").text
    # location = WebDriverWait(element, 60).until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, ".//li[@data-test='location']")
    #     )
    # ).text
    budget_ExpLevel_duration = element.find_element(By.XPATH, ".//ul[@data-test='JobInfoFeatures']").\
        find_elements(By.TAG_NAME, "strong")

    pay_type = budget_ExpLevel_duration[0].text.split()[0]
    pay_type = pay_type if pay_type[-1] != ':' else pay_type[:-1]
    exp_level = budget_ExpLevel_duration[1].text.split()[0]
    duration = budget_ExpLevel_duration[3].text
    budget = "-"
    if pay_type == "Hourly":
        tmp = duration.split()
        duration = " ".join(tmp[:4])[:-1]
        budget = " ".join(tmp[4:])
    else:
        budget = duration[1:]
        duration = "-"
    budget = replacement(budget)
    duration = replacement(duration)

    Results.append(
        {
            "Title": title,
            "URL": url,
            "Post Date": post_date,
            "Payment Type": pay_type,
            "Experience Level": exp_level,
            "Duration": duration,
            "Budget": budget,
            "Description": description
        }
    )

keys = list(Results[0].keys())  # getting the head of the File
with open('file.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, keys)
    writer.writeheader()
    for result in Results:
        writer.writerow(result)
    print("Database Updated!")

time.sleep(3)
