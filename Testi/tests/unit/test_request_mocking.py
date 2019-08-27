from Testi import Requesti
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


def test_get_override():
    requesti = Requesti("./Testi/tests/data/parliament_uk_session.har")

    get_method = copy.copy(requests.get)

    @requesti.inject_get_request
    def test_inner():
        assert requests.get is not get_method
    test_inner()
    assert requests.get is get_method


def test_get():
    requesti = Requesti("./Testi/tests/data/parliament_uk_session.har")

    @requesti.inject_get_request
    def fetch():
        txt = requests.get("https://search-material.parliament.uk/search")
        print(txt)
        assert False

    fetch()
