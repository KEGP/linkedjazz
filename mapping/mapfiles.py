from tqdm import tqdm
import argparse
from glob import glob
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("query", help="Path to the sparql query where files will be mapped.")
parser.add_argument("input_directory", help="Input directory containing the file that will be mapped to a query.")
parser.add_argument("output_directory", help="Output directory where content will be generated.")

parser.add_argument('--sparqlanything', help="Path to the sparql anything jar. If none will try the current directory.", default="./sparql-anything-0.7.0.jar")
parser.add_argument('--template-name', help="Name used in the SPARQL query for the naming template, which will be used by sparqlanything. Defaults to name.", default="name")
parser.add_argument('--format', help="Serialization format used by SPARQLAnything. Defaults to turtle.", default="ttl")
parser.add_argument('--outprefix', help="Prefix added to the outfile. Defaults to empty string.", default="")
args = parser.parse_args()

files = os.listdir(args.input_directory)
sparqlanything_path = os.path.abspath(args.sparqlanything)
format = args.format

already_processed_release_files = set()
for file in tqdm(files):
  filepath = os.path.join(args.input_directory, file)

  if (file.startswith("release_")):  # checks whether 'file' is a release file or not
    unique_release_file = file.rsplit("_", maxsplit=1)[0]  # removes the "_<NUM>.json" part of the filename
    if (unique_release_file not in already_processed_release_files):
      already_processed_release_files.add(unique_release_file)
    else:
      # We want to skip this release file because it's a duplicate!
      continue

  outpath = os.path.join(args.output_directory, f"{args.outprefix}_{file}.ttl")

  with open(outpath, "w") as outfile:
    process = f"java -jar {sparqlanything_path} -q {args.query} -v {args.template_name}={filepath} -f {format} > {outpath}"
    subprocess.run(process.split(), stdout=outfile, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)