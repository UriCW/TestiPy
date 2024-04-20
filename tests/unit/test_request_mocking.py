from testirequesti import Requesti, patch_requests # pyright: ignore [ reportMissingImports ]
import requests


def test_instance_create():
    """ Confirms that we have loaded the expected capture file and that it
    at least contains a list of request/response entries with a url for every request
    """
    requesti = Requesti("./tests/data/session.har")
    assert len(requesti.capture) == 2 # Two entries in har capture
    for e in requesti.capture:
        assert "request" in e
        assert(type(e["request"]) == dict)
        assert "url" in e['request']

        assert "response" in e
        assert(type(e["response"]) == dict)


def test_find_packets():
    requesti = Requesti("./tests/data/session.har")
    url_regex = '^https://.*..com/robots.txt$'
    matched = requesti.find_packets(url_regex)
    assert len(matched) == 1


@patch_requests("./tests/data/session.har")
def test_patch():
    resp = requests.get("https://www.capterra.com/robots.txt")
    assert "# See http://www.robotstxt.org/wc/norobots.html"  in resp.text
    assert "Sitemap: https://www.capterra.com/sitemap.xml"
    assert "\nDisallow: /\nUser-agent: NTENTbot\n" in resp.text
    assert resp.status_code == 200
