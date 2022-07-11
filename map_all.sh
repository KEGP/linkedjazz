#!/bin/bash

SPARQL_OPT="--sparqlanything ./sparql-anything-0.7.0.jar"
TEMPLATE_OPT="--template-name name"

python mapping/mapfiles.py ./mapping/work.sparql ./data/musicbrainz/work/ ./resources/ $TEMPLATE_OPT $SPARQL_OPT --outprefix work
python mapping/mapfiles.py ./mapping/release.sparql ./data/musicbrainz/release/ ./resources/ $TEMPLATE_OPT $SPARQL_OPT --outprefix release
python mapping/mapfiles.py ./mapping/recording.sparql ./data/musicbrainz/recording/ ./resources/ $TEMPLATE_OPT $SPARQL_OPT --outprefix recording
python mapping/mapfiles.py ./mapping/chord-annotations.sparql ./data/jaah/chord_annotations/ ./resources/ $TEMPLATE_OPT $SPARQL_OPT --outprefix chord
python mapping/mapfiles.py ./mapping/artist.sparql ./data/musicbrainz/artist/ ./resources/ $TEMPLATE_OPT $SPARQL_OPT --outprefix artist
python mapping/mapfiles.py ./mapping/artist-work.sparql ./data/musicbrainz/work/ ./resources/ $TEMPLATE_OPT $SPARQL_OPT --outprefix artist_work
python mapping/mapfiles.py ./mapping/artist-recording.sparql ./data/musicbrainz/recording/ ./resources/ $TEMPLATE_OPT $SPARQL_OPT --outprefix artist_recording
python mapping/mapfiles.py ./mapping/artist-artist-relation.sparql ./data/musicbrainz/artist/ ./resources/ $TEMPLATE_OPT $SPARQL_OPT --outprefix artist_artist_rel