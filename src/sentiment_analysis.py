import torch
import logging
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, BertForSequenceClassification

logging.basicConfig(level=logging.INFO)
logging.info('Loading model...')
model = BertForSequenceClassification.from_pretrained(
    r"D:\TIF UB\2. Lomba\2022\AIRNOLOGY - 2022\src\bcc-basudara-v1", num_labels=5
)
logging.info('Loading tokenizer...')
tokenizer = AutoTokenizer.from_pretrained(
    r"D:\TIF UB\2. Lomba\2022\AIRNOLOGY - 2022\src\indobert-tokenizer-basudara-v1")


def predict_sentiment(data: pd.DataFrame, text_col: str) -> pd.DataFrame:
    logging.info("Removing null values...")
    logging.info('Predicting sentiment...')
    data[f"{text_col}_sentiment"] = data[text_col].apply(lambda x: np.argmax(torch.nn.functional.softmax(
        model(**tokenizer([x], return_tensors='pt')).logits, dim=-1).detach().numpy()) + 1)
    return data
