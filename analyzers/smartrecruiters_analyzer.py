import re
import simplejson

from analyzers.ats_analyzers import ATSAnalyzer
from utils.page_fetcher import PageFetcher


class SmartRecruiterAnalyzer(ATSAnalyzer):

    @staticmethod
    def get_ats_name():
        return "SmartRecruiters"

    def find_posting_links(self, soup):
        fetcher = PageFetcher()
        offset = 0
        total = 1
        links = []
        while offset < total:
            content = fetcher.fetch_page("{url}?offset={offset}".format(url=self.url, offset=offset))
            content_json = simplejson.loads(content)
            for posting in content_json['content']:
                links.append(posting['ref'])
            total = content_json['totalFound']
            offset += 100
        return links

    def get_direct_regexp(self):
        return re.compile("https?://careers.smartrecruiters.com/\\w+/?")

    def search_for_direct_ats_page_link(self, soup):
        link = soup.find("a", href=re.compile("https?://careers.smartrecruiters.com/\\w+/"))
        if link:
            pattern = re.compile(re.compile("https?://careers.smartrecruiters.com/(\\w+)/?"))
            m = pattern.match(link['href'])
            company = m.group(1)
            return "api.smartrecruiters.com/v1/companies/{domain}/postings".format(domain=company)

    def search_for_job_links(self, soup):
        link = soup.find("a", href=re.compile("https://careers.smartrecruiters.com/\\w+/\\S+"))
        if link:
            pattern = re.compile(re.compile("https://careers?.smartrecruiters.com/(\\w+)"))
            m = pattern.match(link['href'])
            company = m.group(1)
            return "api.smartrecruiters.com/v1/companies/{domain}/postings".format(domain=company)

    def guess_ats_page_url(self):
        return "https://api.smartrecruiters.com/v1/companies/{domain}/postings".format(domain=self.get_domain().capitalize())

