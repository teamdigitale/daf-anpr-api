#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.tools import es


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'DAF ANPR API.'})
    app.app.config["ELASTICSEARCH_HOST"] = "elastic:9200"
    es.init_app(app.app)
    app.run(port=8443, ssl_context='adhoc')


if __name__ == '__main__':
    main()
