# -*- coding: utf-8 -*-

# collect douban.com data of movie information

from playwright.sync_api import sync_playwright, BrowserContext, Page

from data.gobledefine import CHROME_PATH


class Collect:
    def __init__(self, chrome_path):
        self.chrome_path = chrome_path
        self.browser = None
        self.browser_context = None
        self.page = None
        self.web_url = "https://movie.douban.com/review/best/?start=0"

    def run(self):
        args = ["--no-sandbox", "--disable-infobars", "--lang=zh-CN", "--start-maximized"]
        with sync_playwright() as p:
            self.browser = p.chromium.launch(executable_path=self.chrome_path, args=args, headless=False)
            self.browser_context: BrowserContext = self.browser.new_context(no_viewport=True)
            self.start()

    def start(self):
        self.page: Page = self.browser_context.new_page()
        self.page.goto(self.web_url)

    @staticmethod
    def test():
        c = Collect(CHROME_PATH)
        c.run()


if __name__ == '__main__':
    Collect.test()
