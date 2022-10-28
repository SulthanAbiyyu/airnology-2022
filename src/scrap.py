import time
import logging
import warnings
import argparse
import bs4 as bs
import pandas as pd
from selenium import webdriver

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)


def scrap(url, chrome_driver_path, output_path, N_SCROLL=100, to_csv=False):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_driver_path, options=options)
    logging.info("opening url..")
    driver.get(url)

    # terbaru
    logging.info("click terbaru..")
    wait = webdriver.support.ui.WebDriverWait(driver, 10)
    menu = wait.until(lambda driver: driver.find_element_by_xpath(
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button'))
    menu.click()
    terbaru = wait.until(lambda driver: driver.find_element_by_xpath(
        '//*[@id="action-menu"]/ul/li[2]'))
    terbaru.click()

    time.sleep(1)

    # scroll down
    logging.info("scrolling down..")
    scrollable_div = driver.find_element_by_css_selector(
        '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf'
    )

    for _ in range(N_SCROLL):
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight',
            scrollable_div
        )
        time.sleep(1)

    # Scraping
    logging.info("get html..")
    resp = bs.BeautifulSoup(driver.page_source, 'lxml')
    reviews = resp.select(
        "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div:nth-child(9)")
    soup_reviews = bs.BeautifulSoup(str(reviews), 'lxml')
    review = soup_reviews.find_all('div', class_='jftiEf fontBodyMedium')

    # Nama
    logging.info("get nama..")
    names = []
    for i in range(len(review)):
        names.append(review[i]['aria-label'])

    # Bintang
    logging.info("get bintang..")
    soup_bapak_bintang = bs.BeautifulSoup(str(review), 'lxml')
    bapak_bintang = soup_bapak_bintang.find_all('div', class_='DU9Pgb')

    bintangs = []
    for i in range(len(bapak_bintang)):
        soup_bintang = bs.BeautifulSoup(str(bapak_bintang[i]), 'lxml')
        bintang = soup_bintang.find('span', class_='kvMYJc')
        bintangs.append(int(bintang['aria-label'].split()[0]))

    # Komentar
    logging.info("get komentar..")
    komens = []
    for i in range(len(review)):
        komens.append(bs.BeautifulSoup(str(review[i]), 'lxml').find(
            'span', class_="wiI7pd").text)

    data = pd.DataFrame({
        "nama": names,
        "bintang": bintangs,
        "komentar": komens
    })

    logging.info("to csv..")
    if to_csv:
        data.to_csv(output_path, index=False)
    else:
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str)
    parser.add_argument('--chrome_driver_path', type=str,
                        default='chromedriver.exe')
    parser.add_argument('--output_path', type=str, default='data.csv')
    parser.add_argument('--N_SCROLL', type=int, default=100)
    args = parser.parse_args()

    scrap(args.url, args.chrome_driver_path, args.output_path, args.N_SCROLL)
