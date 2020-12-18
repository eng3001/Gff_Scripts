#!/usr/bin/python3
import argparse
import re

################################################################################
# Author: Wyatt Eng (12/1/20) & Taehyung Kwon
# Goal: This script is to be used to convert a jgi file to a properly formatted gff3 file
################################################################################

#Set input variables
def get_args():
    parser = argparse.ArgumentParser(description="Edit the 'Note' portion of Gff file")
    parser.add_argument("-f", "--jgi_file", help="required argument, input jgi file path", type=str)
    parser.add_argument("-o", "--out", help="gff3 outfile path / Default = 'out.gff'", type=str, default="out.gff3")
    return parser.parse_args()

args = get_args()
IN_FILE = args.jgi_file
OUT_FILE = args.out

# seqid - name of the chromosome or scaffold; chromosome names can be given with or without the 'chr' prefix. Important note: the seq ID must be one used within Ensembl, i.e. a standard chromosome name or an Ensembl identifier such as a scaffold ID, without any additional content such as species or assembly. See the example GFF output below.
# source - name of the program that generated this feature, or the data source (database or project name)
# type - type of feature. Must be a term or accession from the SOFA sequence ontology
# start - Start position of the feature, with sequence numbering starting at 1.
# end - End position of the feature, with sequence numbering starting at 1.
# score - A floating point value.
# strand - defined as + (forward) or - (reverse).
# phase - One of '0', '1' or '2'. '0' indicates that the first base of the feature is the first base of a codon, '1' that the second base is the first base of a codon, and so on..
# attributes - A semicolon-separated list of tag-value pairs, providing additional information about each feature. Some of these tags are predefined, e.g. ID, Name, Alias, Parent - see the GFF documentation for more details.


def clean_attributes(list):
    '''This function reformats the attribute section from jgi to gff3 format'''
    list_length = len(list)
    extract_attributes = list[8:list_length]
    extract_attributes[0] = "ID"
    ID = extract_attributes[1]
    ID = ID.replace('"',"")
    ID = ID.replace(";","")
    # Check to see if "transcriptID" exists in feature
    if any("transcript" in s for s in extract_attributes):
        index = [idx for idx, s in enumerate(extract_attributes) if 'transcript' in s][0]
        tran_index = int(index) + 1
        transcript_ID = extract_attributes[tran_index]
    else:
        transcript_ID = None
    length_extracted = len(extract_attributes)
    # This while loop adds a '=' at every odd index of the list
    while length_extracted > 1:
        length_extracted -= 1
        if length_extracted % 2 != 0:
            extract_attributes.insert(length_extracted, "=")
    extract_attributes = "".join(extract_attributes)
    extract_attributes = extract_attributes.replace('"',"")
    clean_list = list[0:8]
    clean_list.append(extract_attributes)
    return(clean_list, list[3], list[4], ID, transcript_ID)


o_file = open(OUT_FILE, 'w')
o_file.write("##gff-version 3" + "\n")
line_count = 0

Gene_Feature_list = []

old_clean_list = []
gene_count = -1
gene_start = 0
gene_end = 0
gene_ID = ""
gene_trID = ""

with open(IN_FILE) as file:
    for line in file:
        line_count+=1
        line = line.strip()
        line_list = line.split()
        clean_feature_list, start, end, ID, tran_ID = clean_attributes(line_list)

        if gene_count == -1:
            old_clean_list = clean_feature_list
            gene_start = start
            gene_end = end
            gene_ID = ID
            if tran_ID != None:
                gene_trID = str(tran_ID)
            gene_count += 1

        if gene_ID != ID:
            # Output the gene mRNA and gene_features
            # Reset start, end, and ID
            gene_count += 1
            out_gene_line = old_clean_list[0:8]
            out_gene_line[2] = "gene"
            out_gene_line[4] = str(gene_end)
            gene_attribute = f"ID=gene_{gene_ID};Name={gene_ID}"	#changed
            out_gene_line.append(gene_attribute)
            out_gene_line = "\t".join(out_gene_line)
            o_file.write(out_gene_line + "\n")

            out_mRNA_line = old_clean_list[0:8]
            out_mRNA_line[2] = "mRNA"
            out_mRNA_line[4] = str(gene_end)
            mRNA_attribute = f"ID=mrna_{gene_ID};Parent=gene_{gene_ID};Name={gene_ID};orig_transcript_ID={gene_trID}"		#changed
            out_mRNA_line.append(mRNA_attribute)
            out_mRNA_line = "\t".join(out_mRNA_line)
            o_file.write(out_mRNA_line + "\n")

            for item in Gene_Feature_list:
                item_string="\t".join(item)
                item_string2="{0}\tID={1}_{2};Parent=mrna_{2}\n".format('\t'.join(item_string.split('\t')[:-1]),
					item[2].lower(),
					gene_ID)	#changed
                o_file.write(item_string2)	#changed

            gene_start = start
            gene_end = end
            gene_ID = ID
            old_clean_list = clean_feature_list
            Gene_Feature_list.clear()
            Gene_Feature_list.append(clean_feature_list)
            if tran_ID != None:
                gene_trID = str(tran_ID)

        # If line is a feature of a gene
        else:
            if int(end) > int(gene_end):
                gene_end = end
            Gene_Feature_list.append(clean_feature_list)



o_file.close()
