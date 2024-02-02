from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import pandas as pd
import time
import random


class Scrapper:
    def __init__(self):
        self.session = None
        self.driver = webdriver.Edge()
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
        }
        self.data = {
            "lat": "0",
            "lng": "0",
            "radius": "0",
            "product": "0",
            "category": "0",
            "attributes[0][name]": "1",
            "attributes[0][value]": "",
        }
        self.referrer = "https://www.nomination.com/it_it/store-locator/"
        self.referrer_policy = "strict-origin-when-cross-origin"
        self.driver.get("https://www.nomination.com/it_it/")
        header_element = WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.ID, 'maincontent'))
        )
        self.cookies = self.driver.get_cookies()
        self.set_cookies()

    def set_cookies(self):
        self.session = requests.Session()
        for cookie in self.cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

    def get_page_data(self, currPage):
        url = f"https://www.nomination.com/it_it/amlocator/index/ajax/?p={currPage}"
        response = self.session.post(url,
                                     headers=self.headers,
                                     data=self.data,
                                     )
        items_list = json.loads(response.text)['items']
        return items_list, len(items_list)


if __name__ == "__main__":
    scrapper = Scrapper()
    page_index = 0
    page_size = 20
    final_data = []
    while page_size >= 20:
        page_index += 1
        page_data, page_size = scrapper.get_page_data(page_index)
        final_data = final_data + page_data
        time.sleep(random.uniform(0, 2))
    pd.DataFrame(final_data).to_csv('nomination.csv', index=False)
    pd.DataFrame(final_data).to_excel('nomination.xlsx', index=False)
