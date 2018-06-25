from flask_elasticsearch import FlaskElasticsearch
import elasticsearch
es = FlaskElasticsearch()


def get_index_doctypes(index, doc_type=None):
    """Returns all doctypes in an index."""
    try:
        mappings = es.indices.get_mapping(index=index)
        return sorted(list(mappings[index]['mappings'].keys()))
    except (KeyError, AttributeError, elasticsearch.exceptions.NotFoundError):
        return []


def get_meta(index, doc_type=None):
    """Returns all doctypes in an index."""
    try:
        mappings = es.indices.get_mapping(index=index, doc_type=doc_type)
        return mappings[index]['mappings'][doc_type]['_meta']
    except (KeyError, elasticsearch.exceptions.NotFoundError):
        return {}
