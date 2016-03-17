#!/usr/bin/env python

import sys, argparse
from taxonomylite import Taxonomy

parser = argparse.ArgumentParser(description="""Search strains of a species taxid in taxonomy database""")
parser.add_argument('--rank', dest='rank',
                    type = str,
                    help = 'show only strains at specified rank')
parser.add_argument('species_taxid', metavar='SPECIES_TAXID',
                    type=int,
                    help='taxid of the species')
args = parser.parse_args()

taxa_db = Taxonomy("taxonomy.db")

if taxa_db.tid_to_rank(args.species_taxid) != "species":
    print >>sys.stderr, "Error: incorrect species taxid"
    sys.exit(1)

all_children = taxa_db.children(args.species_taxid, deep=True)
if args.rank:
    for taxid in all_children:
        if taxa_db.tid_to_rank(taxid) == args.rank:
            print "%-10s | %s" % (taxid, taxa_db.tid_to_name(taxid))
else:
    for taxid in all_children:
        print "%-10s | %-16s | %s" % (taxid, taxa_db.tid_to_rank(taxid), taxa_db.tid_to_name(taxid))
