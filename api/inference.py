import torch
import pandas as pd
import numpy as np
from fastapi import FastAPI
from transformers import AutoTokenizer, BertForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained(
    "./models/indobert-tokenizer-basudara-v1")
model = BertForSequenceClassification.from_pretrained(
    "./models/bcc-basudara-v1", num_labels=5)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/predict")
def predict(data_text: str):
    # encoded_input = tokenizer(data_text, return_tensors='pt')
    # output = model(**encoded_input)
    # pred = torch.nn.functional.softmax(output.logits, dim=-1)
    # hasil = int(np.argmax(pred.detach().numpy()) + 1)
    # return {"pred": hasil}

    df = pd.read_json(data_text)

    hasil = df.iloc[:, 0].apply(lambda x: np.argmax(torch.nn.functional.softmax(model(
        **tokenizer([x], return_tensors='pt')).logits, dim=-1).detach().numpy()) + 1)
    return {"pred": hasil.tolist()}
