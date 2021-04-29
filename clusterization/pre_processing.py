import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import constants


class Preprocesser:
    """"
    This class in in charge of cleaning the data and embed the words
    with tf-idf
    """



    def preprocess_data(self, docs: []):
        print('Data pre-processing started.')
        clean_data = self._clean_data(docs)
        encoded_data = self._vectorize_data(clean_data)
        return clean_data, encoded_data

    def _clean_data(self, docs: []):
        """"
            function not parametric to pre process the data
            params:
                docs: list of strings
        """
        print('Cleaning data...')
        preprocessed_data = []
        for doc in docs:
            if len(doc) <= constants.MIN_DOC_LENGTH:
                continue

            temp_doc = self._remove_urls(doc)
            temp_doc = self._remove_special_chars(temp_doc)
            temp_doc = self._transform_to_lowercase(temp_doc)
            temp_doc = self._remove_stopwords(temp_doc)

            preprocessed_data.append(temp_doc)

        return preprocessed_data

    def _vectorize_data(self, docs: []):
        """"
        Function to encode the data with TF-IDF
        """
        print('Vectorizing data...')
        tfidf = TfidfVectorizer()
        encoded_data = tfidf.fit_transform(docs)
        return encoded_data

    def _remove_special_chars(self, doc: str):
        """
        Function for removing special chars like
        commas, periods, exclamations, ask marks and more
        """
        processed_tweet = re.sub('[\.,!#¡\?¿%:;´"@”“&()\|]', '', doc)
        return processed_tweet

    def _remove_urls(self, doc: str):
        """
        Function for removing urls from tweets
        """
        processed_tweet = re.sub('(https?:)?\/\/[\w\.\/-]+', '', doc)
        return processed_tweet

    def _transform_to_lowercase(self, doc: str):
        """
        Function for converting all chars to lowercase
        """
        processed_tweet = doc.lower()
        return processed_tweet

    def _remove_stopwords(self, doc: str):
        """
        Function for removing stopwords from spanish and unique characters
        """
        processed_tweet = [word for word in doc.split() if
                          word not in stopwords.words('spanish') and
                          len(word) > 1]
        return ' '.join(processed_tweet)
