#!/bin/python
import argparse
import re

###############################################################################
# Name: Change_Contig_Name_FA_and_Gff.py
#
# Function: Change the fasta header to user defined input and edit gff file
#           respectively. Check for gff symboles to translate ("%3D" or "%2C").
#           Makes notes compatable to view on IGV by replacing " " with "_".
#
# Author: Wyatt Eng
###############################################################################

#Set input variables
def get_args():
    parser = argparse.ArgumentParser(description="Script changes the genome \
    fasta contig names and makes gff 'notes' viewable on IGV.")
    parser.add_argument("-gff", "--gff_file", help="input gff file path", type=str)
    parser.add_argument("-o_gff", "--out_gff", help="outfile name for gff file", type=str)
    parser.add_argument("-fa", "--fasta_file", help="input genome fasta file path", type=str)
    parser.add_argument("-o_fa", "--out_fa", help="outfile name for genome file", type=str)
    parser.add_argument("-head", "--header", help="desired header text. Example: \
    'Nannochloropsis_sp_ColST_Contig_(#)' / contig number will be appended to the \
    end of the header and change based on contig order in file / Default Contig \
    Name 'Contig_(#)'", type=str, default='Contig_')
    return parser.parse_args()

args = get_args()
GFF_FILE = args.gff_file
OUT_GFF_FILE = args.out_gff
FA_FILE = args.fasta_file
OUT_FA_FILE = args.out_fa
HEADER = args.header

# Dictionary to store old fasta headers
new_header_dict = dict()

header_counter = 0

# Open output fasta file
o_fa_file = open(OUT_FA_FILE, 'w')

with open(FA_FILE) as genome_file:
    for line in genome_file:
        if line.startswith(">"):
            header_counter += 1
            line = line.strip()
            # Capture old fasta header
            fasta_header_re = re.search('>(.*)',line) #Extract header after '>'
            fasta_header = fasta_header_re.group(1)
            # Make new header & write it out to a file
            new_header = HEADER + str(header_counter)
            new_header_dict.setdefault(fasta_header, new_header)
            out_header = ">" + new_header + "\n"
            o_fa_file.write(out_header)
        else:
            # Write sequence lines
            o_fa_file.write(line)

o_fa_file.close()


o_gff_file = open(OUT_GFF_FILE, 'w')

# Edit associated gff contig name (Column 1 of gff)
with open(GFF_FILE) as file:
    for line in file:
        line = line.strip()
        line_list = line.split("\t")
        dict_val_head = new_header_dict.get(line_list[0])
        line_list[0] = dict_val_head
        if "Note" in line:
            col_8 = line_list[8].split(";")
            note = col_8[-2]
            # Account for hidden symbols
            new_note = note.replace(" ", "_")
            new_note = new_note.replace("%3D", "=")
            new_note = new_note.replace("%2C", ",")
            col_8[-2] = new_note
            supernator=";"
            string_col_8 = supernator.join(col_8)
            line_list[8] = string_col_8
            tab_supernator = "\t"
            new_line = tab_supernator.join(line_list)
            new_line = new_line + "\n"
            o_gff_file.write(new_line)
        else:
            tab_supernator = "\t"
            new_line = tab_supernator.join(line_list)
            new_line = new_line + "\n"
            o_gff_file.write(new_line)

o_gff_file.close()
