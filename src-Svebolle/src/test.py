import os
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from split_clean import load_data, clean, split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import StratifiedShuffleSplit

def main():
    df = pd.read_csv('test.csv')
    
    X_test = df.drop(['RSSI', 'Unnamed: 0'], axis=1)
    y_test = df['RSSI'].copy()

    print(X_test.columns)
    print(y_test)


    # cleaning missing values of numerical attributes in trainng dataset
    categorical_vals = ["Time", "DevAddr", "mType", "macPayload", "_id"]
    data_num = X_test.drop(categorical_vals, axis=1)

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

    X_test_prepared = full_pipeline.fit_transform(X_test)
    print(X_test_prepared.shape)
    grid_search = joblib.load('Svebolle-model.pkl')
    model = grid_search.best_estimator_

    predictions = model.predict(X_test_prepared)

    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)

    r2 = r2_score(y_test, predictions)

    print('rmse', rmse)
    print('r2', r2)

if __name__=='__main__':
    main()