from swagger_server.test import BaseTestCase
from flask import json


def assert_keys_in(keys_, dict_):
    """Asserts dict_ has keys."""
    k1, k2 = set(keys_), set(dict_)
    assert k1 < k2, "Missing keys: %r" % (k1 - k2)


def assert_dict_in(sub_, dict_):
    """Asserts sub_ is contained in dict_."""
    delta = {k: dict_[k]
             for k, v in sub_.items()
             if dict_[k] != v}

    assert not delta, "Missing items: %r" % delta


class TestHarness(BaseTestCase):

    def request(self, uri, method='GET', expected_status=200, **kwargs):
        response = self.client.open(uri, method=method, **kwargs)
        self.assertStatus(response, expected_status,
                          'Response body is : ' + response.data.decode('utf-8'))
        return response, json.loads(response.data.decode('utf-8'))
