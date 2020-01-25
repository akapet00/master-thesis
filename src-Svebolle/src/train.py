import os
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV
from split_clean import load_data, clean, prepare
from sklearn.externals import joblib

def training_done(duration=1, freq=150):
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

def model(data_prepared, data_labels):
    param_grid = [
        {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]}, 
        {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},
    ]
    forest_reg = RandomForestRegressor()
        
    grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
                                scoring='neg_mean_squared_error')
    grid_search.fit(X=data_prepared, y=data_labels)

    training_done()
    
    joblib.dump(grid_search, 'Svebolle-model.pkl')

    return grid_search

def main():
    DATASET_PATH = '/home/alk/aau/datasets'
    SVEBOLLE_PATH = os.path.join(DATASET_PATH, 'Svebolle')
    SVEBOLLE_CSV = 'LORA_data.csv'

    df = load_data(SVEBOLLE_PATH, SVEBOLLE_CSV, sep=';')
    df_clean = clean(df)
    data_prepared, data_labels = prepare(df_clean)

    grid_search = model(data_prepared, data_labels)
    print('Best parameters:', grid_search.best_params_)
    print('Best estimators:', grid_search.best_estimator_)
    cvres = grid_search.cv_results_
    for mean_score, params in zip(cvres['mean_test_score'], cvres['params']):
        print(np.sqrt(-mean_score), params)

if __name__=='__main__':
    main()