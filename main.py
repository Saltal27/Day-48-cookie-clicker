from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = "C:\Development\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(executable_path=chrome_driver_path)
driver = WebDriver(service=service, options=options)
driver.maximize_window()

# opening the website with 10s delay (while the page loads)
driver.get("https://orteil.dashnet.org/cookieclicker/")
time.sleep(10)

# accepting the cookies
accept_cookies = driver.find_element(By.LINK_TEXT, 'Got it!')
accept_cookies.click()

# choosing English as the language with 10s delay (while the page loads)
lang_select = driver.find_element(By.CSS_SELECTOR, '#langSelect-EN')
lang_select.click()
time.sleep(10)


big_cookie = driver.find_element(By.CSS_SELECTOR, '#bigCookie')
cookies_count = driver.find_element(By.CSS_SELECTOR, '#cookies')

item_num = 0
item_count = 0
store_item = driver.find_element(By.CSS_SELECTOR, '#product0')
store_item_price = driver.find_element(By.CSS_SELECTOR, '#productPrice0')

start_time = time.time()
while True:
    big_cookie.click()

    try:
        cookies_count_int = int(cookies_count.text.split(" ")[0])
    except ValueError:
        cookies_count_int = int(cookies_count.text.split(" ")[0].replace(",", "_"))
    store_item_price_int = int(store_item_price.text.replace(",", "_"))

    # check whether you can buy a new item from the store
    if cookies_count_int >= store_item_price_int:
        # buy the current item
        store_item.click()

        # increase the count of the current store item
        item_count += 1

        # refresh the current store item price and the cookies count
        store_item_price = driver.find_element(By.CSS_SELECTOR, f'#productPrice{item_num}')
        cookies_count = driver.find_element(By.CSS_SELECTOR, '#cookies')

    # check if the item count is greater than 5 (we've bought 10 of this item)
    if item_count >= 10:
        # increase the item number (to switch to the next item)
        item_num += 1
        store_item = driver.find_element(By.CSS_SELECTOR, f'#product{item_num}')
        store_item_price = driver.find_element(By.CSS_SELECTOR, f'#productPrice{item_num}')

        # reset the item count to zero (because it's a new item)
        item_count = 0

    # if the code has run for 300 seconds (= 5 minutes); stop the code
    if time.time() - start_time > 300:
        break

# driver.quit()
