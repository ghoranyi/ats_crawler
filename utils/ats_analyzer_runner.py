from celery import Celery
import logging

from analyzers.greenhouse_analyzer import GreenhouseAnalyzer
from analyzers.jazz_analyzer import JazzAnalyzer
from analyzers.lever_analyzer import LeverAnalyzer
from analyzers.recruiterbox_analyzer import RecruiterboxAnalyzer
from analyzers.smartrecruiters_analyzer import SmartRecruiterAnalyzer
from analyzers.workable_analyzer import WorkableAnalyzer


app = Celery('utils.ats_analyzer_runner', broker='redis://redis:6379/0', backend='redis://redis:6379/1')


logger = logging.getLogger(__name__)
analyzers = [
    LeverAnalyzer,
    WorkableAnalyzer,
    GreenhouseAnalyzer,
    JazzAnalyzer,
    RecruiterboxAnalyzer,
    SmartRecruiterAnalyzer
]


@app.task
def start(origin, job_page):
    logger.info("Starting analyzers on {job}".format(job=job_page))
    merged_result = {
        "ats": [],
        "ats-pages": [],
        "positions": [],
        "departments": []
    }
    for analyzer in analyzers:
        try:
            instance = analyzer(origin, job_page)
            result = instance.start()
            if 'ats' in result:
                merged_result['ats'].append(result['ats'])
            if 'ats-pages' in result:
                merged_result['ats-pages'].append(result['ats-pages'])
            if 'positions' in result:
                merged_result["positions"].extend(result['positions'])
            if 'departments' in result:
                merged_result["departments"].extend(result['departments'])
        except Exception as e:
            logger.warn("ATS analyzer ({name}) has failed".format(name=analyzer.get_ats_name()))
            logger.exception(e)
    output = open("output/output.txt", 'a')
    if merged_result['ats']:
        has_ats="TRUE"
    else:
        has_ats="FALSE"
    output.write("{hostname},{has_ats},{ats},{ats_pages},{positions},{departments}\n".format(
        hostname=origin,
        has_ats=has_ats,
        ats=list_formatter(merged_result['ats']),
        ats_pages=list_formatter(merged_result['ats-pages']),
        positions=len(merged_result['positions']),
        departments=list_formatter(merged_result["departments"])
    ))
    output.close()


def list_formatter(list):
    return ";".join([item[0] for item in list])