#!/bin/python
import argparse
import re, mmap

###############################################################################
# File Name: Add_Gff_Note_To_FASTA.py
#
# Function: This script it to be used to add the "Note" section of the gff file
#           into the fasta header. Script is to be used after functional annotation
#           pipeline when using InterProScan and/or UniProt Databases.
#
# Example:  Old header ">Contig_1"
#           New Header ">Contig_1 Name:'Similar to IPS3: Probable inositol 3-phosphate synthase isozyme3 (Arabidopsis thaliana OX=3702)'"
#
# Author: Wyatt Eng
###############################################################################

#Set input variables
def get_args():
    parser = argparse.ArgumentParser(description="Script changes the amino acid \
    (faa) or nucleotide (fna) fasta contig header names by appending the gff \
    'notes' section to the fasta header")
    parser.add_argument("-gff", "--gff_file", help="input gff file path", type=str)
    parser.add_argument("-fa", "--fasta_file", help="input amino acid fasta file path", type=str)
    parser.add_argument("-o_fa", "--out_fa", help="outfile name for genome file", type=str)
    return parser.parse_args()

#Define passed in arguments
args = get_args()
GFF_FILE = args.gff_file
FA_FILE = args.fasta_file
OUT_FA_FILE = args.out_aa

#Open new FASTA file to write reads to
o_fa_file = open(OUT_FA_FILE, 'w')

#counter will be used to keep track of the number of scaffolds
counter = 0
#Open Fasta File
with open(FA_FILE) as aa_file:
    for line in aa_file:
        if line.startswith(">"):
            counter += 1
            line = line.strip()
            #Regex search for the header and save the header to the variable
            fasta_header_re = re.search('>(.*)',line) #Extract header after '>'
            fasta_header = fasta_header_re.group(1)
            regex = fasta_header + ";Note=(.+);"

            #Search through the gff file to find where the contig header is located
            #Capture the Note portion after "Note"
            with open(GFF_FILE) as gf:
                for line in gf:
                    if re.search(regex, line):
                        Note = re.search(regex, line)
                        break

            #Reformat new header and write out to file
            new_header = Note.group(1)
            final_header = new_header.replace("_", " ")
            out_header = ">" + fasta_header + ' protein Name:"' + final_header + '"\n'
            o_fa_file.write(out_header)
        else:
            #Write non header lines to file
            o_fa_file.write(line)

o_fa_file.close()
