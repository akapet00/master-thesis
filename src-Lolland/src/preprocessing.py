from getting_the_data import get_dataset
from config import Globals
import pandas as pd
import numpy as np

def preprocessing():
    bigdata = get_dataset()

    # remove all columns with only NaN values
    bigdata = bigdata.dropna(axis=1, how='all')

    # wanted columns
    headers = [
                'Timestamp',
                'Direction', # downlink = 1; uplink = 0
                'DevAddr', # end device identification
                'LRR Id', # base station identification
                'LRR Lat', 'LRR Lon', # base station location
                'LRR RSSI', 'LRR SNR', 'LRR ESP', # strength indicators
                'MIC', 'MType',
                'PayloadSize',
                'AirTime', # ToA - dependign of SPF 
                'ADR',
                'SpFact'
                ]
    bigdata_preprocessed = bigdata[headers]

    # object type columns that should be numeric
    obj_headers = ['Direction', 'MType', 'PayloadSize', 'SpFact', 'ADR']
    
    bigdata_preprocessed.loc[:,'Direction'] = pd.to_numeric(bigdata_preprocessed.Direction, errors='coerce')
    bigdata_preprocessed.loc[:,'MType'] = pd.to_numeric(bigdata_preprocessed.MType, errors='coerce')
    bigdata_preprocessed.loc[:,'PayloadSize'] = pd.to_numeric(bigdata_preprocessed.PayloadSize, errors='coerce')
    bigdata_preprocessed.loc[:,'SpFact'] = pd.to_numeric(bigdata_preprocessed.SpFact, errors='coerce')
    bigdata_preprocessed.loc[:,'ADR'] = pd.to_numeric(bigdata_preprocessed.ADR, errors='coerce')

    # adding BW value
    bigdata_preprocessed.loc[:,'Bandwidth'] = 125

    # dropping all rows that does not specify uplink connection
    bigdata_preprocessed = bigdata_preprocessed.query('Direction == 0')
    bigdata_preprocessed = bigdata_preprocessed.reset_index(drop=True)

    # adding label to whole dataset
    bigdata_preprocessed['SUCCESS'] = np.where(bigdata_preprocessed['AirTime']<Globals.TIME_INTERVAL_EST, 1, 0)
    
    return bigdata_preprocessed

def main():
    bigdata_preprocessed = preprocessing()
    print(bigdata_preprocessed.isnull().any())
    bigdata_preprocessed.to_csv('bigdata_preprocessed.csv')
    
if __name__ == "__main__":
    main()