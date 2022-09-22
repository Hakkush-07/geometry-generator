import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://artofproblemsolving.com/community/"

class Contest:
    def __init__(self, code="c3080392"):
        """
        code: aops code of the contest
        """
        self.code = code
        self.url = f"{base_url}{code}"
        self.title, self.problems = self.name_and_problems()
    
    def __repr__(self):
        return f"{self.name}, {self.url}"
    
    def name_and_problems(self):
        """
        scrapes the name and the problems of the contest from aops
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        time.sleep(5)
        html = driver.page_source
        driver.close()
        problems = []
        soup = BeautifulSoup(html, "lxml")
        title = soup.find("div", {"class": "cmty-category-cell-title"}).text
        items = soup.find_all("div", {"class": "cmty-view-posts-item"})
        for item in items:
            item_label = item.find("div", {"class": "cmty-view-post-item-label"})
            if item_label:
                item_text = item.find("div", {"class": "cmty-view-post-item-text"})
                for image in item_text("img"):
                    image.replace_with(image["alt"])
                item_link = item.find("div", {"class": "cmty-view-post-topic-link"}).find("a")
                problems.append([item_label.text, item_text.text, item_link["href"]])
        return title, problems
    
    def save(self):
        """
        saves the problems of the contest to an excel file in outputs/contests folder
        """
        df = pd.DataFrame(self.problems)
        df.columns = ["Label", "Text", "Link"]
        df.to_excel(f"outputs/contests/{self.code}.xlsx", index=False)
