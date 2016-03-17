#!/usr/bin/env python

import sys, argparse
from taxonomylite import Taxonomy

parser = argparse.ArgumentParser(description="""Search name in taxonomy database""")
parser.add_argument('--species', dest='species',
                    action = 'store_true', default = False,
                    help = 'search only species names')
parser.add_argument('--category', dest='category',
                    type = str, default = "",
                    choices = {"", "A", "B", "E", "V", "U"},
                    help = 'A: Archaea, B: Bacteria, E: Eukaryota, V: Viruses or Viroids, U: Unknown')
parser.add_argument('regex', metavar='REGEX',
                    type=str, nargs='+',
                    help='regular expression')
args = parser.parse_args()

regex = args.regex[0]
for r in args.regex[1:]:
    regex += ".*[ \t]+"
    regex += r

def tax_category(taxa_db, taxid):
    lineage = taxa_db.lineage(taxid)
    if 2157 in lineage:
        return 'A'
    elif 2 in lineage:
        return 'B'
    elif 2759 in lineage:
        return 'E'
    elif 10239 in lineage:
        return 'V'
    elif 12884 in lineage:
        return 'V'
    else:
        return 'U'

taxa_db = Taxonomy("taxonomy.db")

matched_tids = taxa_db.name_regex_to_tids(regex)

for taxid in matched_tids:
    if args.species:
        if taxa_db.tid_to_rank(taxid) != "species":
            continue
    c = tax_category(taxa_db, taxid)
    if args.category and c != args.category:
        continue
    print "%-10s | %s | %s" % (taxid, c, taxa_db.tid_to_name(taxid))
