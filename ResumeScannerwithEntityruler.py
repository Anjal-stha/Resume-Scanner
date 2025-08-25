import spacy
import re
from spacy.pipeline import EntityRuler

nlp = spacy.load("en_core_web_sm")

resume_text = """

JJohn Doe
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

def prase_resume():
    name = extract_name(doc)
    email = extract_email(resume_text)
    phone_number = extract_phone_no(resume_text)

    skills = []
    education = []
    work_exp = []

    for ent in doc.ents:
        if ent.label_ == "SKILL":
            skills.append(ent.text)

        if ent.label_ == "EDUCATION":
            education.append(ent.text)

        if ent.label_ == "WORK_EXP":
            work_exp.append(ent.text)

    return({
        "Name": name,
        "Email": email,
        "Phone_No": phone_number,
        "Skills": list(set(skills)),
        "Education": list(set(education)),
        "Work Experience": list(set(work_exp))
    })


print(prase_resume())





