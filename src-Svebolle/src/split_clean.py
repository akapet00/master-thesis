import os
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
import pdb

def load_data(path, csv_file, sep=','):
    "return DataFrame with data from dataset"
    csv_path = os.path.join(path, csv_file)
    return pd.read_csv(csv_path, sep) # sep by default is comma

def clean(df):
    """clean and transform features"""
    # remove all rows with DevAddr = NaN / it cannot be imputed
    df = df.dropna(subset=['DevAddr'])
    df = df.reset_index(drop=True) 

    print(df.isnull().any())    
    # make RSSI numerical value
    df['RSSI'] = [x.replace(',', '.') for x in df.RSSI]
    # missing values will be interpreted as Nan
    df['RSSI'] = pd.to_numeric(df.RSSI, errors='coerce')

    # fix code rate column
    df.rename(columns={' 4/5': 'codeRate'}, inplace=True)
    df['codeRate'] = [x.replace(' ', '') for x in df.codeRate]
    df['codeRate'] = [0.8 for x in df.codeRate if x == '4/5']

    # insted of the JSON calculate actual data rate value
    df.dataRate = df.SPF * df.BW * df.codeRate / (2**df.SPF) * 1000

    # write freq in mHz insted of Hz
    df.Freq = df.Freq / 10**6

    # add macPayloadLen column that contains length (in bits) of MAC Payload
    df['macPayloadLen'] = df.macPayload.str.len() * 4 # times 4 because of HEX

    return df

def split(data):
    """return training set and testing set"""
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2,
                                    random_state=42)
    for train_index, test_index in split.split(data, data['SPF']):
        strat_train_set = data.loc[train_index]
        strat_test_set = data.loc[test_index]

    # proportions of SPF should be the same in training set and original data
    proportions_SPF = strat_test_set['SPF'].value_counts() / len(strat_test_set)
    # print(proportions_SPF)

    return strat_train_set, strat_test_set

def prepare(df):
    # split data on training set and testing set
    strat_train_set, strat_test_set = split(df)
    strat_test_set.to_csv('test.csv')

    data = strat_train_set.drop('RSSI', axis=1)    
    data_labels = strat_train_set['RSSI'].copy()
    
    # cleaning missing values of numerical attributes in trainng dataset
    imputer = SimpleImputer(strategy='median')

    categorical_vals = ["Time", "DevAddr", "mType", "macPayload", "_id"]
    data_num = data.drop(categorical_vals, axis=1)

    imputer.fit(data_num)

    # pipeline
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('std_scaler', StandardScaler()),
        ])

    num_attribs = list(data_num)
    cat_attribs = ['mType']

    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        ("cat", OneHotEncoder(), cat_attribs),
    ])

    data_prepared = full_pipeline.fit_transform(data)

    return data_prepared, data_labels

def main():
    DATASET_PATH = '/home/alk/aau/datasets'
    SVEBOLLE_PATH = os.path.join(DATASET_PATH, 'Svebolle')
    SVEBOLLE_CSV = 'LORA_data.csv'

    df = load_data(SVEBOLLE_PATH, SVEBOLLE_CSV, sep=';')
    df_clean = clean(df)
    data_prepared, data_labels = prepare(df_clean)

    print('data for training:\n', data_prepared)
    print('labels:\n', data_labels)

if __name__ == '__main__':
    main()