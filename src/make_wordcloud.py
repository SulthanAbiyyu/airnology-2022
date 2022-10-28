import matplotlib.pyplot as plt
from wordcloud import WordCloud

import warnings
warnings.filterwarnings('ignore')


def make_wordcloud(s: str, output_path: str):
    wordcloud = WordCloud(background_color="white").generate(s)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
