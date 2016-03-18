## Get all the species of which the names contain "A. baumannii"
./tax_name_search.py --species A. baumannii
470        | B | Acinetobacter baumannii
765767     | U | Acinetobacter baumannii cloning vector pET-RA
765766     | U | Acinetobacter baumannii expression vector pAT-RA
765768     | U | Acinetobacter baumannii expression vector pOT-RA
175719     | E | Amorphophallus baumannii

## Get all the strains of Acinetobacter baumannii
./tax_strains_search.py 470
933265     | no rank          | Acinetobacter baumannii UMB003
945555     | no rank          | Acinetobacter baumannii WM99c
945556     | no rank          | Acinetobacter baumannii D1279779
980514     | no rank          | Acinetobacter baumannii TCDC-AB0715
981328     | no rank          | Acinetobacter baumannii W6976
981329     | no rank          | Acinetobacter baumannii W7282
992402     | no rank          | Acinetobacter baumannii ABNIH1
...

## Get sequences of all the proteins of Acinetobacter baumannii UMB003
./tax_strains_search.py --database protein 933265 933265_prot.fasta
