from bs4 import BeautifulSoup
import re

from analyzers.ats_analyzers import ATSAnalyzer
from utils.page_fetcher import PageFetcher


class LeverAnalyzer(ATSAnalyzer):

    @staticmethod
    def get_ats_name():
        return "Lever"

    @staticmethod
    def find_posting_links(soup):
        links = soup.find_all("a", href=re.compile("https?://jobs\\.lever\\.co/.*/.*"))
        return [link['href'] for link in links]

    @staticmethod
    def get_department(soup, link):
        opening_link = soup.find("a", href=link)
        department = opening_link.find_previous("div", class_="posting-category-title large-category-label")
        if department:
            return department.string

    def get_direct_regexp(self):
        return re.compile('https?://jobs.lever.co/\w+/?$')

    def search_for_job_links(self, soup):
        posting = LeverAnalyzer.find_posting_links(soup)
        if posting:
            offer = posting[0]
            pattern = re.compile('https?://jobs\.lever\.co/(\w*)/.*/')
            m = pattern.match(offer)
            company = m.group(1)
            return "https://jobs.lever.co/{c}/".format(c=company)

    def guess_ats_page_url(self):
        return "https://jobs.lever.co/{domain}/".format(domain=self.get_domain())