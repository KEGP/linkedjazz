from glob import glob
import json
import requests
from lxml import etree
from io import StringIO
import textdistance as td
from itertools import chain
from tqdm import tqdm
from collections import defaultdict

# download the html page containing the instrument list
res = requests.get("https://musicbrainz.org/instruments")
# parse the html page
root = etree.fromstring(res.content.decode("utf8"))
# instruments are contained in <a href="-mbid-"><bdi>...</bdi></a> elements
instruments_list = root.xpath("//a[bdi]")
# convert instruments in dict whose key is the instrument and value the MusicBrainz Id
instruments = defaultdict(lambda: "")
for i in instruments_list:
  instruments[i.xpath("string()").lower()] = i.get("href").split("/")[-1]

instruments_names = set(instruments.keys())
# there are some instruments who are not in MB but they have been used
# by the annotator (ensemble, vocal)]
instruments_names = instruments_names.union({"vocals male", "vocals female", "vocals", "drums"})
# load each annotation
annotations = glob("./data/chord_annotations/*.json")

# cache conversions
conversions = dict()

for ann in (pbar := tqdm(annotations)):
  with open(ann) as fp:
    json_ann = json.load(fp)
  
  parts = json_ann["parts"]
  
  for idx, part in enumerate(parts):
    # extract the name of the section, which might contain an instrument
    # if '-' is not present (the pattern has not been annotated) then the whole
    # string is returned
    splitted = part["name"].split("-")
    section_names = splitted if len(splitted) == 1 else splitted[:-1]
    pattern = None if len(splitted) == 1 else splitted[-1]

    # remove spaces and lower the text
    section_names = [s.lower().strip() for s in section_names]
    section_instruments = list()
    
    for sn in section_names:
      # if a comma or an & is present on the section name then more than 2 instruments are inserted
      sn_instruments = sn.split(",")
      sn_instruments = list(chain(*[sni.split("&") for sni in sn_instruments]))
      sn_instruments = list(chain(*[sni.split("/") for sni in sn_instruments]))
      # strip whitespace
      sn_instruments = map(str.strip, sn_instruments)

      for sn_instr in sn_instruments:
        # one recurring pattern seems to be the presence of "<instrument> solo"
        # the word solo might confuse the algorithm without any meaning for the
        # instrument recognition itself. we will remove it
        sn_instr_pp = sn_instr.replace("solo", "").strip()
        # another recurring pattern is the abbreviation of saxophone into sax
        sn_instr_pp = sn_instr_pp.replace("sax", "saxophone").strip()
      
        if sn_instr_pp not in conversions.keys():
          # compute similarity with MB instruments by using Ratcliff/Obershelp Pattern Recognition
          # algorithm
          scores = {i: td.ratcliff_obershelp.normalized_similarity(i, sn_instr_pp) for i in instruments_names}
          best = max(scores, key=scores.get)
          if scores[best] > 0.75: 
            conversions[sn_instr] = best            
        
        if sn_instr in conversions:
          section_instruments.append({
            "name": conversions[sn_instr],
            "mbid": instruments[conversions[sn_instr]]
          })

    # add instruments
    json_ann["parts"][idx]["instruments"] = section_instruments
    json_ann["parts"][idx]["pattern"] = pattern


  # overwrite file with newly created content
  with open(ann, "w") as fp:
    json.dump(json_ann, fp)  