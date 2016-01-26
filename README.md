## Deep Time Data Infrastructure - Mineral Observation Map

Project Page: http://tw.rpi.edu/web/project/DTDI

Use Cases: http://tw.rpi.edu/web/project/DTDI/WorkingGroups/usecases

github: https://github.com/tetherless-world/dtdi-mineral-observation-map

### Overview

The DTDI faceted mineral observation map is powered by [FacetView2](https://github.com/tetherless-world/facetview2) - a pure javascript frontend for ElasticSearch search indices that let you easily embed a faceted browse front end into any web page.

To configure a working faceted browser you need:
1. A running instance of ElasticSearch with a populated index
2. A webpage with references to facetview2 scripts and an embedded configuration

That's it!

You can find out more about ElasticSearch at [https://www.elastic.co/products/elasticsearch](https://www.elastic.co/products/elasticsearch)

### ElasticSearch Installation

Instructions for setting up a local instance of ElasticSearch are available at [https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)

Additionally, if you are on OSX you can install elasticsearch using homebrew with this command:

```
brew install elasticsearch
```

Finally, you can use the official docker image to start a containerized instance of ElasticSearch.  Instructions are available at [https://hub.docker.com/_/elasticsearch/](https://hub.docker.com/_/elasticsearch/).

### Installation using docker compose

The project includes a [docker compose](https://www.docker.com/products/docker-compose) script (docker-compose.yml) which can be used to deploy the faceted search browser using docker.  

This script defines a container for the following services:
1) an elasticsearch instance (available to the docker host system on port 49200)
2) a nginx instance which is used to host the HTML and JS files of the map webpage (available to the docker host system on port 49157)

#### HTML/JS deploy via docker compose and nginx

The nginx docker container hosts all files in html/ as http://localhost:49157/map

The HTML and JS files for the deployed service can be updated by editing the contents of the html/ directory.  A restart of the docker container should not be necessary.

#### Elasticsearch deploy via docker compose

An instance of elasticsearch 1.6 is deployed as a docker container and accessible to the host system at port 49200.

The elaseticsearch REST API for this instance should be available from the docker system host at localhost:49200/.

For the faceted browser to work the elasticsearch service will need to be accessible by any web client that is running the facetview2 JS.  Therefore it is recommended to make the elasticsearch API publicly available via a proxy; this proxy will have to be embedded in the facetview2 configuration in the map browser JS config.