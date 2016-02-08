import re

from analyzers.ats_analyzers import ATSAnalyzer
from utils.link_utils import resolve_one_relative_page
from utils.page_fetcher import resolve_short_link


class WorkableAnalyzer(ATSAnalyzer):

    @staticmethod
    def get_ats_name():
        return "Workable"

    def find_posting_links(self, soup):
        links = soup.find_all("a", href=re.compile("/jobs/[0-9]+"))
        return [resolve_one_relative_page(self.get_ats_url(soup), link['href']) for link in links]

    def get_direct_regexp(self):
        return re.compile("https?://\\S+\\.workable\\.com/?$")

    def search_for_job_links(self, soup):
        posting = soup.find("a", href=re.compile("https?://\\S+\\.workable\\.com/jobs/[0-9]+"))
        if posting:
            pattern = re.compile("(https?://\\S+\\.workable\\.com)/jobs/[0-9]+")
            m = pattern.match(posting['href'])
            return m.group(1)
        else:
            posting = soup.find("a", href=re.compile("https?://(www\\.)?workable\\.com/j/\\w+"))
            if posting:
                short_link = posting['href']
                pattern = re.compile("(https?://\\S+\\.workable\\.com)/jobs/[0-9]+")
                m = pattern.match(resolve_short_link(short_link))
                return m.group(1)

    def guess_ats_page_url(self):
        return "https://{domain}.workable.com".format(domain=self.get_domain())

