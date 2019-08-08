# RAG DB

A graph theory project for a graph database.

## Abstract

Finding indirect relationships is not an easy or typical usage for traditional databases. A graph database is designed in such a way that makes finding indirect associations for applications such as a social network or reccomendation engine much more efficient and easy. Below is a great photo from Nicolle Cysneiros Blog Post about Graph Databases on Medium to display the typical structure which I will be modeling:

![alt text](https://miro.medium.com/max/700/1*3BvGbuFSHeLUihVXAAaNdw.png "Social Network scenario represented as a graph")

Here are the problems I wish to solve with this project:

1. Quickly find specific types of associations in a set of data.
2. Find the level of association for indirect associations in order to make determinations or reccomendations.
3. Categorize differing data by common associations.

## Future Todo

- Add visualize method to database that will render figure of a specific collection.
- Add a cli file that will serve as a command line interface/service for running the database and interacting with it.
- Add a file persistent layer that will backup the in-memory structures as binary to disk on a consistent interval and before shutdown.
- Add REST API

## Resources

- https://en.wikipedia.org/wiki/Graph_database#/media/File:GraphDatabase_PropertyGraph.png
- https://medium.com/labcodes/graph-databases-talking-about-your-data-relationships-with-python-b438c689dc89
