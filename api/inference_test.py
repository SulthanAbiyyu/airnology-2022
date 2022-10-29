import requests
import pandas as pd

base_url = "http://127.0.0.1:8000/"

data = pd.read_csv(
    "../data/google_review_wisata_jabar/data_review_validated.csv")
data = pd.DataFrame(data["text"])
data = data.to_json()

# print(data)

# print(pd.read_json(data).iloc[:, 0])

r = requests.post("http://127.0.0.1:8000/predict?data_text=" + data)
print(r.text)
