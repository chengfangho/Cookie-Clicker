from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

PATH = "/Users/cfho/Desktop/git/Selenium/selenium/chromedriver"
URL = "https://orteil.dashnet.org/experiments/cookie/"
 
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(PATH)
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items][:8]


cookie = driver.find_element(By.ID, "cookie")

timeout = time.time() + 60
while True:
    cookie.click()
    if time.time() > timeout:
        prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = [price.text.split('-')[1].strip()  for price in prices if price.text != ""]
        items = {}
        for i in range(len(item_ids)):
            items[item_ids[i]] = int(item_prices[i].replace(",", ""))
        print(items)
        money = int(driver.find_element(By.ID, "money").text.replace(",", ""))
        affordables = {}
        for id, price in items.items():
            if money >= price:
                affordables[price] = id
        print(f"Affordable: {affordables}, Current Money: {money}")
        buy = max(affordables)
        print(affordables[buy])
        affordable = driver.find_element(By.ID, affordables[buy])
        affordable.click()
        timeout = time.time() + 60
    
