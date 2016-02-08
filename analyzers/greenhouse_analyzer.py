import re

from analyzers.ats_analyzers import ATSAnalyzer
from utils.link_utils import resolve_one_relative_page


class GreenhouseAnalyzer(ATSAnalyzer):

    ATS_PAGE_REGEXP = re.compile('https?://boards\\.greenhouse\\.io/\\w+')

    @staticmethod
    def get_ats_name():
        return "Greenhouse"

    def find_posting_links(self, soup):
        links = soup.find_all("a", href=re.compile("/\\w+/jobs/[0-9]+"))
        return [resolve_one_relative_page(self.get_ats_url(soup), link['href']) for link in links]

    @staticmethod
    def get_department(soup, link):
        pattern = re.compile("https?://boards\\.greenhouse\\.io(/\\w+/jobs/\\d+)")
        m = pattern.match(link)
        opening_link = soup.find("a", href=m.group(1))
        department = opening_link.find_previous("h2")
        if department:
            return department.string

    def get_direct_regexp(self):
        return re.compile('https?://boards\\.greenhouse\\.io/\\w+/?$')

    def search_for_job_links(self, soup):
        posting = soup.find("a", href=re.compile("https?://boards\\.greenhouse\\.io/\\w+/jobs/\\d+"))
        if posting:
            pattern = re.compile('https?://boards\\.greenhouse\\.io/\\w+')
            m = pattern.match(posting['href'])
            ats_url = m.group(0)
            return ats_url

    def guess_ats_page_url(self):
        return "https://boards.greenhouse.io/{domain}/".format(domain=self.get_domain())

