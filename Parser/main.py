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

    EXE_PATH = r'chromedriver.exe'
    op = webdriver.ChromeOptions()
    # отключить отображение браузера
    op.add_argument('headless')
    driver = webdriver.Chrome(executable_path=EXE_PATH, options=op)
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


def save_images(links, folder_name, galery_name):
    if str(galery_name) not in os.listdir():
        os.makedirs(os.path.join(os.getcwd(), galery_name))

    if str(folder_name) not in os.listdir(os.path.join(os.getcwd(), galery_name)):
        os.makedirs(os.path.join(os.getcwd(), f'{galery_name}/{str(folder_name)}'))

    count = 0
    for link in links:
        link = link.get("src")
        linked = "https:" + str(link)

        p = requests.get(linked)
        with open(f"{galery_name}/{folder_name}/{count}.jpg", "wb") as file:
            file.write(p.content)
            file.close()
        count += 1


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