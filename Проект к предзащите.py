
import  re
import random
import  pymorphy2


def read_text(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
    return text


def delete_variations(text):
    pattern = '/.+?[,.]'
    return re.sub(pattern, ',', text)

def simplify_charachters(text):
    return re.sub('́', '', text).lower()

def delete_markers(text):
    pattern = '[а-яА-ЯёЁ]+?\.'
    return re.sub(pattern, '', re.sub('\.\n', '\n', text))

def delete_punct(text):
    return  re.sub(',', '', text)

def flip_text(filename):
    text = read_text(filename)
    text = delete_markers(simplify_charachters(delete_variations(text)))
    return re.sub('  +', ' ', delete_punct(text))

def create_dict(text):
    entries = text.split('\n')
    entries.remove('') 
    my_dict = {}
    for line in entries:
        words = line.split(' ')
        my_values = []
        for i in range(1, len(words)):
            my_values.append(words[i])
        my_dict[words[0]] = my_values
    return my_dict

def listmerge(lstlst):
    all_items=[]
    for lst in lstlst:
      all_items=all_items+lst
    return all_items

def get_key(d, value):
    for k, v in d.items():
        if value in v:
            return k

def synonym_search(word, synonym_dictionary):
    key_words = list(synonym_dictionary.keys())
    value_lists = list(synonym_dictionary.values())
    value_words = listmerge(value_lists)
    if word in key_words:
        synonyms_values = synonym_dictionary[word]
        needed_value_synonyms = list(synonyms_values)
        smart_synonym = random.choice(needed_value_synonyms)
        return smart_synonym
    elif word in value_words:
        key_needed = get_key(synonym_dictionary, word)
        values_needed = synonym_dictionary[key_needed]
        smarter_synonym = random.choice(values_needed)
        while smarter_synonym == word:
            smarter_synonym = random.choice(values_needed)
        return smarter_synonym 
    else:
        return word

        
def main():
    dict_text = flip_text('Пробный словарь.txt')
    synonym_dictionary = create_dict(dict_text)

    morph = pymorphy2.MorphAnalyzer()

    text = input ('Введите предложение: ')
    words = text.split()

    new_sentence = []

    for word in words:
        if morph.parse(word)[0].tag.POS == 'NOUN':

            word_parse = morph.parse(word)[0]
            word_normal = word_parse.normal_form
            word_tags = {word_parse.tag.number, word_parse.tag.case}

            synonym = synonym_search(word_normal, synonym_dictionary)

            new_word = morph.parse(synonym)[0].inflect(word_tags).word

            new_sentence.append(new_word)
        else:
            new_sentence.append(word)

    print(' '.join(new_sentence))

if __name__ == '__main__':
    main()    
