import spacy
import re
from spacy.matcher import Matcher,PhraseMatcher


nlp = spacy.load("en_core_web_sm")
skills_list = ["Python", "Java", "C++", "SQL", "NLP", "Machine Learning", "Deep Learning", "Data Analysis"]
education_keywords = ["Bachelor", "Master", "B.Sc", "M.Sc", "PhD", "University", "College"]

resume_text = """
John Doe
Email: johndoe@gmail.com
Phone: +1-234-567-8901

Education:
Bachelor of Science in Computer Science, ABCD University, 2023

Skills:
Python, Java, C++, Machine Learning, Data Analysis, NLP, SQL

Experience:
Software Development Intern, ABC Tech, 2022-2023
Worked on backend APIs and NLP-based chatbot.

"""

doc = nlp(resume_text)

def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern,text)
    if match is not None:
        return match.group(0)
    return 0

def extract_phone_no(text):
    phone_number_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}"
    match = re.search(phone_number_pattern,text)
    if match is not None:
        return match.group(0)
    return 0

def extract_skill(skills_list):
    matcher =   PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in skills_list]
    matcher.add("SKILLS",patterns)

    matches = matcher(doc)

    found_skills = list({doc[start:end].text for match_id, start, end in matches})
    return found_skills

def extract_education(text):
    education_keywords = ["Bachelor", "Master", "B.Sc", "M.Sc", "PhD", "University", "College"]
    lines = text.split("\n")
    education = [line.strip() for line in lines if any(word in line for word in education_keywords)]
    return education


def extract_work(text):
    work_keyword = ["Intern", "Engineer", "Developer", "Manager","API","backend"]
    lines = text.split("\n")
    work = [line.strip() for line in lines if any(word in line for word in work_keyword)]
    return work


extracted_data = {
    "name": extract_name(doc),
    "Email": extract_email(resume_text),
    "Phone_Number": extract_phone_no(resume_text),
    "Skills": extract_skill(skills_list),
    "Education": extract_education(resume_text),
    "Work_exp":extract_work(resume_text)
}

for key,value in extracted_data.items():
    print(f"{key}: {value}")





