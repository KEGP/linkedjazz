from glob import glob
import json
import requests
from lxml import etree
from io import StringIO
import textdistance as td
from itertools import chain
from tqdm import tqdm
import os

cur_dir = os.path.dirname(__file__)
annotations = glob(os.path.join(cur_dir, "/chord_annotations/*.json"))

for ann in (pbar := tqdm(annotations)):
  with open(ann) as fp:
    json_ann = json.load(fp)
  
  parts = json_ann["parts"]
  
  for idx, part in enumerate(parts):
    # extract the chords of the said part
    if "chords" in part:
      chords = part["chords"]

      # remove leading and traling | for better split
      chords = map(lambda s: s[1:-1], chords)
      # split each progression into bars
      chords = list(map(lambda c: c.split("|"), chords))
      # split each bar into list of chords
      chords = [list(map(str.split, bar)) for bar in chords]

      # set new chords structure
      json_ann["parts"][idx]["chords"] = chords    

  # overwrite file with newly created content
  with open(ann, "w") as fp:
    json.dump(json_ann, fp)  