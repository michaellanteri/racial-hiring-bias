# Makes a dataset that lists the jobs for each resume

#%%
import json

resumes = []
# Flag so we don't list multiple designations for one resume, only the first
flag = 0

with open("./datasets/og_resumes.json", "r") as data:
    for line in data:
        resumes.append(json.loads(line))
    
    with open("./datasets/jobs.csv", "w") as jobs:
        jobs.write("resume,job\n")

        counter = 0
        for resume in resumes:
            jobs.write(str(counter) + ",")
            
            # If the label is "Designation"
            for label in resume["annotation"]:
                if len(label.get("label")) > 0 and label.get("label")[0] == "Designation" and flag != 1:
                    # Write the job
                    job = label.get("points")[0].get("text").strip()
                    jobs.write(job)
                    # Flag = 1 so we continue to the next resume
                    flag = 1
            
            jobs.write("\n")
            flag = 0
            counter += 1