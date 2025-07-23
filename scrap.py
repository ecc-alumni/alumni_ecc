from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

load_dotenv()


email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
# Chemin vers ton chromedriver
service = Service(r"chromedriver-win64\chromedriver.exe")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://outlook.office365.com/mail/")

# Exemple de scraping a = /html/body/nav/div/a[2]
a10 = WebDriverWait(driver, 10)
eform = a10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0116"]')))
eform.send_keys(email)


pform = a10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
pform.send_keys(password)


# //*[@id="rememberMeOptIn-checkbox"]  
check = a10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="idSIButton9"]')))
check.click()


non = a10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="idBtn_Back"]')))
non.click()


time.sleep(10)

nouveau = a10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="114-group"]/div/div[1]/div/div/span/button[1]')))
nouveau.click()

dest = a10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="docking_InitVisiblePart_0"]/div/div[3]/div[1]/div/div[3]/div/span/input')))



time.sleep(13)
driver.get("https://www.linkedin.com/school/ecole-centrale-casablanca/people/")

time.sleep(random.uniform(4, 10))

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll en bas
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Attendre que le contenu se charge
    time.sleep(1.3)
    more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember380"]')))
    more.click()
    time.sleep(random.uniform(0.9, 3))
    # Nouvelle hauteur 
    new_height = driver.execute_script("return document.body.scrollHeight")

    # Si la hauteur n’a pas changé → on est en bas
    if new_height == last_height:
        break

    last_height = new_height
    with open("data.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)


driver.quit()
