import argparse, os
import sys
import glob, pandas

#This script will consider length for both counts and 16S sequences when
#normalizing if the argument is given

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--counts", help="count matrix")
    #parser.add_argument("-p","--path", help="path to counts")
    parser.add_argument("-l","--length", help="mean length of 16S sequences present in library", type = float)
    parser.add_argument("-n","--number", help="number of 16S sequences present in library", type = float)
    return parser.parse_args()

if __name__ == "__main__":

    args = main()

    counts = args.counts

    length16s = args.length

    number16s = args.number

    #sample = os.path.basename(counts)

    #sample_name = sample.split(".")[0]

    #print("Geneid", sample_name, sep = "\t")

    if length16s == 0:
        print("Length of 16S cannot be 0. Exiting...")
        exit()

    if number16s == 0:
        print("Number 16S cannot be 0. Exiting...")
        exit()

    with open(counts, "r") as f:
#write smt to skip first line
        for line in f:
            line = line.split("\t")
            length, counts = float(line[5]), float(line[6])
            if length16s and number16s:
                try:
                    norm = (length/counts)/length16s/number16s
                except ZeroDivisionError:
                    norm = 0
                print(line[1], norm, sep="\t")
            elif number16s and length16s == None:
                try:
                    norm = (counts)/number16s
                except ZeroDivisionError:
                    norm = 0
                print(line[1], norm, sep="\t")

    

    #path = args.path

    #files = os.listdir(path)

    #matrix = {}
#
    #for file in files:
    #    
    #    sample = os.path.basename(file)
#
    #    sample_name = sample.split(".")[0]
#
    #    count_data = []
#
    #    with open(file, "r") as f:
    #        for x in range(2):
    #            next(f)
    #        for line in f:
    #            line = line.split("\t")
    #            length, counts = float(line[5]), float(line[6])
    #            if length16s and number16s:
    #                try:
    #                    norm = (length/counts)/length16s/number16s
    #                except ZeroDivisionError:
    #                    norm = 0
    #                append(line[1], norm, sep="\t")
    #            elif number16s and length16s == None:
    #                try:
    #                    norm = (counts)/number16s
    #                except ZeroDivisionError:
    #                    norm = 0
    #                print(line[1], norm, sep="\t")
#
#













    
    sample = os.path.basename(counts)

    sample_name = sample.split(".")[0]

    print("Geneid", sample_name, sep = "\t")

    with open(counts, "r") as f:
        for x in range(2):
            next(f)
        for line in f:
            line = line.split("\t")
            length, counts = float(line[5]), float(line[6])
            if length16s and number16s:
                try:
                    norm = (length/counts)/length16s/number16s
                except ZeroDivisionError:
                    norm = 0
                print(line[1], norm, sep="\t")
            elif number16s and length16s == None:
                try:
                    norm = (counts)/number16s
                except ZeroDivisionError:
                    norm = 0
                print(line[1], norm, sep="\t")



