# -*- coding: utf-8 -*-

# collect douban.com data of movie information
import os
import time
from threading import Thread
from time import sleep
from alive_progress import alive_bar
from playwright.sync_api import sync_playwright, BrowserContext, Page

from data.gobledefine import CHROME_PATH, MOVIE_DB, COLLECT_NUMBER
from logs.logRecord import LOG
import database.connect as db

headless = True


class ProgressBar(Thread):
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.index = 0

    def run(self):
        cur = self.index
        with alive_bar(COLLECT_NUMBER) as bar:
            while self.is_running:
                if cur != self.index:
                    bar()
                    cur = self.index

    def stop(self):
        self.is_running = False


class Collect:
    def __init__(self, chrome_path):
        self.chrome_path = chrome_path
        self.browser = None
        self.browser_context = None
        self.page = None
        self.progress_bar = ProgressBar()
        self.web_url = "https://movie.douban.com/tag/#/"

    def run(self):
        args = ["--no-sandbox", "--disable-infobars", "--lang=zh-CN", "--start-maximized"]
        with sync_playwright() as p:
            self.browser = p.chromium.launch(executable_path=self.chrome_path, args=args, headless=headless)
            self.browser_context: BrowserContext = self.browser.new_context(no_viewport=True)
            self.start()
            self.browser.close()

    def start(self):
        print("Initializing data collection")
        self.page: Page = self.browser_context.new_page()
        self.page.goto(self.web_url)
        self.page.wait_for_load_state("networkidle")
        douban_all_div = '//*[@id="app"]/div/div[1]/div[3]/a'
        try:
            for n in range(int(COLLECT_NUMBER / 20)):
                self.page.wait_for_timeout(1000)
                self.page.click("//a[text()='加载更多']")
                self.page.wait_for_load_state("networkidle")
            movies: list = self.page.query_selector_all(douban_all_div)
            movies_url = []
            print("Initializing success")
            self.progress_bar.start()
            i = 1
            for item in movies:
                movies_url.append(str(item.get_property("href")))
                i += 1
                if i > COLLECT_NUMBER:
                    break
            movies_info = self.get_movie_info(movies_url)
            self.progress_bar.stop()
            db.insert_movie_table(MOVIE_DB, movies_info)
        except Exception as e:
            LOG.error(f"{e}")
            self.progress_bar.stop()

    def get_movie_info(self, movies_url) -> dict:
        _page: Page = self.browser_context.new_page()
        movies = {}
        for url in movies_url:
            _page.goto(url)
            movie_name = _page.query_selector("//h1").inner_text()
            more_button = "//a[text()='更多...']"
            if _page.is_visible(more_button):
                _page.click(more_button)
            movie_infos_str = _page.query_selector("//div[@id='info']").inner_text()
            movie_infos = movie_infos_str.split('\n')
            temp = {}
            for item in movie_infos[:-1]:
                _item = item.split(':')
                key = _item[0]
                value = [v.strip() for v in _item[1].split('/')]
                temp[key] = value
            self.progress_bar.index += 1
            review = _page.query_selector("//div[@id='link-report']").inner_text().strip()
            temp['review'] = review
            movies[movie_name] = temp
        return movies

    @staticmethod
    def main():
        c = Collect(CHROME_PATH)
        c.run()


if __name__ == '__main__':
    Collect.main()
