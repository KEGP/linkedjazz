from tqdm import tqdm
import argparse
from glob import glob
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("query", help="Path to the sparql query where files will be mapped.")
parser.add_argument("input_directory", help="Input directory containing the file that will be mapped to a query.")
parser.add_argument("output_directory", help="Output directory where content will be generated.")

parser.add_argument('--sparqlanything', help="Path to the sparql anything jar. If none will try the current directory.", default="./sparql-anything-0.6.0.jar")
parser.add_argument('--template-name', help="Name used in the SPARQL query for the naming template, which will be used by sparqlanything. Defaults to name.", default="name")
parser.add_argument('--format', help="Serialization format used by SPARQLAnything. Defaults to turtle.", default="ttl")
parser.add_argument('--outprefix', help="Prefix added to the outfile. Defaults to empty string.", default="")
args = parser.parse_args()

files = os.listdir(args.input_directory)
sparqlanything_path = os.path.abspath(args.sparqlanything)
format = args.format

for file in tqdm(files):
  filepath = os.path.join(args.input_directory, file)
  outpath = os.path.join(args.output_directory, f"{args.outprefix}_{file}.ttl")

  with open(outpath, "w") as outfile:
    process = f"java -jar {sparqlanything_path} -q {args.query} -v {args.template_name}={filepath} -f {format} > {outpath}"
    subprocess.run(process.split(), stdout=outfile, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)