# Linked Jazz project

## How to run it

  1. First of all, download or clone this repository (this requires `git` to be installed on your machine):

     ```bash
     git clone https://github.com/KEGP/linkedjazz.git
     cd $(pwd)/linkedjazz/
     ```

  2. launch the Docker containers (this requires `Docker` to be installed on your machine):

     ```bash
     docker-compose up
     ```

  3. open your favorite web browser and explore the following endpoints:

     | Endpoint | Description | Link |
     | ------------- | ------------- | --- |
     | [LODE](https://github.com/essepuntato/LODE) | _human readable version of our ontology_ | <http://localhost:8080/ontology> |
     | [WebVOWL](https://github.com/VisualDataWeb/WebVOWL) | _graphical visualisation of our ontology_ | <http://localhost:8080/webvowl/> |
     | [LodView](https://github.com/LodLive/LodView) | _human readable representation of the entities in our dataset_ | `http://localhost:8080/lodview/kejazz/<CLASSNAME>/<ID>` (ex. <http://localhost:8080/resource/kejazz/Artist/663f8232-8c46-4851-803f-a91d31593b14>) |
     | [SPARQL.Anything](https://github.com/SPARQL-Anything/sparql.anything) | _human readable representation of the entities in our dataset_ | <http://localhost:8080/sparqlanything/sparql> (remember to replace `/sparql.anything` with `sparql.anything` in the text field placed at the top of the page) |

  4. the ontology source files in `RDF/XML` format are available, respectively, at <http://localhost:8080/ontology/kejazz> and at <http://localhost:8080/ontology/chord-annotations>.
