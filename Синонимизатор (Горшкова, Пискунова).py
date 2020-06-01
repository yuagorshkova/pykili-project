import synonym_dictionary as s
import re
import random
import pymorphy2


def listmerge(lstlst):
    all=[]
    for lst in lstlst:
      all=all+lst
    return all

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
        if (len(values_needed)) == 1:
            return key_needed
        else:
            smarter_synonym = random.choice(values_needed)
            while smarter_synonym == word:
                smarter_synonym = random.choice(values_needed)
            return smarter_synonym
    else:
        return word


def collect_tags(word):
    morph = pymorphy2.MorphAnalyzer()
    word_parse = morph.parse(word)[0]
    if morph.parse(word)[0].tag.POS == 'NOUN':
        return [word_parse.tag.number, word_parse.tag.case]
    elif morph.parse(word)[0].tag.POS == 'ADJF':
        return [word_parse.tag.gender, word_parse.tag.case, word_parse.tag.number]
    elif morph.parse(word)[0].tag.POS == 'VERB':
        return [word_parse.tag.number, word_parse.tag.tense, word_parse.tag.person, word_parse.tag.aspect, word_parse.tag.gender]

        
def main():
    synonym_dictionary = s.create_dict('l.g.babenko-slovar_sinonimov.txt')

    morph = pymorphy2.MorphAnalyzer()

    text = input ('Введите предложение: ')
    words = text.lower().split()

    new_sentence = []

    for word in words:
        if morph.parse(word)[0].tag.POS in ['NOUN', 'ADJF', 'VERB']:
            word_normal = morph.parse(word)[0].normal_form
            word_tags = collect_tags(word)

            synonym = synonym_search(word_normal, synonym_dictionary)
            synonym_parse = morph.parse(synonym)[0]

            for item in word_tags:
                if item:
                    synonym_parse = synonym_parse.inflect({item})
            new_sentence.append(synonym_parse.word)
        elif morph.parse(word)[0].tag.POS == 'ADVB':
            synonym = synonym_search(word, synonym_dictionary)
            new_sentence.append(synonym)
        else:
            new_sentence.append(word)

    print(' '.join(new_sentence))

if __name__ == '__main__':
    main()    
