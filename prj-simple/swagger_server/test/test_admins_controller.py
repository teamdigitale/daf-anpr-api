# coding: utf-8

from flask import json

from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.table import Table  # noqa: E501
from swagger_server.models.table_data import TableData  # noqa: E501
from swagger_server.test.harness import TestHarness, assert_dict_in
from swagger_server.tools import es

MOCK_BODY = {
    "index": "codistat",
    "description": "Data description",
    "items": [
        {"a": 1, "codistat": 1},
        {"a": 1, "codistat": 2},
        {"a": 1, "codistat": 3},
    ]
}


class TestAdminsController(TestHarness):
    """AdminsController integration test stubs"""

    def test_upload_dictionary(self):
        """Test case for upload_dictionary

        Upload a new (version of a) dictionary eventually creating a new dictionary.
        The passed csv file contains a trailing line with the expected line count.
        If the schema does not match previous version, an error is returned.
        """
        response, data = self.request(  # noqa:
            '/robipolli/core-vocabularies/0.0.1/dictionaries/test',
            method='POST',
            data=json.dumps(MOCK_BODY),
            content_type='application/json',
            expected_status=201)

        assert_dict_in({'name': 'test'}, data)

    def test_upload_dictionary_with_meta(self):
        """Test case for upload_dictionary

        Upload a new (version of a) dictionary eventually creating a new dictionary.
        The passed csv file contains a trailing line with the expected line count.
        If the schema does not match previous version, an error is returned.
        """
        response, data = self.request(  # noqa:
            '/robipolli/core-vocabularies/0.0.1/dictionaries/test1',
            method='POST',
            data=json.dumps(MOCK_BODY),
            content_type='application/json',
            expected_status=201)

        assert data['description'] != 'TODO'
        assert_dict_in({'index': 'codistat'}, data)

    def test_upload_dictionary_noindex(self):
        """Test case for upload_dictionary

        Upload a new (version of a) dictionary eventually creating a new dictionary.
        The passed csv file contains a trailing line with the expected line count.
        If the schema does not match previous version, an error is returned.
        """
        body = MOCK_BODY.copy()
        del body['index']
        response, data = self.request(  # noqa:
            '/robipolli/core-vocabularies/0.0.1/dictionaries/test',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            expected_status=400)

        assert_dict_in({'detail': "'index' is a required property"}, data)

    def test_upload_dictionary_badindex(self):
        """Test case for upload_dictionary

        Upload a new (version of a) dictionary eventually creating a new dictionary.
        The passed csv file contains a trailing line with the expected line count.
        If the schema does not match previous version, an error is returned.
        """
        body = {
            'index': 'two',
            'description': 'test descs.',
            'items': [
                {'a': 1, 'one': 1},
                {'a': 1, 'two': 1},
                {'a': 1, 'three': 1},
            ]
        }
        response, data = self.request(  # noqa:
            '/robipolli/core-vocabularies/0.0.1/dictionaries/test',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            expected_status=500)

    def tearDown(self):
        es.indices.delete('test', ignore=[400, 404])


if __name__ == '__main__':
    import unittest
    unittest.main()
