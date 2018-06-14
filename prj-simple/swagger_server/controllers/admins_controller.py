import connexion
import six

from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.table import Table  # noqa: E501
from swagger_server.models.table_data import TableData  # noqa: E501
from swagger_server import util, tools
from swagger_server.controllers.public_controller import get_dictionary

from elasticsearch import Elasticsearch, helpers
import json
from datetime import datetime


def upload_dictionary(dictionary_name, body):  # noqa: E501
    """Upload a new (version of a) dictionary eventually creating a new dictionary. The passed csv file contains a trailing line with the expected line count. If the schema does not match previous version, an error is returned. 

     # noqa: E501

    :param dictionary_name: The name of the dictionary
    :type dictionary_name: str
    :param body: Use MarkDown here!
    :type body: dict | bytes

    :rtype: Table
    """
    if not connexion.request.is_json:
        return problem(status=415, title="Unsupported Media Type",
                       detail="Bad Content-Type: did you use application/json?")
    body = connexion.request.get_json()  # noqa: E501
    print("body: ", body)
    
    es = Elasticsearch(hosts='elastic')

    #if version == 'latest':
    #    raise ValueError("""Version should not be "latest".""")
    
    versions = tools.get_index_doctypes(es, dictionary_name)
    new_version = datetime.now().isoformat()[:19]
    if versions and (versions[-1] > new_version):
        raise NotImplementedError(f"Version too low: {versions} vs {new_version}")
    
    loader = DataLoader('elastic', dictionary_name, new_version, 'codistat')
    inserted, errors = loader.index_data(body)
    return get_dictionary(dictionary_name)


class DataLoader:

    """exposes the methods to index and update data from the cities"""

    def __init__(self, hosts, index_name='anpr', doc_type='comuni', id_col_name='CODISTAT'):
        self._hosts = hosts
        self._index_name = index_name
        self._doc_type = doc_type
        self._id_col_name = id_col_name
        self._es = Elasticsearch(hosts=hosts)

    def index_data(self, json_data):
        """ this method is called to index the information about the city
          json_data: a list or generator of data
        """
        self._create_index()
        actions = (
            self._make_action(d[self._id_col_name], d) for d in json_data
        )
        result = helpers.bulk(self._es, actions)
        return result

    def update_data(self, json_data):
        """ this method is called to update the information about the city
          json_data: a list or generator of data
        """
        actions = (
            self._make_action(d[self._id_col_name], d, op='update') for d in json_data
        )
        result = helpers.bulk(self._es, actions)
        return result

    def delete_index(self):
        if self._es.indices.exists(self._index_name):
            self._es.indices.delete(self._index_name)

    def _create_index(self):
        if not self._es.indices.exists(self._index_name):
            self._es.indices.create(self._index_name)

    def _make_action(self, id_doc, doc, op='index'):
        """define the action to index or update the documents"""
        return {
            '_op_type': op,
            '_index': self._index_name,
            '_type': self._doc_type,
            '_id': id_doc,
            'doc': doc
        }

