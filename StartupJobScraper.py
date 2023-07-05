from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.common.exceptions import ElementNotInteractableException

from selenium.webdriver.common.by import By


class StartupJobsScraper:
    def __init__(self, jobs_needed=10, topic="Data Science", browser_vis=True):
        self.jobs_collected = 0
        self.jobs_needed = jobs_needed
        self.data = []
        self.topic = topic

        self.base_url = "https://startup.jobs/"

        c_options = webdriver.ChromeOptions()
        c_options.add_argument('--incognito')
        c_options.add_argument('--disable-geolocation')

        sel_service = Service(r"C:\Users\Dilshaan Sandhu\Downloads\chromedriver_win32\chromedriver.exe")
        self.driver = webdriver.Chrome(service=sel_service, options=c_options)

        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, "query").send_keys(self.topic)

    def get_page_links(self):
        time.sleep(2)
        try:
            while self.jobs_needed > self.jobs_collected:
                print(f"Number of jobs collected: {self.jobs_collected}")
                print(f"{self.jobs_collected / self.jobs_needed * 100}% Completed", end="\n\n")

                view_button = self.driver.find_element(By.XPATH, '//*[@id="posts-index"]/section[2]/div/div/a')

                b_soup = BeautifulSoup(self.driver.page_source, 'html.parser')

                job_posts = b_soup.find('div', class_="divide-gray-100", attrs={'data-search-target': 'hits'}).find_all(
                    'div', class_="grid-cols-6", attrs={"data-mark-visited-links-target": "container"}
                )

                for h_job in job_posts:
                    job_aHTML = h_job.find('a', class_="pt-1", attrs={"data-mark-visited-links-target": "anchor"})

                    job_dict = {
                        "Link": self.base_url + job_aHTML["href"],
                        "Tags": ["Tag1", "Tag2"]  # TODO Figure out a way to collect tag names
                    }

                    self.data.append(job_dict)
                    self.jobs_collected += 1

                self.driver.execute_script("arguments[0].scrollIntoView();", view_button)
                view_button.click()
                time.sleep(2)
        except ElementNotInteractableException:
            print("The max number of jobs the site has provided is", self.jobs_collected)

        self.data = self.data[:self.jobs_needed] # only keeps the number of jobs to the number specified
        print("Link Collection Completed")
        print("Number of job links collected:", self.jobs_collected)

    def scrape_page(self):
        for job_d in self.data:
            self.driver.get(job_d["Link"])
            # TODO Scrape Description, Company Name, Location, Full-Time
            # Update self.data

    def save_to_csv(self):
        # My suggestion: Used pandas dataframe


job_scraper = StartupJobsScraper(jobs_needed=99)
job_scraper.get_page_links()
job_scraper.scrape_page()

# TODO Set up multiple scrapers to run at the same time HINT: Multiprocessing? Threading?


