import re
import tldextract

from analyzers.ats_analyzers import ATSAnalyzer
from utils.link_utils import resolve_one_relative_page

class JazzAnalyzer(ATSAnalyzer):

    @staticmethod
    def get_ats_name():
        return "Jazz / applytojob.com"

    def find_posting_links(self, soup):
        links = soup.find_all("a", href=re.compile("https?://\\w+\\.applytojob\\.com/apply/\\w+/\\w+"))
        return [resolve_one_relative_page(self.get_ats_url(soup), link['href']) for link in links]


    def get_direct_regexp(self):
        return re.compile("https?://\\w+\\.applytojob\\.com/?$")

    def search_for_job_links(self, soup):
        posting = soup.find("a", href=re.compile("https?://\\w+\\.applytojob\\.com/apply/\\w+/\\w+"))
        if posting:
            pattern = re.compile('(https?://\\w+\\.applytojob\\.com/)')
            m = pattern.match(posting['href'])
            ats_url = m.group(1)
            return ats_url

    def guess_ats_page_url(self):
        return "http://{domain}.applytojob.com".format(domain=self.get_domain())
