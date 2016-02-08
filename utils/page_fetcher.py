import dryscrape
import gzip
import logging
import pycurl
import robotparser
from StringIO import StringIO
import urlparse
import urllib2


USER_AGENT = "ATS_CRAWLER (Version 1.0)"


class FetchException(Exception):
    pass


def check_page_exists(url):
    try:
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.USERAGENT, USER_AGENT)
        c.perform()
        response_code = c.getinfo(c.RESPONSE_CODE)
        c.close()
        if buffer.getvalue() == '{\n' + \
            '  "offset": 0,\n' + \
            '  "limit": 100,\n' + \
            '  "totalFound": 0,\n' + \
            '  "content": []\n' + \
                '}':
            return False
        if buffer.getvalue() == "<h1>This account is not active</h1>":
            return False
        return response_code == 200
    except:
        return False


def resolve_short_link(short_link):
    try:
        content = StringIO()
        header = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, short_link)
        c.setopt(c.WRITEDATA, content)
        c.setopt(c.USERAGENT, USER_AGENT)
        c.setopt(c.HEADERFUNCTION, header.write)
        c.perform()
        response_code = c.getinfo(c.RESPONSE_CODE)
        c.close()
        if response_code != 301 and response_code != 302:
            return short_link
        header.seek(0)
        for l in header:
            if "Location" in l:
                return l.split(": ")[-1]
    except:
        return short_link



class PageFetcher(object):

    logger = logging.getLogger(__name__)
    dryscrape.start_xvfb()

    def _can_fetch(self, url):
        return True
        robots_file = self._get_robots_file_url(url)
        rp = robotparser.RobotFileParser()
        rp.set_url(robots_file)
        rp.read()
        return rp.can_fetch(USER_AGENT, url)

    def _get_robots_file_url(self, url):
        hostname = urlparse.urlparse(url).hostname
        robots_file = "http://{hostname}/robots.txt".format(hostname=hostname)
        self.logger.debug("Robots file: {r}".format(r=robots_file))
        return robots_file

    def _get_content(self, response):
        if response.info().get('Content-Encoding') == 'gzip':
            self.logger.debug("Decompressing gzip content")
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            return f.read()
        return response.read()

    def fetch_page(self, url):
        corrected_url = url
        if not url.startswith("http://") and not url.startswith("https://"):
            corrected_url = "http://{u}".format(u=url)
        self.logger.debug("Fetching page: {u}".format(u = corrected_url))
        cache = get_page_cache()
        cached_content = cache.get_cached_content(corrected_url)
        if cached_content:
            self.logger.debug("Page served from cache")
            return cached_content
        if not self._can_fetch(corrected_url):
            self.logger.warn("Unable to fetch, disallowed by robots.txt")
            raise FetchException("Disallowed by robots.txt")
        try:
            parsed_url = urlparse.urlparse(url)
            base_url = parsed_url.scheme + "://" + parsed_url.hostname
            path = parsed_url.path
            sess = dryscrape.Session(base_url=base_url)
            sess.set_attribute('auto_load_images', False)
            sess.visit(path)
            content = sess.body()
            cache.save_content(corrected_url, content)
            return content
        except Exception as e:
            raise FetchException("Failed to load the page", e)


class PageCache(object):
    cache = dict()

    def get_cached_content(self, key):
        if key in self.cache:
            return self.cache[key]
        return None

    def save_content(self, key, content):
        self.cache[key] = content

_page_cache = PageCache()


def get_page_cache():
    return _page_cache