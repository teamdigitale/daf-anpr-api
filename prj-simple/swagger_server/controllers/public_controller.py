import connexion
import six

from swagger_server.models.dictionaries import Dictionaries  # noqa: E501
from swagger_server.models.dictionary import Dictionary  # noqa: E501
from swagger_server.models.entries import Entries  # noqa: E501
from swagger_server.models.entry import Entry  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.tables import Tables  # noqa: E501
from swagger_server import util

from connexion import problem
from elasticsearch import Elasticsearch, exceptions as es_exc

filter_indexes = lambda data: [x for x in data if x['index'] not in ('.kibana',)]

def get_index_doctypes(cli, index):
    mappings = cli.indices.get_mapping(index=index)
    return list(mappings[index]['mappings'].keys())


def get_dictionaries(name=None, limit=10, offset=0, sort=None):  # noqa: E501
    """Get informations about provided dictionaries.

    Shows a list of supported dictionaries.  # noqa: E501

    :param name: The indexed key to search with.
    :type name: str
    :param limit: How many items to return at one time (max 100)
    :type limit: int
    :param offset: The zero-ary offset index into the results
    :type offset: int
    :param sort: Sorting order
    :type sort: str

    :rtype: Dictionaries
    """
    c = Elasticsearch(hosts='elastic')
    ret = c.cat.indices(format='json')[offset:offset+limit]
    ret = filter_indexes(ret)
    for i in ret:
        i['versions'] = get_index_doctypes(c, i['index'])
    return ret


def get_dictionary(dictionary_name):  # noqa: E501
    """Get informations about a dictionary.

    Retrieve available dictionary version and URI.  # noqa: E501

    :param dictionary_name: The name of the dictionary
    :type dictionary_name: str

    :rtype: Dictionary
    """
    c = Elasticsearch(hosts='elastic')
    ret = c.cat.indices(index=dictionary_name, format='json')[0]
    ret['versions'] = get_index_doctypes(c, dictionary_name)
    return ret


def get_dictionary_version(dictionary_name, version, name=None, limit=10, offset=0, sort=None):  # noqa: E501
    """Get entries from a dictionary.

    Retrieve paged entries from a Table.  # noqa: E501

    :param dictionary_name: The name of the dictionary
    :type dictionary_name: str
    :param version: A specific version of a dictionary.
    :type version: int
    :param name: The indexed key to search with.
    :type name: str
    :param limit: How many items to return at one time (max 100)
    :type limit: int
    :param offset: The zero-ary offset index into the results
    :type offset: int
    :param sort: Sorting order
    :type sort: str

    :rtype: Entry
    """
    c = Elasticsearch(hosts='elastic')
    res = c.search(index=dictionary_name, doc_type=[version],
                   size=limit, from_=offset,
                   body={"query": {"match_all": {}}})
    print(res)
    items = [ hit["_source"]["doc"] for hit in res['hits']['hits']]
    return {
        "items": items,
        "count": res['hits']['total'],
        "offset_next": offset+limit
        }


def get_dictionary_meta(dictionary_name):  # noqa: E501
    """Get meta informations about a dictionary.

    Retrieve available dictionary version and URI: foo bar  # noqa: E501

    :param dictionary_name: The name of the dictionary
    :type dictionary_name: str

    :rtype: Dictionary
    """
    raise NotImplementedError(dictionary_name)
    c = Elasticsearch(hosts='elastic')
    entry = c.get(index=dictionary_name, id=entry_key, doc_type=version)

    return 'do some magic!'


def get_entry(dictionary_name, version, entry_key):  # noqa: E501
    """Get a Table entry

    Retrieve an entry from a Table. # noqa: E501

    :param dictionary_name: The name of the dictionary
    :type dictionary_name: str
    :param version: A specific version of a dictionary.
    :type version: int
    :param entry_key: The entry key
    :type entry_key: str

    :rtype: Entries
    """
    c = Elasticsearch(hosts='elastic')
    try:
        entry = c.get(index=dictionary_name, id=entry_key, doc_type=version)
    except es_exc.NotFoundError:
        return problem(status=404, title=f"Entry not found",
                       detail=f"Entry id: {entry_key} not found in {dictionary_name}/{version}") 
    
    return entry['_source']['doc']


def get_entry_by_table(table_uuid, entry_key):  # noqa: E501
    """Get a Table entry

    Retrieve an entry from a Table. # noqa: E501

    :param table_uuid: The table uuid
    :type table_uuid: str
    :param entry_key: The entry key
    :type entry_key: str

    :rtype: Entries
    """
    return 'do some magic!'


def get_table_entries(table_uuid, name=None, limit=None, offset=None, sort=None):  # noqa: E501
    """Get entries from a given table.

    Retrieve paged entries from a Table.  # noqa: E501

    :param table_uuid: The table uuid
    :type table_uuid: str
    :param name: The indexed key to search with.
    :type name: str
    :param limit: How many items to return at one time (max 100)
    :type limit: int
    :param offset: The zero-ary offset index into the results
    :type offset: int
    :param sort: Sorting order
    :type sort: str

    :rtype: Entries
    """
    return 'do some magic!'


def get_tables(dictionary_name=None, limit=None, offset=None, sort=None):  # noqa: E501
    """Get informations about exiting tables.

    Shows a list of supported tables matching the given name.  # noqa: E501

    :param dictionary_name: The name of the dictionary
    :type dictionary_name: str
    :param limit: How many items to return at one time (max 100)
    :type limit: int
    :param offset: The zero-ary offset index into the results
    :type offset: int
    :param sort: Sorting order
    :type sort: str

    :rtype: Tables
    """
    return 'do some magic!'
