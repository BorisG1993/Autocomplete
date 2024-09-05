import re


def extract_words(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return [word.lower() for word in words]   