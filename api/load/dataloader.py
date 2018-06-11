from elasticsearch import Elasticsearch, helpers
import argparse
import json

class DataLoader:
    """exposes the methods to index and update data from the cities"""

    def __init__(self, hosts, index_name='anpr-index', doc_type='comuni', id_col_name='CODISTAT'):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load data into Elasticsearch")
    parser.add_argument('--hosts', type=str, nargs='+', help='elastic hosts', required=True)
    parser.add_argument('--index_name', default='anpr-index', help='the name of the index, default anpr-index')
    parser.add_argument('--doc_type', default='comuni', help='the name of the doc type')
    parser.add_argument('--id_col', default='CODISTAT', help='the id column')
    parser.add_argument('--action', default='index', help='action to perform can be update or index')
    parser.add_argument('--source_path', help='the path of the json file with the data to index', required=True)
    args = parser.parse_args()

    with open(args.source_path, 'r') as f:
        data = json.load(f)

    loader = DataLoader(args.hosts, args.index_name, args.doc_type, args.id_col)
    inserted, errors = loader.index_data(data)
    print('loaded {} records'.format(inserted))


