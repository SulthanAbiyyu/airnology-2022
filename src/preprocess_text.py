import argparse
import warnings
import logging
import pandas as pd
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)


def clean_text(data: pd.DataFrame) -> pd.DataFrame:
    def remove_trailing_char(st):
        s_arr = st.split(" ")
        hasil = []
        for s in s_arr:
            unique_char = set(s)
            for char in unique_char:
                if s.count(char) > 2:
                    s = s.replace(char*s.count(char), char)
            hasil.append(s)

        return " ".join(hasil)

    stemmer = StemmerFactory().create_stemmer()
    stopword = StopWordRemoverFactory().create_stop_word_remover()

    logging.info("removing null..")
    data = data.dropna()
    logging.info("lowercasing..")
    data["komentar"] = data["komentar"].str.lower()
    logging.info("removing google translate..")
    data["komentar"] = data["komentar"].apply(
        lambda x: x.replace("(diterjemahkan oleh google)", ""))
    logging.info("removing newline..")
    data["komentar"] = data["komentar"].apply(lambda x: x.replace("\n", " "))
    logging.info("removing punctuation..")
    data["komentar"] = data["komentar"].str.replace('[^\w\s]', ' ')
    data["komentar"] = data["komentar"].str.replace('²', ' ')
    logging.info("stripping..")
    data["komentar"] = data["komentar"].apply(lambda x: x.strip())
    logging.info("stemming..")
    data["komentar"] = data["komentar"].apply(stemmer.stem)
    logging.info("remove stopword..")
    data["komentar"] = data["komentar"].apply(stopword.remove)
    logging.info("removing traling char..")
    data["komentar"] = data["komentar"].apply(
        lambda x: remove_trailing_char(x))

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess text")
    parser.add_argument("--input", type=str, help="Input file path")
    parser.add_argument("--output", type=str, help="Output file path")
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    data = clean_text(data)
    data.to_csv(args.output, index=False)
