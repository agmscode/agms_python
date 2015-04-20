from __future__ import absolute_import
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from agms.exception.not_found_exception import NotFoundException
try:
    import pycurl
except ImportError as e:
    raise NotFoundException(e)


class PycurlClient(object):
    
    def http_do(self, http_verb, url, headers, request_body):
        curl = pycurl.Curl()
        response = StringIO()
        curl.setopt(curl.SSL_VERIFYPEER, 1)
        curl.setopt(curl.SSL_VERIFYHOST, 2)
        curl.setopt(curl.URL, url)
        curl.setopt(curl.ENCODING, 'gzip')
        curl.setopt(curl.WRITEFUNCTION, response.write)
        curl.setopt(curl.FOLLOWLOCATION, 1)
        curl.setopt(curl.HTTPHEADER, self._format_headers(headers))
        self._set_request_method_and_body(curl, http_verb, request_body)

        curl.perform()

        status = curl.getinfo(curl.HTTP_CODE)
        response = response.getvalue()
        return [status, response]

    def _set_request_method_and_body(self, curl, method, body):
        if method == "GET":
            curl.setopt(curl.HTTPGET, 1)
        elif method == "POST":
            curl.setopt(curl.POST, 1)
            curl.setopt(curl.POSTFIELDSIZE, len(body))
        elif method == "PUT":
            curl.setopt(curl.PUT, 1)
            curl.setopt(curl.INFILESIZE, len(body))
        elif method == "DELETE":
            curl.setopt(curl.CUSTOMREQUEST, "DELETE")

        if body:
            curl.setopt(curl.READFUNCTION, StringIO(body).read)

    def _format_headers(self, headers):
        return [str(key) + ": " + str(value) for key, value in headers.items()]
