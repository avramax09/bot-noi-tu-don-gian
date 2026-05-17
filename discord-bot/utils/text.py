def normalize(text):
    return text.lower().strip()

def get_first_word(text):
    return normalize(text).split()[0]

def get_last_word(text):
    return normalize(text).split()[-1]
