from pathlib import Path
import nltk
from nltk.corpus import stopwords
from Summarize.utils import read_from_file, parse_nasari_dictionary


def bag_of_word(sent):
    """Auxiliary function for the Lesk algorithm. Transforms the given sentence
    according to the bag of words approach, apply lemmatization, stop words
    and punctuation removal.
    Params:
        sent: sentence
    Returns:
        bag of words
    """

    stop_words = set(stopwords.words('english'))
    punctuation = {',', ';', '(', ')', '{', '}', ':', '?', '!'}
    # Returns the input word unchanged if it cannot be found in WordNet.
    wnl = nltk.WordNetLemmatizer()
    # Return a tokenized copy of text, using NLTK’s recommended word tokenizer (Treebank + PunkSentence)
    tokens = nltk.word_tokenize(sent)
    tokens = list(filter(lambda x: x not in stop_words and x not in punctuation, tokens))
    return set(wnl.lemmatize(t) for t in tokens)


def get_Nasari_vectors(titolo, Nasari_vector):
    """Returns Nasari Vectors (pairs lemma-score) of a sentence in a single list.
    Params:
        title
        Nasari vector
    Returns:
        A dict where the keys are the word in the title and the value are their Nasari vectors
    """
    
    nasari = {}
    bag = list(bag_of_word(titolo))
    print(bag)
    
    for word in bag:
        if word in str(Nasari_vector.keys()).lower():
            #print(word)
            vettore = Nasari_vector[str(word)]
            #print(vettore)
            #nasari.append(vettore)
            nasari.update({word:vettore})
     
    return nasari


if __name__ == "__main__":
    nasari_path = Path('.') / 'datasets' / 'NASARI_vectors' / 'dd-small-nasari-15.txt'

    path = Path('.') / 'datasets' / 'text-documents'
    file_paths = [path / 'Ebola-virus-disease.txt',
                  path / 'Andy-Warhol.txt',
                  path / 'Life-indoors.txt',
                  path / 'Napoleon-wiki.txt',
                  path / 'Trump-wall.txt']

    compression_rate: int = 10
    paragraphs, titles = read_from_file(file_paths[0])

    dict_na = parse_nasari_dictionary(nasari_path)

    print(dict_na.popitem())
    
    contesto = {}

    for title in titles:
        x = get_Nasari_vectors(title, dict_na)
        contesto.update(x)
    
    print(contesto)

