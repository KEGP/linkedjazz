from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import pickle
import urllib.request
import re

sparql = SPARQLWrapper("http://fuseki:3030/db/query")
sparql.setReturnFormat(JSON)

def query(sparql_query):
  sparql.setQuery(sparql_query)
  ret = sparql.queryAndConvert()["results"]["bindings"]
  return [{ k: v["value"] for k, v in b.items()} for b in ret]

try:
  with open("res.pickle", "rb") as f:
    studio_friendships = pickle.load(f)
except:
  # cache artists with some relationships
  studio_friendships = query("""
  PREFIX kejazz: <http://localhost:8080/ontology/kejazz/> 
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX relationship: <http://purl.org/vocab/relationship/>
  PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
  SELECT DISTINCT ?recordingIRI ?recordingName ?from ?to ?artistIRI ?artistName ?artistInstrument ?otherIRI ?otherName ?otherInstrument WHERE {
    ?recordingIRI kejazz:hasTitle ?recordingName .
    ?recordingPerformance kejazz:forRecording ?recordingIRI ;
                          kejazz:includesArtist ?artistIRI ;
                          kejazz:withInstrument [ kejazz:hasName ?artistInstrument ] ;
              kejazz:atTime [ 
                  kejazz:hasIntervalStartDate ?from ;
                  kejazz:hasIntervalEndDate ?to
                ] .
    
    ?artistIRI kejazz:hasName ?artistName ;
              owl:sameAs ?sameAs .

    ?otherIRI kejazz:hasName ?otherName ;
              owl:sameAs ?sameAsOther .
    ?otherRecordingPerformance kejazz:forRecording ?recordingIRI ;
                              kejazz:includesArtist ?otherIRI ;
                              kejazz:withInstrument [ kejazz:hasName ?otherInstrument ] .

    ?sameAs (relationship:friendOf|^relationship:friendOf) ?sameAsOther . }
  """)
  with open("res.pickle", "wb") as f:
    studio_friendships = pickle.dump(studio_friendships, f)


def get_artist_image(artist):
  return query("""
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX dbo: <http://dbpedia.org/ontology/>
  SELECT ?image WHERE {
    BIND(<%s> AS ?artist) .
    ?artist owl:sameAs ?dbpedia .
    SERVICE <https://dbpedia.org/sparql/> { 
      ?dbpedia dbo:thumbnail ?imageCropped . 
      BIND(REPLACE(STR(?imageCropped), "width=300", "") AS ?image) .
    } 
    FILTER(CONTAINS(STR(?dbpedia), "dbpedia")) . 
  }
  """ % artist)[0]["image"]

def get_youtube_video(query):
  title = query.replace(" ", "%20")
  html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={title}")
  video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]
  return video_id

app = FastAPI()
templates = Jinja2Templates(directory="templates")
print("READY")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
  ctx = {
    "request": request,
  }

  friendship = random.choice(studio_friendships)  
  ctx.update(**friendship)

  ctx["artistImage"] = get_artist_image(friendship["artistIRI"])
  ctx["otherImage"] = get_artist_image(friendship["otherIRI"])
  
  youtube_query = f"{ctx['artistName']} {ctx['otherName']} {ctx['recordingName']}"
  ctx["youtubeIRI"] = get_youtube_video(youtube_query)

  return templates.TemplateResponse("index.html", ctx)
