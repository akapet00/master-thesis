import pandas as pd
from config import Globals
import os

def load_data_from_xlsx(path, xlsx_file, header=0):
    """Returns data frame of concatenated spreadsheets from loaded xlsx file"""
    xlsx_path = os.path.join(path, xlsx_file)
    df = pd.read_excel(xlsx_path, sheet_name=None, ignore_index=True, header=header)
    df_concat = pd.concat(df.values(), ignore_index=True)
    return df_concat

def get_dataset():
    # data of each basestation during 7 days of measuring
    data_bs_1 = load_data_from_xlsx(Globals.LOLLAND_PATH_BS_1, Globals.LOLLAND_EXCEL, header=1)
    data_bs_2 = load_data_from_xlsx(Globals.LOLLAND_PATH_BS_2, Globals.LOLLAND_EXCEL, header=1)
    data_bs_3 = load_data_from_xlsx(Globals.LOLLAND_PATH_BS_3, Globals.LOLLAND_EXCEL, header=1)
    data_bs_4 = load_data_from_xlsx(Globals.LOLLAND_PATH_BS_4, Globals.LOLLAND_EXCEL, header=1)
    data_bs_5 = load_data_from_xlsx(Globals.LOLLAND_PATH_BS_5, Globals.LOLLAND_EXCEL, header=1)
    data_bs_6 = load_data_from_xlsx(Globals.LOLLAND_PATH_BS_6, Globals.LOLLAND_EXCEL, header=1)

    return data_bs_1.append(data_bs_2, 
        ignore_index=True).append(data_bs_3, 
        ignore_index=True).append(data_bs_4,
        ignore_index=True).append(data_bs_5, 
        ignore_index=True).append(data_bs_6,
        ignore_index=True)

def main():
    bigdata = get_dataset()
    print(bigdata.head(10))

if __name__ == "__main__":
    main()