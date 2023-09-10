import argparse, os
from collections import defaultdict
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--counts", help="file or list of files with counts", nargs="+", type=str)
    parser.add_argument("-head","--header", help="add header using count's file names yes/no [y/n]", choices=['y','n'], default="n", type=str)
    parser.add_argument("-o","--output", help="Outputfile directory", default=".", type=str)
    parser.add_argument("-n", "--norm_file", help="Normalization file specific format (view readme)", type=str)
    return parser.parse_args()

def get_norm_values(norm_file):
    values = {}
    with open(norm_file) as norm_file:
        for line in norm_file:
            line = line.strip()
            sample_id, value = line.split(" ")
            values[sample_id] = float(value)
    return(values)

if __name__ == "__main__":
#Set variables
    args = main()

    tables = args.counts

    tables = sorted(tables)

    #tables = tables.sort()

    header = args.header

    norm_file = args.norm_file

    outdir = args.output
    outpath = os.path.abspath(outdir)
    isExist = os.path.exists(outpath)
    if not isExist:
        os.makedirs(outpath)
    outpath = outpath + "/out_counts.tsv"

    out_counts = open(outpath, "w")
#Start building table
    if header == 'y':
        sampleids = []
        for filename in tables:
            filename = os.path.basename(filename)
            sampleid = os.path.splitext(filename) # remove extension
            sampleid = sampleid[0] # select strting before the dot
            sampleids.append(sampleid)
        head = "\t".join(sampleids)
        head = "prot_id" + "\t" + head + "\n"
        out_counts.write(head)
        #print("prot_id", head, sep="\t")

    uniq_ids = [] # unique ids

    group_sample = [] # group by samples

    for table in tables:
        table = open(table, "r")
        group_id = {} # group by ids
        group_sample.append(group_id)
        for line in table:
            line = line.strip()
            protid,count = line.split("\t")
            count = float(count) # in case we include normalization
            group_id.setdefault(protid, []).append(count)
            if protid not in uniq_ids:
                uniq_ids.append(protid) # add to unque ids list that is going to be use later
        table.close()

    for id_ in uniq_ids:
        for sample in group_sample:
            if id_ not in sample:
                sample[id_] = [0] # Add count = 0 if id not in sample table

    # Use default table to build final table with counts

    final_table = defaultdict(list) # Setdefault might be enough (like above)

    for sample in group_sample:
        sample = dict(sorted(sample.items())) # Don't know if necessary but just in case
        for id_, sample in sample.items():
            final_table[id_].extend(sample) # Add key to final table. If already exits update key with value using extend, everytime it loops (first loop)


    for v,k in final_table.items():
        if norm_file:
            norm_values = get_norm_values(norm_file)
            norm_values = dict(sorted(norm_values.items())) #Python 3.7+
            norm_values = list(norm_values.values())
            print(norm_values)
            k = np.array(k)
            k = np.where(k==0, 0, k/norm_values)
            k = k.tolist()
            k = [str(i) for i in k]
            k = "\t".join(k)
            line =v + "\t" + k
            out_counts.write(line + "\n")
        else:
            k = [str(i) for i in k]
            k = "\t".join(k)
            line =v + "\t" + k
            out_counts.write(line + "\n")
            

#    for v,k in final_table.items():
#        k = [str(i) for i in k]
#        k = "\t".join(k)
#        line =v + "\t" + k
#        out_counts.write(line + "\n")
#    
#    out_counts.close()




#####
#    if header == 'y':
#        sampleids = []
#        for filename in tables:
#            filename = os.path.basename(filename)
#            sampleid = os.path.splitext(filename) # remove extension
#            sampleid = sampleid[0] # select strting before the dot
#            sampleids.append(sampleid)
#        head = "\t".join(sampleids)
#        print("prot_id", head, sep="\t")
#
#    ids = []
#
#    for table in tables:
#        table = open(table, "r")
#        #counts = {}
#        for line in table:
#            protid,count = line.split("\t")
#            #counts.setdefault(protid, []).append(count)
#            if protid not in ids:
#                ids.append([protid])
#
#    for table in tables:
#        table = open(table, "r")
#        counts = {}
#        for line in table:
#            protid,count = line.split("\t")
#            count = int(count)
#            counts.setdefault(protid, []).append(count)
#        for n,id_ in enumerate(ids):
#            id_ = id_[0]
#            #print(id_)
#            if id_ not in counts:
#                ids[n].append(0)
#            else:
#                count = counts[id_][0] # [0] to transformto string
#                ids[n].append(count)
#
#    for i in ids:
#        print("\t".join(map(str, i)))
#