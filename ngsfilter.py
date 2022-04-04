import pandas as pd
import os
from itertools import repeat
import json
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create .ngsfilter for STR NGS data analysis. Please, provide a path to configuration file in .json format.')
    parser.add_argument('-config', '--config_file', help='Path to configuraion file', metavar='Str', default='ALL')
    args = parser.parse_args()
    config_file = args.config_file

    with open(config_file, 'r') as f:
      params = json.load(f)

    project = params["Output_path"]
    if not os.path.exists(project):
        print("Incorrect project folder. Please, check your path!")
        exit()
    output_path = f"{project}/ngsfilters/"
    if not os.path.exists(output_path):
            os.mkdir(output_path)
    ngsfilters = []
    for lib in params["Batches"]:
        tags = lib["Tags"]
        if not os.path.isfile(tags):
            print("Tag combination file is not found (--tags argument is incorrect). Please, check your path")
            exit()
        tagcombo = pd.read_csv(tags, sep="\t")

        if not (tagcombo.nunique() == len(tagcombo)).all():
            print("Tag combinations are not unique. Check the tag combo.")

        if not os.path.isfile(lib["Primers"]):
            print("Primers file is not found. Please, check the path")
            exit()
        primers = pd.read_csv(lib["Primers"],  sep="\t")
        primers = primers[["locus", "primerF", "primerR"]].drop_duplicates()

        if not os.path.isfile(lib["Samples"]):
            print("Samples position file is not found. Please, check the path")
            exit()

        tagcombo = pd.melt(tagcombo, id_vars=['Position'], value_vars=lib["Tag_plates"])
        APfile = pd.read_csv(lib["Samples"],  sep="\t")
        APfile = APfile[["Sample","Position"]]
        APfile = APfile.merge(tagcombo, left_on= "Position", right_on="Position")

        intermediate = APfile.apply(
            lambda row: pd.DataFrame(list(zip(primers.iloc[:, 0], repeat(row["Sample"]),
                                              repeat(row["Position"]), repeat(row["variable"]), repeat(row["value"]),
                                              primers.iloc[:, 1], primers.iloc[:, 2], repeat("F"),
                                              repeat("@")))), axis=1)

        ngsfilters.append(pd.concat(intermediate.tolist()))

    ngsfilter = pd.concat(ngsfilters)
    ngsfilter[1] = ngsfilter[[1, 2, 3]].apply(lambda row: '__'.join(row.values.astype(str)),
                                                        axis=1)  # prepare sample names in format ID_position_PP
    ngsfilter = ngsfilter.sort_values([3,0])  # sort by PP, position and loci name
    ngsfilter = ngsfilter.drop(columns=[2, 3])  # remove extra columns
    name = params["Library"]
    ngsfilter.to_csv(output_path + name + ".ngsfilter", sep="\t", header=False, index=False)
    print(f"{name}.ngsfilter created in {output_path}.")
    with open(f"{project}/read_names.txt", 'w') as f:
        f.write('\t'.join([str(x) for x in [i[0] for i in params["Reads"]]]) + "\n")
        f.write('\t'.join([str(x) for x in [i[1] for i in params["Reads"]]]) + "\n")
        f.write(lib["Primers"])
        f.close()

