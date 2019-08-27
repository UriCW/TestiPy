from Testi import Requesti


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


def test_populate_response():
    requesti = Requesti("./Testi/tests/data/parliament_uk_session.har")
    url_regex = "^https\:\/\/search-material\.parliament\.uk/search$"
    matched = requesti.find_packets(url_regex)
    assert len(matched) == 1
    resp_dict = matched[0]['response']
    resp_obj = requesti.populate_response(resp_dict)
    assert resp_obj.status_code == 200
    print(resp_obj.headers)
    assert 'set-cookie' in resp_obj.headers
    assert resp_obj.headers['set-cookie'] ==\
        'ARRAffinity=05893460edd64dea18419719afaa21f452a43'\
        '339bdce881ba0f8ccabe7ab2e9c;Path=/;HttpOnly;Domain'\
        '=search-material.azurewebsites.net'
    print(resp_obj)
    assert '<!doctype html><html itemscope=""' in resp_obj.text
    assert False


def test_get_override():
    pass


def test_get_release():
    pass


def test_response_contents():
    pass
