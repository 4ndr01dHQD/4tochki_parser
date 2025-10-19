import time

from config import REQUEST_RETRY_TIMEOUT
from logger import logger
from fortochki.exceptions import UnsuccessfullySeriesOfRequests

log = logger.new(component='http_parser')


def retry_error_request(func):
    def wrapper(*args, **kwargs):
        for idx, timeout in enumerate(REQUEST_RETRY_TIMEOUT):
            try:
                response = func(*args, **kwargs)
                if 200 <= response.status_code <= 300:
                    return response
                else:
                    log.error(
                        "Unexpected response by fortochki api.",
                        staus=response.status_code,
                        content=response.content,
                    )
                    time.sleep(timeout)
            except Exception as err:
                log.error(
                    "Unexpected error by fortochki api.",
                    err=err,
                    step=idx + 1,
                    exc_info=True,
                )
                time.sleep(timeout)
                continue
        raise UnsuccessfullySeriesOfRequests("An unsuccessful series of requests.")

    return wrapper
