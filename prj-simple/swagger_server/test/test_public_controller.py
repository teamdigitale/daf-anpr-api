# coding: utf-8

from swagger_server.test.harness import assert_dict_in, assert_keys_in, TestHarness


class TestPublicController(TestHarness):

    """PublicController integration test stubs"""

    def test_get_dictionaries(self):
        response, data = self.request(  # noqa:
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

    def _test_get_dictionary_versions_latest(self):
        response, data = self.request(
            f'/robipolli/core-vocabularies/0.0.1/dictionaries/comuni/latest?limit=5&offset=5'
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
