from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from config import userName, password
import time
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from . import headers


def gettingHeaders(hashtag):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        options=chrome_options)
    driver.implicitly_wait(10)
    driver.get("https://instagram.com/accounts/login")
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input").send_keys(userName)
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(5)
    driver.implicitly_wait(10)
    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}")
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]")
    flag = 0
    for request in driver.requests:
        if request.response and "instagram.com/api/v1/tags/web_info/?tag_name" in request.url and flag != 1:
            flag = 1
            with open('instagram/headers.py', 'w') as f:
                f.write('headersChrome = {\n')
                for header in request.headers:
                    header_answ = str(request.headers[f'{header}'])
                    json_link = f"'{str(header)}': '{header_answ}',\n"
                    f.write(str(json_link))
                f.write('}')
        elif flag == 1:
            break
    driver.quit()
