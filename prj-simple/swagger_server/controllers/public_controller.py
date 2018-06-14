import connexion
import six

from swagger_server.models.dictionaries import Dictionaries  # noqa: E501
from swagger_server.models.dictionary import Dictionary  # noqa: E501
from swagger_server.models.entries import Entries  # noqa: E501
from swagger_server.models.entry import Entry  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.tables import Tables  # noqa: E501
from swagger_server import util, tools

from connexion import problem
from elasticsearch import Elasticsearch, exceptions as es_exc

filter_indexes = lambda data: [
    x for x in data if x['index'] not in ('.kibana',)]


def entry_from_doc(doc):
    return Entry(key=doc['_id'], data=doc['_source']['doc'])


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
    ret = c.cat.indices(format='json')[offset:offset + limit]
    ret = filter_indexes(ret)
    items = []
    for i in ret:
        versions = tools.get_index_doctypes(c, i['index'])
        items.append(Dictionary(name=i['index'],
                                description="TODO",
                                versions=versions,
                                last_version=versions[-1] if versions else None,
                                meta=i))

    return Dictionaries(
        items=items,
        offset=offset,
        offset_next=limit + offset,
    )


def get_dictionary(dictionary_name):  # noqa: E501
    """Get informations about a dictionary.

    Retrieve available dictionary version and URI.  # noqa: E501

    :param dictionary_name: The name of the dictionary
    :type dictionary_name: str

    :rtype: Dictionary
    """
    c = Elasticsearch(hosts='elastic')
    ret = c.cat.indices(index=dictionary_name, format='json')[0]
    versions = tools.get_index_doctypes(c, dictionary_name)

    return Dictionary(name=dictionary_name,
                      description="TODO",
                      versions=versions,
                      last_version=versions[-1] if versions else None,
                      meta=ret)


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
    if version == 'latest':
        version = tools.get_index_doctypes(es, dictionary_name)
    if not version:
        return problem(status=404, title=f"No version",
                      detail=f"No versions for {dictionary_name}")
    
    res = c.search(index=dictionary_name, doc_type=[version],
                   size=limit, from_=offset,
                   body={"query": {"match_all": {}}})
    print(res)
    items = [entry_from_doc(hit) for hit in res['hits']['hits']]
    return Entries(
        items=items,
        count=res['hits']['total'],
        offset=offset,
        offset_next=offset + limit,
    )


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
    except es_exc.NotFoundError as e:  # TODO map Elastic error in API
        if e.error == 'index_not_found_exception':
            title = "dictionary not found"
        else:
            title = e.error
        return problem(status=404, title=title,
                       detail=f"Entry id: {entry_key} not found in {dictionary_name}/{version}")

    return entry_from_doc(entry)
