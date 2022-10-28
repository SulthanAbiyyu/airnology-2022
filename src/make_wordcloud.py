import matplotlib.pyplot as plt
from wordcloud import WordCloud

import warnings
warnings.filterwarnings('ignore')


def make_wordcloud(s: str):
    fig, ax = plt.subplots(figsize=(10, 10))
    wordcloud = WordCloud(background_color="white").generate(s)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

    return fig
