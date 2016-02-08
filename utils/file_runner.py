import logging

from analyzers.job_page_finder import JobPageFinder
from utils.ats_analyzer_runner import start


class FileRunner(object):

    logger = logging.getLogger(__name__)

    def load_file_and_analyze(self, filename):
        webpages = []
        with open(filename, "r") as ins:
            for line in ins:
                webpages.append("http://" + line.strip())


        output = open("output/output.txt", 'w')
        output.write("Hostname,Has_ATS,ATS,ATS_Pages,Positions,Departments\n")
        output.close()
        tasks = []
        for page in webpages:
            page_result = {}
            self.logger.info("Analyzing {page} page".format(page=page))
            try:
                finder = JobPageFinder(page)
                page_result['job-pages'] = finder.start()
            except Exception as e:
                self.logger.warn("Failed to get job page")
                self.logger.exception(e)
                page_result['job-pages'] = [page]

            for job_page in page_result['job-pages']:
                self.logger.info("Starting celery task")
                tasks.append(start.delay(page, job_page))
        return tasks

