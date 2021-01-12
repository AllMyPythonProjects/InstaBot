from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
from time import sleep

from data import USERNAME, PASSWORD
from cookies.get_cookies import create_browser

url = 'https://www.instagram.com'


def find_hrefs_by_likes(browser: webdriver.Chrome, hashtag: str):
    try:
        browser.get(f'{url}/explore/tags/{hashtag}')
        sleep(random.randint(3, 5))

        hrefs = [item.get_attribute('href')
                 for item in browser.find_elements_by_tag_name('a')
                 if '/p/' in item.get_attribute('href')]
        print('\n'.join(hrefs))

        if len(hrefs) != 0:
            return hrefs

    except Exception as ex:
        print('EXCEPTION in find_hrefs_by_likes', ex, end='\n\n')


def like_posts_by_hashtags(browser: webdriver.Chrome, hashtags):
    try:
        for href in hashtags:
            browser.get(href)
            sleep(random.randint(2, 4))
            like_path = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button'
            browser.find_element_by_xpath(like_path).click()
            sleep(random.randint(2, 4))
    except Exception as ex:
        print('EXCEPTION in like_posts_by_hashtags', ex, end='\n\n')


if __name__ == '__main__':
    driver = create_browser()

    find_hrefs_by_likes(driver, 'cyberpunk')
    like_posts_by_hashtags(driver, 'cyberpunk')

    driver.close()
    driver.quit()
