
import re
from typing import List, Tuple

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
PHONE_RE = re.compile(r'(?:\+?\d{1,3}[\s-]?)?(?:\(\d{2,4}\)|\d{2,4})[\s-]?\d{3,4}[\s-]?\d{3,4}')
URL_RE = re.compile(r'(https?://\S+)')

# A compact skills dictionary; extend as needed
KNOWN_SKILLS = [
    "python","java","c++","c","javascript","typescript","node","react","angular","vue",
    "html","css","tailwind","bootstrap","fastapi","flask","django","spring","mysql",
    "postgres","mongodb","redis","docker","kubernetes","aws","gcp","azure","git",
    "linux","bash","pandas","numpy","scikit-learn","tensorflow","pytorch","llm",
    "langchain","prompt engineering","nlp","cv","ml","dl","data analysis","rest api",
]

def find_emails(text:str)->List[str]:
    return list(dict.fromkeys(EMAIL_RE.findall(text)))

def find_phones(text:str)->List[str]:
    return list(dict.fromkeys(PHONE_RE.findall(text)))

def find_urls(text:str)->List[str]:
    return list(dict.fromkeys(URL_RE.findall(text)))

def extract_skills(text:str)->List[str]:
    text_low = text.lower()
    hits = [s for s in KNOWN_SKILLS if s in text_low]
    dedup = list(dict.fromkeys(hits))
    return dedup

def guess_name(text:str)->str:
    # naive heuristic: first line with at least 2 capitalized words
    for line in text.splitlines():
        words = line.strip().split()
        caps = [w for w in words if w[:1].isupper() and w[1:].islower()]
        if len(caps) >= 2 and len(line) <= 60:
            return line.strip()
    return ""

def rate_resume(skills:List[str])->int:
    # very simple heuristic: scale to 10
    cap = 20
    return min(10, max(4, int(round(len(skills)/cap*10)) + 5))
