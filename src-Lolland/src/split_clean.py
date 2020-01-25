from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

def stratified_split():
    df = pd.read_csv('bigdata_preprocessed.csv')
    # remove all NaN values if there are any
    df = df.dropna(subset=['DevAddr'])
    df = df.reset_index(drop=True)

    # LRR Id to numeric
    df['LRR_Id_encoded'], _ = df['LRR Id'].factorize()

    # stratified split based on number of measurements by each base station
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(df, df.LRR_Id_encoded):
        strat_train_set = df.loc[train_index]
        strat_test_set = df.loc[test_index]
    
    return strat_train_set, strat_test_set

def clean():
    strat_train_set, strat_test_set = stratified_split()
    data = strat_train_set[['MType', 'PayloadSize', 'ADR', 'SpFact', 
                            'Bandwidth', 'LRR_Id_encoded', 'DevAddr']].copy()
    data_labels = strat_train_set['SUCCESS'].copy()

    data_num = data[['MType', 'PayloadSize', 'ADR', 'SpFact', 'Bandwidth']].copy()
    SpFact_ix, Bandwidth_ix = [
        list(data_num.columns).index(col)
        for col in ("SpFact", "Bandwidth")
        ]

    num_attribs = ['MType', 'PayloadSize', 'ADR', 'SpFact', 'Bandwidth']
    cat_attribs = ['LRR_Id_encoded', 'DevAddr']

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('attribs_adder', CombinedAttributesAdder(SpFact_ix, Bandwidth_ix)),
        ('std_scaler', StandardScaler()),
    ])

    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        ("cat", OneHotEncoder(categories='auto'), cat_attribs),
    ])

    data_prepared = full_pipeline.fit_transform(data)
    
    return data_prepared, data_labels

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, SpFact_ix, Bandwidth_ix, code_rate=0.8, add_data_rate=True):
        self.add_data_rate = add_data_rate
        self.code_rate = code_rate
        self.SpFact_ix = SpFact_ix
        self.Bandwidth_ix = Bandwidth_ix
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        data_rate = X[:, self.SpFact_ix] * X[:, self.Bandwidth_ix] * self.code_rate / (np.power(2, X[:, self.SpFact_ix]))
        if self.add_data_rate:
            return np.c_[X, data_rate]
        else:
            return np.c_[self.code_rate]

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values


def main():
    print('--SPLIT--')
    strat_train_set, strat_test_set = stratified_split()
    print('Proportions of train set: ')
    print(strat_train_set['LRR Id'].value_counts() / len(strat_train_set))
    print('Proportions of test set: ')
    print(strat_test_set['LRR Id'].value_counts() / len(strat_test_set))

    print('\n--CLEAN--')
    data_prepared, data_labels = clean()
    print('Data prepared: ')
    print(data_prepared)
    print('Data labels: ')
    print(data_labels)

if __name__ == "__main__":
    main()