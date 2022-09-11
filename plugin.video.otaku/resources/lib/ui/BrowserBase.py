from six.moves import urllib_parse
from resources.lib.ui import http


class BrowserBase(object):
    _BASE_URL = None

    def _to_url(self, url=''):
        assert self._BASE_URL is not None, "Must be set on inherentance"

        if url.startswith("/"):
            url = url[1:]
        return f"{self._BASE_URL}/{url}"

    def _send_request(self, url, data=None, set_request=None):
        return http.send_request(url, data, set_request).text

    def _post_request(self, url, data={}, set_request=None):
        return self._send_request(url, data, set_request)

    def _get_request(self, url, data=None, set_request=None):
        if data:
            url = f"{url}?{urllib_parse.urlencode(data)}"
        return self._send_request(url, None, set_request)
