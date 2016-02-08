from bs4 import BeautifulSoup
import re

from analyzers.ats_analyzers import ATSAnalyzer
from utils.link_utils import resolve_one_relative_page


class RecruiterboxAnalyzer(ATSAnalyzer):

    @staticmethod
    def get_ats_name():
        return "Recruiterbox"

    def find_posting_links(self, soup):
        links = soup.find_all("a", href=re.compile("/jobs/\\w+"))
        return [resolve_one_relative_page(self.get_ats_url(soup), link['href']) for link in links]

    @staticmethod
    def get_department(soup, link):
        pattern = re.compile("https?://\\w+\\.recruiterbox\\.com(/jobs/\\w+/?)")
        m = pattern.match(link)
        opening_link = soup.find("a", href=m.group(1))
        department = opening_link.find_previous("h2", class_="group-header")
        if department:
            return department.string

    def get_direct_regexp(self):
        return re.compile("https?://\\w+\\.recruiterbox\\.com/?$")

    def search_for_job_links(self, soup):
        posting = soup.find("a", href=re.compile("https?://\\w+\\.recruiterbox\\.com/jobs/\\w+"))
        if posting:
            pattern = re.compile("https?://\\w+\\.recruiterbox.com")
            m = pattern.match(posting['href'])
            return m.group(0)

    def guess_ats_page_url(self):
        return "https://{domain}.recruiterbox.com".format(domain=self.get_domain())

