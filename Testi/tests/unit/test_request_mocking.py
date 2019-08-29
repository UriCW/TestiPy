from Testi import Requesti, patch_requests
import copy
import requests


def test_instance_create():
    """ Confirms that we have loaded the expected capture file and that it
    at least contains a list of request/response entries with a url for every request
    """
    requesti = Requesti("./Testi/tests/data/parliament_uk_session.har")
    assert len(requesti.capture) == 328
    for e in requesti.capture:
        assert "request" in e
        assert(type(e["request"]) == dict)
        assert "url" in e['request']

        assert "response" in e
        assert(type(e["response"]) == dict)


def test_find_packets():
    requesti = Requesti("./Testi/tests/data/parliament_uk_session.har")
    url_regex = "^http.*.parliament\.uk"
    matched = requesti.find_packets(url_regex)
    assert len(matched) == 290


# @patch_requests("./Testi/tests/data/parliament_uk_session.har")
@patch_requests("./Testi/tests/data/parliament_uk_session.har")
def test_patch():
    resp = requests.get("https://search-material.parliament.uk/search")
    # print(resp.headers)
    assert "<!DOCTYPE html>\r\n<!--[if IE 7]> " in resp.text
    assert "To retrieve earlier debates, please" in resp.text
    assert resp.status_code == 200
    # assert resp.headers[""]
    # assert False
