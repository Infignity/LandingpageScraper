
def strip_text(text):
    return " ".join([string for string in text.strip().replace("\n","").split(" ") if string])
