import requests
import re
import logging
import json
import urllib3


class Requesti():
    def __init__(self, capture_file, exact_urls=True):
        """ New Requesti instance using a packet capture file

        Arguments:
            capture_file: A path to a .har file
            exact_urls:
                If False, preform some preprocesing of URLs to match against
                remove http[s]://www and trailing /, lowercase.
                Not implemented
        """
        self.exact_urls = exact_urls
        if capture_file.endswith(".har"):
            with open(capture_file, "r") as fp:
                self.capture = json.load(fp)['log']['entries']

        elif capture_file.endswith(".cap"):
            raise NotImplementedError(".cap files not implemented yet")
        else:
            raise ValueError("Unknown filetype {}".format(capture_file))

    def find_packets(self, url_regex, params=None):
        """ Searches capture for a packet matching url, and optionally params

        Arguments:
            url_regex: match only packets with url matching this regex statement
            params:
                an optional dictionary of additional http request header filters
                Not implemented!
        Returns: 
            A list of matching request/response pairs from capture file
        """
        if params:
            raise NotImplementedError("Parameter limiting is not Implmented")
        matched = [
            e for e in self.capture
            if re.match(url_regex, e['request']['url'])
        ]
        return matched

    @staticmethod
    def populate_response(response_dict):
        """ Populate a requests.Response object from a dictionary

        Arguments:
            response_dict:
                A dictionary of response in the format of a har file entry
        Returns: A requests.Response object with those populated values
        """
        content_text = response_dict['content']['text']
        headers = response_dict['headers']
        # name/value list into key:value dict
        headers = {h['name']: h['value'] for h in headers}
        status = response_dict['status']
        cookies = response_dict['cookies']
        ret = requests.Response()
        resp = urllib3.response.HTTPResponse(
            content_text,
            headers=headers,
            status=status)
        ret.raw = resp
        ret.status_code = status
        ret.headers = headers
        ret.cookies = cookies
        # Can't easily override requests.Response.text >:( !!!
        return ret

    def mock_get(self, url, params=None, **kwargs):
        """ Mock requests.get calls by replying matched responses from capture.

        Arguments:
            url: match against this url
            params:
                optional, containing these params
                Not implemented
        Returns:
            A requests.Response object from capture
        Raise:
            ResourceWarning: If no matching packets found in capture.
            NotImplementedError: Anything other than exact matching of URLs
        """
        if self.exact_urls and not params:
            matched = [e for e in self.capture if e['request']['url'] == url]
            if len(matched) == 1:
                resp_dict = matched[0]['response']
                resp = populate_response(resp_dict)
            if len(matched) == 0:
                raise Warning("No packets matched url {}".format(url))
            if len(matched > 1):
                logging.debug(
                    "request for {} matched multiple entries in the "
                    "capture file, using first entry".format(url)
                )
        else:
            raise NotImplementedError(
                "Matching against parameters and non-exact urls not yet implemented"
            )
        pass

    def inject_get_request(self, func):
        """ Method override for requests.get to reply from capture instead of
        shooting real http requests.
        """
        # Keep a copy of the original method
        original_requests_get = copy.copy(requests.get)

        def wrapper(*args,  **kwargs):
            requests.get = self.mock_get
            func()
            # Restore original method
            requsts.get = original_requests_get
        return wrapper
