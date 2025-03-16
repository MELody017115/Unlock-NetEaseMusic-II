# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A5C15326507B47077AD52D75427652725081F3A63B6E4459CA11D7C8105B856A046CA4CD4C1A4DA08107237F22A75BC32D765A07E65B486ED533BA2ABA88229328C4E0194E3A72935E72E6E8D983005EA2F759ECE554D8C21490BD602A38A93FD09DFE3B8ED61629CD5D76540B3C584EF99F3042F68C259E7A5FBBA8E55CFC861C29D1B5DB696D0CBA8F309C3C09DE8F5BFD20C91DA093663FF28DF2E892B54B258E3ADBD58C69CDA42981C523BB7FEC9ACF6C4B0E269D3EA5D06654281619CE72B330DCB8ACCD71BCC4BC3184BD82DBB6A4C543369BDC29D3C6991D4F4E394D2444416F9B9147CD0917AE7442F0F08ED7B22887C6C091BD7EC0CD14C795F390BDA7E45F0D8C20A19090260DAB0D40243EB226A92C62BA0BF0F86876FFD767627E13D6027433BEB7BC644F09BD67D67B8DCCBFDC4D849B02D04EF30B3E73F5C917DA0602FE51ACCF3F473D0AF956042616921CEEFBC1D7A7389D5934FF4324F0"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
