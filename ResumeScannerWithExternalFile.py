import json

import spacy
import re
from spacy.pipeline import EntityRuler

nlp = spacy.load("en_core_web_sm")

resume_text = """

John Doe

Email: john.doe@example.com
Phone: +1 9876543210

Education:
Bachelor of Science in Computer Science, XYZ University

Skills:
Python, Java, SQL, Machine Learning, Deep Learning

Experience:
Software Engineer at ABC Corp (2019-2022)
Intern at DEF Ltd (2018)

"""


doc = nlp(resume_text)

with open("patterns.json","r") as f:
    patterns = json.load(f)


ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns(patterns)

doc = nlp(resume_text)


def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_phone_no(text):
    phone_no_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}"
    match  = re.search(phone_no_pattern,text)
    return match.group(0) if match else None

def extract_email(text):
    email_pattern =  r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern,text)
    return match.group(0) if match else None

def prase_resume(text):
    doc = nlp(text)
    name = extract_name(doc)
    email = extract_email(text)
    phone_number = extract_phone_no(text)
    list_of_exp = ["intern", "engineer", "developer", "manager"]
    list_of_education = ["bachelor","master","phd","b.sc","m.sc", "university","college", "school"]

    data = {"Name": name,
        "Email": email,
        "Phone_No": phone_number,
        "Skills": [],
        "Education": [],
        "Work_Experience": []

    }



    for ent in doc.ents:

        if ent.label_ == "SKILL":
            data["Skills"].append(ent.text)

        if ent.label_ == "EDUCATION":
            data["Education"].append(ent.text)

        if ent.label_ == "WORK_EXP":
            data["Work_Experience"].append(ent.text)

    lines = text.split("\n")

    experience_lines = []
    education_lins = []
    lines = text.split("\n")
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in list_of_exp):
            experience_lines.append(line.strip())

        if any(keyword in line_lower for keyword in list_of_education):
            education_lins.append(line.strip())
    data["Work_Experience"] = experience_lines
    data["Education"] = education_lins



    data["Skills"] = list(set(data["Skills"]))
    data["Education"] = list(set(data["Education"]))
    data["Work_Experience"] = list(set(data["Work_Experience"]))



#    print(f" Name: {name}\n Email: {email}\n Phone number: {phone_number}\n Skills: {list(set(skills))}\n Education: {list(set(education))}\n Work Experience: {list(set(work_exp))}")

    return(data)


for key, value in prase_resume(resume_text).items():
    print(f"{key}:{value}")





