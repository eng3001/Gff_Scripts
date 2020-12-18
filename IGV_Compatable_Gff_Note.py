#!/bin/python
import argparse
import re

###############################################################################
# File Name: IGV_Compatable_Gff_Note.py
#
# Function: This script it to be used to edit the "Note" section of the gff file
#           into IGV compatable. Turns "Note" section into a one liner.
#           Script is to be used after functional annotation
#           pipeline when using InterProScan and/or UniProt Databases.
#
# Example:  Old Gff Note "Similar to IPS3: Probable inositol 3-phosphate synthase isozyme3 (Arabidopsis thaliana OX=3702)"
#           New Gff Note "Similar_to_IPS3:_Probable_inositol_3-phosphate_synthase_isozyme3_(Arabidopsis_thaliana_OX=3702)"
#
# Author: Wyatt Eng
###############################################################################

#Set input variables
def get_args():
    parser = argparse.ArgumentParser(description="Edit the 'Note' portion of Gff file \
    in order to be viewed on IGV. ' ' are replaced with '_'")
    parser.add_argument("-f", "--file", help="required arg, input gff file path", type=str)
    parser.add_argument("-o", "--out", help="required arg, outfile name", type=str)
    return parser.parse_args()

args = get_args()
IN_FILE = args.file
OUT_FILE = args.out

o_file = open(OUT_FILE, 'w')

with open(IN_FILE) as file:
    for line in file:
        if "Note" in line:
            line = line.strip()
            line_list = line.split("\t")
            col_8 = line_list[8].split(";")
            note = col_8[-2]
            new_note = note.replace(" ", "_")
            col_8[-2] = new_note
            supernator=";"
            string_col_8 = supernator.join(col_8)
            line_list[8] = string_col_8
            tab_supernator = "\t"
            new_line = tab_supernator.join(line_list)
            new_line = new_line + "\n"
            o_file.write(new_line)
        else:
            o_file.write(line)


o_file.close()
