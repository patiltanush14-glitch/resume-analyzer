import PyPDF2

def extract_text(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except:
        return "ERROR"

    return text.lower()

def analyze_resume(text, skills_list):
    found_skills = []
    missing_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int((len(found_skills) / len(skills_list)) * 100)

    suggestions = []

    if score < 50:
        suggestions.append("Add more relevant technical skills.")
    if "project" not in text:
        suggestions.append("Include project experience.")
    if "experience" not in text:
        suggestions.append("Add work experience or internships.")
    if "education" not in text:
        suggestions.append("Mention your education details.")

    return score, found_skills, missing_skills, suggestions