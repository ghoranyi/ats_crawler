from utils.link_utils import resolve_relative_paths, resolve_one_relative_page
from utils.page_fetcher import PageFetcher

from bs4 import BeautifulSoup
import logging
import re


class JobPageFinder(object):

    def __init__(self, url):
        self.url = url
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.logger.info("Starting job page finder on {orig}".format(orig=self.url))
        fetcher = PageFetcher()
        page_source = fetcher.fetch_page(self.url)
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            return self.find_job_pages(soup)
        except Exception as e:
            success = False
            for link in self.find_alternative_pages(soup):
                self.logger.info("Checking alternative page: {u}".format(u=link))
                try:
                    page_source = fetcher.fetch_page(link)
                    alternative_soup = BeautifulSoup(page_source, 'html.parser')
                    pages = self.find_job_pages(alternative_soup)
                    success = True
                    return pages
                except:
                    continue
            if not success:
                raise e

    def find_job_pages(self, soup):
        job_links = []
        job_links.extend(soup.find_all("a", string=re.compile("careers", re.I), href=True))
        job_links.extend(soup.find_all("a", string=re.compile("join us", re.I), href=True))
        job_links.extend(soup.find_all("a", string=re.compile("jobs?", re.I), href=True))
        job_links.extend(soup.find_all("a", string=re.compile("we'? ?a?re hiring", re.I), href=True))
        job_pages = set()
        for link in job_links:
            job_pages.add(link['href'])
        if not job_pages:
            raise AnalyzerException("Unable to find jobs page")
        final_pages = []
        for page in resolve_relative_paths(self.url, job_pages):
            final_page = self.get_current_openings_page(page)
            self.logger.info("Job page identified: {page}".format(page=final_page))
            final_pages.append(final_page)
        return final_pages

    def find_alternative_pages(self, soup):
        links = []
        links.extend(soup.find_all("a", string=re.compile("more", re.I), href=True))
        links.extend(soup.find_all("a", string=re.compile("about us", re.I), href=True))
        return [resolve_one_relative_page(self.url, link['href']) for link in links]

    def get_current_openings_page(self, job_page):
        fetcher = PageFetcher()
        page_source = fetcher.fetch_page(job_page)
        soup = BeautifulSoup(page_source, 'html.parser')
        current_openings_link = soup.find("a", string=re.compile("openings", re.I), href=True)
        if current_openings_link:
            return resolve_one_relative_page(self.url, current_openings_link['href'])
        else:
            link = soup.find("a", string=re.compile("open positions", re.I), href=True)
            if link:
                return resolve_one_relative_page(self.url, link['href'])
            else:
                return job_page


class AnalyzerException(Exception):
    pass
