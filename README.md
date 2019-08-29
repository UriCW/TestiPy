# TestiPy - Mocking utils for pytest.
Mock HTTP Responses by replying Responses from a capture file.
Currently only supports .har files, and patching requests.get

To generate a .har file in Firefox, open the network console (Ctrl + Shift + E) and start browsing.
When done, right click on ths capture window and "Save All As HAR".

# requests
Requests mocked by replying packet captures in .har file format.
I plan to implement .pcap files in the future if i find those necessary, 
and possibly also scripts to craft responses. 

Databases are not yet mocked at all.

## Examples

inject mocked requests onto requests.get 
```python
from Testi import Requesti, patch_requests

URL = "https://search-material.parliament.uk/search"

@patch_requests("./Testi/tests/data/parliament_uk_session.har")
def test_something():
    mocked_response = requests.get(URL)
```

To find all captured packets to url
```python
requesti = Requesti(HAR_FILE)
url_regex = "^http.*.parliament\.uk"
matched = requesti.find_packets(url_regex)
```
