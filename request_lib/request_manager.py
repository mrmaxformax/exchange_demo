""" This module implements the wrapper class for accessing the services
 using REST API calls"""

import urllib3
from requests import Response, Session

from utilities.logging import LOG
from request_lib.retry import retry
from request_lib.request_property import RequestProperty
from request_lib.response_property import ResponseProperty


class RequestManager:
    """
    Class to implement this fixture
    .. warning::
       To maintain test independence, instances of this class should be considered immutable
       by test developers.
    """

    __slots__ = ["s"]

    def __init__(self):
        self.s = Session()

    @retry(Exception, tries=3, delay=float(3), backoff=2, response_property=ResponseProperty)
    def send_request(self, request_property: RequestProperty, verify: bool = True) -> ResponseProperty:

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.__build_log(request_property)
        request = getattr(self, f"_{request_property.request_type}")
        response = request(request_property, verify)

        LOG.debug(f"Response: {response}")
        response.raise_for_status()
        response_object = ResponseProperty(
            response=response, status_code=response.status_code, response_time=response.elapsed.total_seconds()
        )
        return response_object

    def close(self):
        self.s.close()

    def _get(self, request_property: RequestProperty, verify: bool) -> Response:
        return self.s.get(
            url=request_property.base_url,
            params=request_property.params,
            headers=request_property.headers,
            verify=verify,
        )

    def _post(self, request_property: RequestProperty, verify: bool) -> Response:
        return self.s.post(
            url=request_property.base_url,
            params=request_property.params,
            json=request_property.payload,
            data=request_property.data,
            headers=request_property.headers,
            files=request_property.file,
            verify=verify,
        )

    @staticmethod
    def __build_log(request_property: RequestProperty):
        LOG.debug(
            f"""
                ***********************************************************
                REQUEST: {request_property.request_type}
                URL: {request_property.base_url}
                PARAMS: {request_property.params}
                PAYLOAD: {request_property.payload}
                DATA: {request_property.data}
                HEADERS: {request_property.headers}
                FILES: {request_property.file}
                ***********************************************************
                """
        )
