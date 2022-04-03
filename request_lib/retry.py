import time
from functools import wraps
from utilities.logging import LOG


def retry(exceptions, tries, delay, backoff, response_property):

    """
    exceptions: the exceptions raised with request session, may be a tuple
    tries: int
    delay: time in seconds float
    backoff: int=2 will double of the delay time each retry

    """

    def deco_retry(func):
        @wraps(func)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    mtries -= 1
                    if mtries > 0:
                        msg = f"{str(e)}, Retrying in {float(mdelay)} seconds....."
                        LOG.error(msg)
                        time.sleep(mdelay)
                    else:
                        msg = f"{str(e)}, Sorry, no more retries for today....."
                        LOG.error(msg)
                    mdelay *= backoff
                    response_property.exception = e
                    response_property.status_code = e.response.status_code
                    response_property.response = e.response
                    try:
                        response_property.response_json = e.response.json()
                    except:
                        pass
            return response_property

        return f_retry

    return deco_retry
