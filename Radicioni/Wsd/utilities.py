import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn


def lesk(word, sentence):
    """Lesk algorithm implementation. Given a word and a sentence in which it appears,
    it returns the best sense of the word.

    Args:
        word: word to disambiguate
        sentence: sentence to compare
    Returns:
        best sense of word
    """

    # Calculating the synset of the given word inside WN
    word_senses = wn.synsets(word)
    best_sense = word_senses[0]
    max_overlap = 0

    # I choose the bag of words approach
    context = bag_of_word(sentence)

    for sense in word_senses:
        # set of words in the gloss
        signature = bag_of_word(sense.definition())

        # and examples of the given sense
        examples = sense.examples()
        for ex in examples:
            # after this line, signature will contain for all the words, their
            # bag of words definition and their examples
            signature = signature.union(bag_of_word(ex))

        overlap = compute_overlap(signature, context)
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense


def bag_of_word(sent):
    """Auxiliary function for the Lesk algorithm. Transforms the given sentence
    according to the bag of words approach, apply lemmatization, stop words
    and punctuation removal.

    Args:
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


def compute_overlap(signature, context):
    """Auxiliary function for the Lesk algorithm. Computes the number of words in
    common between signature and context.

    Args: 
        signature: bag of words of the signature (e.g. definitions + examples)
        context: bag of words of the context (e.g. sentence)
    Returns:
        number of elements in commons
    """

    return len(signature & context)


def get_sense_index(word, sense):
    """Given a ambiguous word and a sense of that word, it returns the
    corresponding index of the sense in the synsets list associated with the
    word indices starts with 1.

    Args: 
        word: ambiguous word (with more that 1 sense)
        sense: sense of the word
    Returns:
        index of the sense in the synsets list of the word
    """

    senses = wn.synsets(word)
    return senses.index(sense) + 1


def pos_validity(pos, text, word):
    """Auxiliary function for the parse_xml
    Args:
        pos:
        text:
        word: ambiguous word (with more that 1 sense)
    Returns:
        boolean: True if the word is valid and false otherwise
    """
    return pos == 'NN' and '_' not in text and len(wn.synsets(text)) > 1 and 'wnsn' in word.attrib


def max_freq(word):
    """
    Helper method for lesk_demaria
    :param word of interest
    :return: frequency of the word
    """
    synsets = wn.synsets(word)
    sense2freq = None
    freq_max = 0

    for s in synsets:
        freq = 0
        for lemma in s.lemmas():
            freq += lemma.count()
            if freq > freq_max:
                freq_max = freq
                sense2freq = s
    return sense2freq


def lesk_demaria(word, sentence):
    """
    Given a word and a sentence in which it appears, it returns the best sense of the word.
    DeMaria Implementation more precise than simpler lesk above thanks to max_freq
    Args:
        word: word to disambiguate
        sentence: sentence to compare
    Returns:
        best sense of word
    """
    # inizializzazione
    max_overlap = 0
    best_sense = max_freq(word)

    # If I choose the bag of words approach
    context = bag_of_word(sentence)
    signature = []

    for ss in wn.synsets(word):
        signature += ss.definition().split()
        signature += ss.lemma_names()

        overlap = set(signature).intersection(context)
        signature.clear()

        if len(overlap) > max_overlap:
            best_sense = ss
            max_overlap = len(overlap)

    return best_sense
