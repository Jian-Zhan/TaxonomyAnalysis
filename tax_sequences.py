#!/usr/bin/env python

import sys, argparse
from Bio import Entrez
from Bio import SeqIO
Entrez.email = "A.N.Other@example.com"

parser = argparse.ArgumentParser(description="""Retrieve sequences of a specified taxid""")
parser.add_argument('--database', dest='database',
                    type=str, default='protein',
                    choices = ['protein', 'nuccore'],
                    help = 'NCBI database. [DEFAULT: protein]')
parser.add_argument('--trials', dest='trials',
                    type=int, default=5,
                    help = 'Maximum number of trials. [DEFAULT: 5]')
parser.add_argument('tax_id', metavar='TAXID',
                    type=int)
parser.add_argument('out_fasta_file', metavar='OUT_FASTA_FILE',
                    type=argparse.FileType('w'))
args = parser.parse_args()

def print_progress(progress, file_handle=sys.stdout, prefix="", suffix="", length=20):
    progress = float(progress)
    if progress < 0:
        progress = 0.0
    elif progress > 1.0:
        progress = 1.0
    n = int(progress * length)
    file_handle.write("\r%s[%s%s]%s" % (prefix, '#'*n, ' '*(length-n), suffix))
    file_handle.flush()

def fetch_fasta(tax_id, out_file_handle, database = "protein"):
    ## Start esearch and store the WebEnv
    search_handle1 = Entrez.esearch(db=database, term = "txid%d[Organism:noexp]" % tax_id, retmax="1", usehistory="y")
    search_results1 = Entrez.read(search_handle1)
    search_handle1.close()
    count = int(search_results1["Count"])
    webenv1 = search_results1["WebEnv"]

    batch_size = 1000
    downloaded_gis = set()
    for start in range(0, count, batch_size):
        end = min(count, start+batch_size)

        ## Download GIs by esearch
        search_handle2 = Entrez.esearch(db=database, term = "txid%d[Organism:noexp]" % tax_id, webenv = webenv1, retstart=start, retmax=batch_size)
        search_results2 = Entrez.read(search_handle2)
        search_handle2.close()
        count2 = len(search_results2["IdList"])
        assert count2 == (end-start)
       
        ## Download FASTAs by efetch
        print_progress(float(start)/count, prefix="Download fasta sequence ", suffix = " ... [%d-%d]/%d" % (start,end,count))
        post_results = Entrez.read(Entrez.epost(db=database, id=",".join(search_results2["IdList"])))
        webenv2 = post_results["WebEnv"]
        query_key = post_results["QueryKey"]
        fetch_handle = Entrez.efetch(db=database, rettype="fasta",retmode="text", webenv=webenv2, query_key=query_key)
        data = fetch_handle.read()

        assert data.startswith(">"), data
        fetch_handle.close()
        out_file_handle.write(data)
    sys.stdout.write("\n")
    sys.stdout.flush()

n_trials = 0
while True:
    n_trials += 1
    if n_trials > args.trials:
        break

    try:
        fetch_fasta(args.tax_id, args.out_fasta_file)
    except:
        continue
    else:
        break

args.out_fasta_file.close()
