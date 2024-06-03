import random
import csv
import json

LOW_RANK = -3
HIGH_RANK = 3

# Get a US college matched to an HBCU college
def get_matched_college(us_colleges, hbcus, hbcu_college):
    # Loop through the colleges csv to find the school, then get its rank
    hbcu_college_rank = 0
    for col in hbcus[1:]:
        if(col[1] == hbcu_college):
            hbcu_college_rank = int(col[0])

    # Get a random non-zero factor
    rand_factor = 0
    while(rand_factor == 0):
        rand_factor = random.randint(LOW_RANK, HIGH_RANK)

    # Match the HBCU to a non-HBCU by taking the rank and adding a random factor (to get a non-HBCU)
    rank_match = hbcu_college_rank + rand_factor
    
    # Get and update the college to the HBCU match
    for col in us_colleges[1:]:
        if(int(col[0]) == rank_match):
            us_college = col[1]
    
    #print(hbcu_college + "\t" + us_college)

    return us_college

# Given a JSON file, we want to extract the content and the annotations, and then replace the text at the points with the text from the "text" field in the annotation.
def replace_text_at_points(content, points, names):
    cumulative_offset = 0
    new_content = content
    new_points = []
    
    zipped = list(zip(points, names))

    # Sort the zipped list by points' start indices in ascending order
    zipped.sort(key=lambda x: x[0]["start"])

    for point, name in zipped:
        start, end = point["start"], point["end"] + 1
        text = name
        # Update the start and end indices to reflect the cumulative offset
        new_start = start + cumulative_offset
        end += cumulative_offset
        # Replace the text between the start and end indices with the new college name
        new_content = new_content[:new_start] + text + new_content[end:]
        # Update the cumulative offset
        new_end = new_start + len(text)
        cumulative_offset += new_end - end
        # Append the new point to the list of new points
        new_points.append({"start": new_start, "end": new_end, "text": text})

    #print(new_points)
    #print(new_content)
    return new_content, new_points

# Given a two lists of resumes, and a file name, we want to tab-separate elements in the list and write it to a .txt file
def tab_separate_resumes(aa_resumes, us_resumes, filename):
    with open(f"./data/pairs/{filename}.txt", "w", encoding="utf8") as new_resumes:
        for aa_resume, us_resume in zip(aa_resumes, us_resumes):
            aa_content = aa_resume["content"].replace("\n", "\\n")
            us_content = us_resume["content"].replace("\n", "\\n")
            new_resumes.write(aa_content + '\t' + us_content)
            new_resumes.write("\n")

def open_csv(filename):
    with open(f"./datasets/{filename}.csv", "r", encoding="utf8") as fp:
        return list(csv.reader(fp))
    
def save_json(resumes, filename):
    with open(f"./data/jsons/{filename}.json", "w", encoding="utf8") as new_resumes:
        new_resumes.seek(0)
        new_resumes.truncate()
        for resume in resumes:
            json.dump(resume, new_resumes)
            new_resumes.write("\n")