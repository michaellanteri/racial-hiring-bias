# Makes a dataset that tab-separates each HBCU to a a non-HBCU ("US" college) with a similar rank (+-3)

import helpers
import random

TYPES = ["college", "name"]

def load_pairs(type):

    if(type not in TYPES):
        print(f"{type} not in list of TYPES")
        exit()
    
    # Open needed files and turn csv's into lists
    if(type == "college"):
        us_colleges = helpers.open_csv("us_matches")
        hbcu_colleges = helpers.open_csv("hbcu_colleges")

        with open("./data/pairs/pairs_college.txt", "w") as pairs:
            # For every HBCU in the list
            for hbcu in hbcu_colleges[1:]:
                for us_college in us_colleges[1:]:
                    # If the HBCU is +-3 in rank, add it to our file to tab-separate (excluding the matching to itself)
                    if(int(us_college[0]) in range(int(hbcu[0])-3, int(hbcu[0])+4) and us_college[0] != hbcu[0]):
                        pairs.write(hbcu[1] + '\t' + us_college[1])
                        pairs.write("\n")

    elif(type == "name"):
        us_firstnames = helpers.open_csv("us_firstnames")
        us_lastnames = helpers.open_csv("us_lastnames")
        aa_firstnames = helpers.open_csv("aa_firstnames")
        aa_lastnames = helpers.open_csv("aa_lastnames")

        with open("./data/pairs/pairs_name.txt", "w") as pairs:
            for _ in range(200):
                idx = random.randint(1, len(aa_firstnames)-1)
                first = aa_firstnames[idx][0]
                idx = random.randint(1, len(aa_lastnames)-1)
                last = aa_lastnames[idx][0]
                full = " ".join((first, last))
                pairs.write(full + '\t')

                idx = random.randint(1, len(us_firstnames)-1)
                first = us_firstnames[idx][0]
                idx = random.randint(1, len(us_lastnames)-1)
                last = us_lastnames[idx][0]
                full = " ".join((first, last))
                pairs.write(full + "\n")

load_pairs("college")
load_pairs("name")