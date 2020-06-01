import re

def read_text(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
    return text

def processing_text(text):
    needed_rows = re.findall(r'[А-ЯЁ]́?[А-ЯЁ]+.+?\n', text)
    return needed_rows

def delete_variations(text):
    pattern = '/.+?[,.](/n)?'
    return re.sub(pattern, ',', text)

def simplify_charachters(text):
    return re.sub('́', '', text).lower()

def delete_markers(text):
    pattern = '[а-яё]+?\.( ,)?'
    return re.sub(pattern, '', re.sub('\.\n', '', text))

def delete_punct(text):
    return  re.sub(',', '', text)

def flip_text(text):
    text = delete_markers(simplify_charachters(delete_variations(text)))
    return re.sub('  +', ' ', re.sub(' ? ?', ' ', text))

def create_dict(filename):
    entries = processing_text(read_text(filename))
    my_dict = {}
    for line in entries:
        words = flip_text(line).split(', ')
        my_values = []
        for i in range(1, len(words)):
            my_values.append(words[i])
        my_dict[words[0]] = my_values
    return my_dict

