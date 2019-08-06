# RAG DB

A graph theory project for a graph database that is exposed as a REST API.

## Abstract

The database will be modeled in the following way: A hash table of collections will exist in memory and be loaded from a file at startup. The database will be saved to file as a binary representation on update and safe shutdown. Each collection will be a directed graph data structure with a members property. The members property is a hash table with a list of connected members. Each member added to a collection will have a labels property which is a hash table of labels. Each label is a hash table of pointers to other members representing associations. To further visualize, look at this great photo from Nicolle Cysneiros Blog Post about Graph Databases on Medium:

![alt text](https://miro.medium.com/max/700/1*3BvGbuFSHeLUihVXAAaNdw.png "Social Network scenario represented as a graph")

As a v1 of this idea, the basic functionality will be tested via a cli test program and not be exposed for general usage.

Finding all associations and commonalities will use a modified version of Dijkstra's. Finding associations will require finding all the neighbors with the same weight(label). Finding commonalities/differences will require finding all the neighbors with two different weights(labels) and finding the intersection or difference between these two sets of data. To display all of the associations for a single collection, we can use Prim's to generate a minimum spanning tree of the data.

## Resources

- https://en.wikipedia.org/wiki/Graph_database#/media/File:GraphDatabase_PropertyGraph.png
- https://medium.com/labcodes/graph-databases-talking-about-your-data-relationships-with-python-b438c689dc89
