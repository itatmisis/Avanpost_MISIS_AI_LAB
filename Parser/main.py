from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
import time
import sys
import requests


def get_page_selenium(object):
    url = f'https://yandex.ru/images/search?text={object}&from=tabbar'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome(executable_path=EXE_PATH, options=op)
    driver.get(url)

    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script(f"window.scrollTo({last_height}, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

    page = driver.page_source
    return page


def get_links(page):
    soap = BeautifulSoup(page, "html.parser")
    links = soap.find_all("img", class_="serp-item__thumb justifier__thumb")
    return links


def save_images(links, folder_name, amount=100):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    count = 0
    for link in links:
        link = link.get("src")
        linked = "https:" + str(link)

        p = requests.get(linked)

        with open(f"{folder_name}/{count}.jpg", "wb") as file:
            file.write(p.content)
            file.close()
        count += 1
        if count >= amount:
            break


# objects = {'газонокосилка': 'lawnmower',
#            'трактор': 'tractor',
#            'велосипед': 'bicycle',
#            'сноуборд': 'snowboarding',
#            'лыжи':'ski',
#            'грузовик': 'truck',
#            'газель': 'gazelle',
#            'поезд': 'train',
#            'самосвал': 'dump truck',
#            'лошадь': 'horse',
# }

# for object, folder_name in objects.items():
#     save_images(get_links(get_page_selenium(object)), folder_name=folder_name)


def main(object, folder_name, galery_name):
    save_images(get_links(get_page_selenium(object)), folder_name=folder_name, galery_name=galery_name)


if __name__ == '__main__':
    object = str(sys.argv[1])
    folder_name = str(sys.argv[2])
    galery_name = str(sys.argv[3])

    main(object, folder_name, galery_name)