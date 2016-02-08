from page_fetcher import PageFetcher

from unittest import TestCase

class PageFetcherTestSuite(TestCase):

    def setUp(self):
        self.page_fetcher = PageFetcher()

    def test_robots_url_getter(self):
        self.assertEqual("http://pipetop.com/robots.txt", self.page_fetcher._get_robots_file_url("http://pipetop.com"))
        self.assertEqual("http://pipetop.com/robots.txt", self.page_fetcher._get_robots_file_url("http://pipetop.com/"))
        self.assertEqual("http://pipetop.com/robots.txt", self.page_fetcher._get_robots_file_url("http://pipetop.com/customer-cases"))
