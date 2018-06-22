# ANPR datasets per i comuni [MVP]

*NOTE*: This app is work-in-progress. The implementation is
        a quick and dirty hack around connexion and elasticsearch.

Install the required libraries with

```
pip install -e requirements.txt
```
 > please use conda of python virtual env!!!

This project provides the notebooks and code to:
1. preprocess anpr dataset
2. integrate it with istat data
3. load the processed dataset into elastichsearch (test, and prod env)


## API


### Prepare the environment

The infrastructure is based on:

  - elasticsearch
  - kibana browser
  - an one-shot python container for dataloader
  - a running python-flask containter with the app.

To create the infrastructure containers and import data:

         make setup

To generate code and run the application:

	make app-run	

### Load data into Elasticsearch

To load the data run the following script

```
python ./api/load/dataloader.py --help
usage: dataloader.py [-h] --hosts HOSTS [HOSTS ...] [--index_name INDEX_NAME]
                     [--doc_type DOC_TYPE] [--id_col ID_COL] [--action ACTION]
                     --source_path SOURCE_PATH

Load data into Elasticsearch

optional arguments:
  -h, --help            show this help message and exit
  --hosts HOSTS [HOSTS ...]
                        elastic hosts
  --index_name INDEX_NAME
                        the name of the index, default anpr-index
  --doc_type DOC_TYPE   the name of the doc type
  --id_col ID_COL       the id column
  --action ACTION       action to perform can be update or index
  --source_path SOURCE_PATH
                        the path of the json file with the data to index

```

where `hosts` and `source_path` are mandatory.

### Local Development

In order to develop the service you can run an elasticsearch and kibana instance via [docker-compose].

```
$ docker-compose up -d
$ docker-compose ps

        Name                      Command               State                Ports              
------------------------------------------------------------------------------------------------
dafanprapi_elastic_1   /docker-entrypoint.sh elas ...   Up      0.0.0.0:9200->9200/tcp, 9300/tcp
dafanprapi_kibana_1    /docker-entrypoint.sh kibana     Up      0.0.0.0:5601->5601/tcp   
```

load data

```
python ./api/load/dataloader.py --hosts 127.0.0.1 --source_path ./data/full.json
```

#### Kibana

To check if the values are loaded you can user [sense](http://localhost:5601/app/kibana#/dev_tools/console?_g=()) and run a `match_all` query.

```
GET _search
{
  "query": {
    "match_all": {}
  }
}
```

### Production Setup


Elastic Host: 192.168.0.43 (available only via vpn). At [this link](http://192.168.0.43:5601/app/kibana#/dev_tools/console?_g=()) is available kibana with the [sense plugin](https://www.elastic.co/guide/en/sense/current/sense-ui.html).

#### To index the documents

```
python ./api/load/dataloader.py --hosts 192.168.0.43 --source_path ./data/full.json
```

#### To update the documents

```
python ./api/load/dataloader.py --hosts 192.168.0.43 --source_path ./data/full.json --action update
```
