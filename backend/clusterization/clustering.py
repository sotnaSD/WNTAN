from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from itertools import compress
import pickle

from pre_processing import Preprocesser

class Custom_KMeans():
    """"
            Custom KMeans model. It looks for an optimum K value automatically
            params:
                data: list of numeric vectors.
    """

    def __init__(self, data_encoded: []):
        print('Clusterization process started.')
        self.data_encoded = data_encoded
        self.optimum_k = None
        self.Y = None

    def fit_predict(self):
        print('  Fitting the model...')
        self._get_optimum_K()
        km = KMeans(n_clusters=self.optimum_k, random_state=1000)  # It uses by default KMeans ++
        self.Y = km.fit_predict(self.data_encoded)

    def _get_optimum_K(self, init=2, end=20):
        print('  Finding optimum value for K...')
        inercias = np.zeros(shape=(end - init + 1,))
        for i in range(init, end + 1):
            km = KMeans(n_clusters=i, random_state=1000)  # It uses by default KMeans ++
            km.fit(self.data_encoded)
            inercias[i - init] = km.inertia_

        # get the differences between i and i - 1
        diff = [inercias[i - 1] - inercias[i] for i in range(1, len(inercias))]
        # I need the + 3 because KMeans stats at 2 clusters, and the [0] takes the main result
        optimum_k = [diff.index(x) + 3 for x in sorted(diff, reverse=True)][0]

        self.optimum_k = optimum_k

    def generate_visualizations(self, preprocessed_data):
        """"
        Function to plow wordclouds. Takes as input the cleaned data (not the encoded) for
        showing the words
        """
        print('  Generating visualizations...')
        file_names = {}
        for k in range(self.optimum_k):
            cluster_text = ' '.join(doc for doc in list(compress(preprocessed_data, self.Y == k)))


            wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(cluster_text)
            plt.imshow(wordcloud, interpolation='bilinear', aspect='auto')
            plt.axis("off")
            plt.savefig(f"../images/cluster_{k}.png", format="png")

            file_names[str(k)] = f'cluster_{k}.png'



with (open("../data/tweets.p", "rb")) as openfile:
    try:
        tweets = pickle.load(openfile)
    except EOFError:
        print('Error opening tweets.p')

preprocesser = Preprocesser()
clean_data, encoded_data = preprocesser.preprocess_data(tweets['text'])


kmeans_model = Custom_KMeans(encoded_data)
kmeans_model.fit_predict()
kmeans_model.generate_visualizations(clean_data)