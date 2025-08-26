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

patterns = [
    # Skills
    {"label": "SKILL", "pattern": "Python"},
    {"label": "SKILL", "pattern": "Java"},
    {"label": "SKILL", "pattern": "C++"},
    {"label": "SKILL", "pattern": "Machine Learning"},
    {"label": "SKILL", "pattern": "Deep Learning"},
    {"label": "SKILL", "pattern": "SQL"},

    # Education / Qualifications
    {"label": "EDUCATION", "pattern": "Bachelor"},
    {"label": "EDUCATION", "pattern": "Master"},
    {"label": "EDUCATION", "pattern": "PhD"},
    {"label": "EDUCATION", "pattern": "B.Sc"},
    {"label": "EDUCATION", "pattern": "M.Sc"},
    {"label": "EDUCATION", "pattern": "University"},
    {"label": "EDUCATION", "pattern": "College"},

    # Work Experience (keywords)
    {"label": "WORK_EXP", "pattern": "Software Engineer"},
    {"label": "WORK_EXP", "pattern": "Data Scientist"},
    {"label": "WORK_EXP", "pattern": "Intern"},
    {"label": "WORK_EXP", "pattern": "Developer"},


]

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

    for line in lines:
        if any(word in line.lower() for word in list_of_exp):
            data["Work_Experience"].append(line.strip())

    data["Skills"] = list(set(data["Skills"]))
    data["Education"] = list(set(data["Education"]))
    data["Work_Experience"] = list(set(data["Work_Experience"]))



#    print(f" Name: {name}\n Email: {email}\n Phone number: {phone_number}\n Skills: {list(set(skills))}\n Education: {list(set(education))}\n Work Experience: {list(set(work_exp))}")

    return(data)


for key, value in prase_resume(resume_text).items():
    print(f"{key}:{value}")





