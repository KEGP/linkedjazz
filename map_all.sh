#!/bin/bash

SPARQL_OPT="--sparqlanything ./sparql-anything-0.7.0.jar"
TEMPLATE_OPT="--template-name name"

python mapping/mapfiles.py ./mapping/chord-annotations.sparql ./data/jaah/chord_annotations/ ./resources/chord/ $TEMPLATE_OPT $SPARQL_OPT
python mapping/mapfiles.py ./mapping/work.sparql ./data/musicbrainz/work/ ./resources/work/ $TEMPLATE_OPT $SPARQL_OPT
python mapping/mapfiles.py ./mapping/release.sparql ./data/musicbrainz/release/ ./resources/release/ $TEMPLATE_OPT $SPARQL_OPT
python mapping/mapfiles.py ./mapping/recording.sparql ./data/musicbrainz/recording/ ./resources/recording/ $TEMPLATE_OPT $SPARQL_OPT
python mapping/mapfiles.py ./mapping/artist.sparql ./data/musicbrainz/artist/ ./resources/artist/ $TEMPLATE_OPT $SPARQL_OPT
python mapping/mapfiles.py ./mapping/artist-work-relation.sparql ./data/musicbrainz/work/ ./resources/artist_work_rel/ $TEMPLATE_OPT $SPARQL_OPT
python mapping/mapfiles.py ./mapping/artist-recording-relation.sparql ./data/musicbrainz/recording/ ./resources/artist_recording_rel/ $TEMPLATE_OPT $SPARQL_OPT
python mapping/mapfiles.py ./mapping/artist-artist-relation.sparql ./data/musicbrainz/artist/ ./resources/artist_artist_rel/ $TEMPLATE_OPT $SPARQL_OPT
