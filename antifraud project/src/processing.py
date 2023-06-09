# -*- coding: utf-8 -*-
"""препроцессинг в прод.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WLU93HeyilveINggqx3BxpS5SOW-1XhT
"""

import joblib
import pandas as pd
import numpy as np

from sklearn.preprocessing import RobustScaler


def preprocessing(df):
    rob_scaler = RobustScaler()

    df['scaled_amount'] = rob_scaler.fit_transform(df['Amount'].values.reshape(-1,1))
    df['scaled_time'] = rob_scaler.fit_transform(df['Time'].values.reshape(-1,1))

    df.drop(['Time','Amount'], axis=1, inplace=True)

    scaled_amount = df['scaled_amount']
    scaled_time = df['scaled_time']

    df.drop(['scaled_amount', 'scaled_time'], axis=1, inplace=True)
    df.insert(0, 'scaled_amount', scaled_amount)
    df.insert(1, 'scaled_time', scaled_time)

    return df


def load_models():
    model_Xg = joblib.load("./models/boosting.pkl")
    bagging = joblib.load("./models/bagging.pkl")

    return model_Xg, bagging


def process_fraud(filename, models):
    # check filename
    if filename.endswith('.csv') and filename.count('.') == 1 and filename.count('/') == 0:
        pass
    else:
        return False
    
    model_Xg, bagging = models["model_Xg"], models["bagging"]
    
    df = pd.read_csv("./input/" + filename)

    # Delete next line in production (used for training)
    df.drop('Class', axis=1, inplace=True)

    scaled_df = df.copy()
    scaled_df = preprocessing(scaled_df)

    blending_pred = (model_Xg.predict(scaled_df) + bagging.predict(scaled_df))/2
    
    df['fraud'] = blending_pred
    fraud = df[blending_pred >= 0.5]

    fraud.to_csv("./output/" + filename)

    return True


if __name__ == "__main__":
    try:
        process_fraud("creditcard.csv")
    except Exception as e:
        print(f"e is {e}")