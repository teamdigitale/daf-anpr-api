# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.problem import Problem  # noqa: E501
from swagger_server.models.timestampa import Timestampa  # noqa: E501
from swagger_server.test import BaseTestCase


def assert_keys_in(keys_, dict_):
    k1, k2 = set(keys_), set(dict_)
    assert k1 < k2, "Missing keys: %r" % (k1 - k2)


def assert_dict_in(sub_, dict_):
    delta = {k: dict_[k]
             for k, v in sub_.items()
             if dict_[k] != v}

    assert not delta, "Missing items: %r" % delta


class TestPublicController(BaseTestCase):

    """PublicController integration test stubs"""

    def request(self, uri, method='GET', **kwargs):
        response = self.client.open(uri, method=method, **kwargs)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        return response, json.loads(response.data.decode('utf-8'))

    def test_get_dictionaries(self):
        response, data = self.request(
            '/robipolli/core-vocabularies/0.0.1/dictionaries')
        assert_keys_in(('items', 'offset'), data)

        first, *_ = data['items']
        assert_keys_in(('name', 'versions', 'last_version'), first)

    def test_get_dictionary(self):
        response, data = self.request(
            '/robipolli/core-vocabularies/0.0.1/dictionaries/comuni')
        assert_keys_in(('name', 'versions', 'last_version'), data)

    def test_get_dictionary_versions(self):
        response, data = self.request(
            '/robipolli/core-vocabularies/0.0.1/dictionaries/comuni')
        v = data['last_version']
        response, data = self.request(f'/robipolli/core-vocabularies/0.0.1/dictionaries/comuni/{v}')
        assert 'items' in data
        assert len(data['items']) < 100

    def test_get_dictionary_versions_limit_offset(self):
        response, data = self.request(
            '/robipolli/core-vocabularies/0.0.1/dictionaries/comuni')
        v = data['last_version']
        response, data = self.request(
            f'/robipolli/core-vocabularies/0.0.1/dictionaries/comuni/{v}?limit=5&offset=5'
        )
        assert 'items' in data
        assert len(data['items']) == 5
        assert_dict_in({'offset': 5, 'offset_next': 10}, data)

    def test_get_dictionary_data(self):
        response, data = self.request(
            '/robipolli/core-vocabularies/0.0.1/dictionaries/comuni')
        v = data['last_version']
        response, data = self.request(
            f'/robipolli/core-vocabularies/0.0.1/dictionaries/comuni/{v}/87005'
        )
        assert_dict_in({'key': '87005'}, data)
        assert 'data' in data, f"Missing 'data' {data}"


if __name__ == '__main__':
    import unittest
    unittest.main()
