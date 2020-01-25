import os

class Globals():
    DATASET_PATH = '/home/alk/aau/datasets'
    # 6 dataset (1 per gateway) w/ 7 spreadsheets (1 per day)
    LOLLAND_PATH_BS_1 = os.path.join(DATASET_PATH, 'Lolland/LRR689')
    LOLLAND_PATH_BS_2 = os.path.join(DATASET_PATH, 'Lolland/LRR68D')
    LOLLAND_PATH_BS_3 = os.path.join(DATASET_PATH, 'Lolland/LRR68F')
    LOLLAND_PATH_BS_4 = os.path.join(DATASET_PATH, 'Lolland/LRR690')
    LOLLAND_PATH_BS_5 = os.path.join(DATASET_PATH, 'Lolland/LRR698')
    LOLLAND_PATH_BS_6 = os.path.join(DATASET_PATH, 'Lolland/LRR69F')
    # 7 sheet spreadsheet
    LOLLAND_EXCEL = 'data.xlsx'
    # time interval for prediction
    TIME_INTERVAL_EST = 0.5