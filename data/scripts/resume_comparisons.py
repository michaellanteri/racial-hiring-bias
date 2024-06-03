import random
import helpers
import json

TYPES = ["college", "name"]

# Changes variable "type" in the resume to an AA dataset and US dataset
def change_variable(type=None, resumes=None, type2=None):
    
    # Check if we can change this variable
    if(type not in TYPES):
        print(f"Error: {type} not in list of TYPES")
        exit()

    # Lists to store each resume
    og_resumes = []
    aa_resumes = []
    us_resumes = []

    # Open file with original resumes
    with open("./datasets/og_resumes.json", "r", encoding="utf8") as og_resumes_fp:
            # Fill resumes list with original resumes
            for resume in og_resumes_fp:
                og_resumes.append(json.loads(resume))
    
    # Open needed files and turn csv's into lists
    if(type == "college"):
        us_colleges = helpers.open_csv("us_matches")
        hbcus = helpers.open_csv("hbcu_colleges")
    elif(type == "name"):
        us_firstnames = helpers.open_csv("us_firstnames")
        us_lastnames = helpers.open_csv("us_lastnames")
        aa_firstnames = helpers.open_csv("aa_firstnames")
        aa_lastnames = helpers.open_csv("aa_lastnames")

    for resume in og_resumes:
        aa_resume = {"content": "", "annotation": []}
        us_resume = {"content": "", "annotation": []}

        if(type == "college"): desired_label = "College Name"
        elif(type == "name"): desired_label = "Name"

        og_points = []               
        for label in resume["annotation"]:
            # If the label is "College Name"
            if len(label.get("label")) > 0 and label.get("label")[0] == desired_label:
                for point in label.get("points"):
                    # Add the original college points to the list
                    og_points.append(point)
            else:
                # Add the label to the new resumes
                aa_resume["annotation"].append(label)
                us_resume["annotation"].append(label)

        # Text we need to replace
        og_text = []
        for point in og_points:
            og_text.append(point.get("text").strip())
        
        # Text we're replacing og_text with
        aa_text = []
        us_text = []
        
        if(type == "college"):
            # Get random HBCU colleges and US colleges matched to HBCU colleges
            random_hbcus = []
            us_matches = []

            for _ in range(0, len(og_text)):
                idx = random.randint(1, len(hbcus)-1)
                hbcu = hbcus[idx][1]
                random_hbcus.append(hbcu)

                us_college = helpers.get_matched_college(us_colleges, hbcus, hbcu)
                us_matches.append(us_college)
            
            aa_text = random_hbcus
            us_text = us_matches

        elif(type == "name"):
            # Get random AA names and random US names
            aa_names = []
            us_names = []

            for _ in range(0, len(og_text)):
                idx = random.randint(1, len(aa_firstnames)-1)
                first = aa_firstnames[idx][0]
                idx = random.randint(1, len(aa_lastnames)-1)
                last = aa_lastnames[idx][0]
                full = " ".join((first, last))
                aa_names.append(full)

                idx = random.randint(1, len(us_firstnames)-1)
                first = us_firstnames[idx][0]
                idx = random.randint(1, len(us_lastnames)-1)
                last = us_lastnames[idx][0]
                full = " ".join((first, last))
                us_names.append(full)
            
            aa_text = aa_names
            us_text = us_names

        # Replace text and content
        aa_content, aa_points = helpers.replace_text_at_points(resume["content"], og_points, aa_text)
        us_content, us_points = helpers.replace_text_at_points(resume["content"], og_points, us_text)
        
        aa_resume["content"] = aa_content
        us_resume["content"] = us_content

        # Add the new annotation
        for point in us_points:
            us_resume["annotation"].append({"label": [desired_label], "points": [point]})
        for point in aa_points:
            aa_resume["annotation"].append({"label": [desired_label], "points": [point]})

        if(type2):
            change_variable(type2, us_resumes)
            change_variable(type2, aa_resumes)
        
        us_resumes.append(us_resume)
        aa_resumes.append(aa_resume)

    # Save as individual json files with annotations, and a txt file without annotations
    helpers.save_json(us_resumes, f"resumes_us_{type}")
    helpers.save_json(aa_resumes, f"resumes_aa_{type}")
    helpers.tab_separate_resumes(aa_resumes, us_resumes, f"resumes_{type}")