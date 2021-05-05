import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def tf_idf(my_corpus, compression_rate):
    """Given a corpus, it learns vocabulary and idf
    Args:
        corpus
    Returns:
        Returns document-term matrix.
    """
    tfidf_vectorizer = TfidfVectorizer(use_idf=True, analyzer='word', stop_words='english')
    tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(my_corpus)
    index = tfidf_vectorizer.get_feature_names()
    values = tfidf_vectorizer_vectors[0].T.todense()
    dataframe = pd.DataFrame(values, index=index, columns=['F-WORD']).sort_values('F-WORD', ascending=False)
    n_selected_values: float = (100 - compression_rate) / 100 * dataframe.shape[0]

    return dataframe.head(int(n_selected_values))

def Tf_Idf_sum(corpus):
    """Given a corpus, it learns vocabulary and idf
    Args:
        corpus
    Returns:
        Returns the sum of tf-idf for each paragraph.
    """
    tfIdfVectorizer=TfidfVectorizer(use_idf=True)
    tfIdf = tfIdfVectorizer.fit_transform(corpus)
    
    i=0
    somme = []
    while i < len(corpus):
        df = pd.DataFrame(tfIdf[i].T.todense(), 
        index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
        somme.append(sum(df.iloc[:,0]))
        i += 1
    
    return somme
