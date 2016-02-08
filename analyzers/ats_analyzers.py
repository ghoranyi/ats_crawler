from bs4 import BeautifulSoup
import logging
import tldextract

from utils.page_fetcher import PageFetcher, check_page_exists


class ATSAnalyzer(object):

    def __init__(self, origin, job_page):
        self.origin = origin
        self.url = job_page
        self.logger = logging.getLogger(__name__)
        self._ats_url_cache = None

    def fetch_page(self):
        fetcher = PageFetcher()
        job_page_content = fetcher.fetch_page(self.url)
        soup = BeautifulSoup(job_page_content, 'html.parser')
        return soup

    def start(self):
        ats_result = {}
        self.logger.info("Probing {analyzer} ATS Analyzer on {u}".format(analyzer=self.get_ats_name(), u=self.url))
        soup = self.fetch_page()
        ats_page = self.get_ats_url(soup)
        if ats_page:
            self.logger.info("{ats} ATS page identified: {url}".format(
                ats=self.get_ats_name(),
                url=ats_page
            ))
            ats_result['ats-pages'] = ats_page
            ats_result['ats'] = self.get_ats_name()
            self.url = ats_page
            soup = self.fetch_page()
            posting_links = self.find_posting_links(soup)
            if posting_links:
                self.logger.info("{ats} ATS identified for {origin} with {count} postings".format(
                        ats=self.get_ats_name(),
                        origin=self.origin,
                        count=len(posting_links)
                ))
                ats_result['positions'] = []
                ats_result['departments'] = []
                for link in posting_links:
                    ats_result['positions'].append(link)
                    department = self.get_department(soup, link)
                    if department:
                        self.logger.debug("Department identified for posting: {dep}".format(dep=department))
                        ats_result['departments'].append(department)
            else:
                self.logger.info("No offering found on {url}".format(url=ats_page))
        return ats_result

    @staticmethod
    def get_ats_name(self):
        raise Exception("Not implemented")

    @staticmethod
    def find_posting_links(soup):
        raise Exception("Not implemented")

    def search_for_direct_ats_page_link(self, soup):
        link = soup.find("a", href=self.get_direct_regexp())
        if link:
            return link['href']

    def search_for_job_links(self, soup):
        raise Exception("Not implemented")

    def guess_ats_page_url(self):
        raise Exception("Not implemented")

    @staticmethod
    def get_department(soup, link):
        return None

    def get_ats_url(self, soup):
        if not self._ats_url_cache:
            pattern = self.get_direct_regexp()
            if pattern.match(self.url):
                self._ats_url_cache = self.url
            if not self._ats_url_cache:
                self._ats_url_cache = self.search_for_direct_ats_page_link(soup)
            if not self._ats_url_cache:
                self._ats_url_cache = self.search_for_job_links(soup)
            if not self._ats_url_cache:
                self._ats_url_cache = self.try_direct_ats_page_load()
        return self._ats_url_cache

    def try_direct_ats_page_load(self):
        domain = self.guess_ats_page_url()
        if check_page_exists(domain):
            return domain

    def get_domain(self):
        split = tldextract.extract(self.origin)
        return split.domain