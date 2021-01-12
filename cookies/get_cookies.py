import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
from time import sleep
import json

from data import USERNAME, PASSWORD, USER_AGENT

url = 'https://www.instagram.com'

project_path = os.path.abspath('main.py')
project_path = project_path[:project_path.rfind('/') + 1]


def login(browser: webdriver.Chrome, username: str, password: str):
    """
    The function login into instagram account and gets cookie
    for following sessions.
    """
    try:
        browser.get(url)
        sleep(3)

        name_input = browser.find_element_by_name('username')
        name_input.clear()
        name_input.send_keys(username)
        sleep(random.randint(2, 4))

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)
        sleep(random.randint(2, 4))

        password_input.send_keys(Keys.ENTER)
        sleep(random.randint(4, 6))

        cookies = browser.get_cookies()
        with open(project_path + 'cookies/cookies.json', 'w') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
            print("Cookies were successfully got")

    except Exception as ex:
        print('EXCEPTION in login', ex, end='\n\n')


def create_browser() -> webdriver.Chrome:
    """
    Create and return browser for using instagram with your account
    """
    options = webdriver.ChromeOptions()
    options.add_argument(USER_AGENT)
    browser = webdriver.Chrome(
        executable_path=project_path + 'driver/chromedriver',
        options=options
    )
    if not os.path.exists(project_path + 'cookies/cookies.json'):
        tmp_options = webdriver.ChromeOptions()
        tmp_options.add_argument(USER_AGENT)
        tmp_browser = webdriver.Chrome(
            executable_path=project_path + 'driver/chromedriver',
            options=options
        )
        login(tmp_browser, USERNAME, PASSWORD)
        tmp_browser.close()
        tmp_browser.quit()
    browser.get(url)
    for cookie in json.load(open(project_path + 'cookies/cookies.json')):
        browser.add_cookie(cookie)
    sleep(random.randint(3, 5))
    browser.refresh()
    return browser
