import pandas as pd
import pandas as ps
import spacy
import numpy as np
import os

directories = ['After_Pendamic_Admin_User', 'After_Pendamic_Regular_User', 'Before_Pendamic_Admin_User',
               'Before_Pendamic_Regular_User']


def read_file_content(file_name):
    try:
        data_frame = pd.read_csv(file_name)
        row,col = data_frame.shape
        for i in range(row):
            print(data_frame.iloc[i])
    except FileNotFoundError as e:
        print(e)


def open_directory():
    for directory in directories:
        for dir_, _, files in os.walk(directory + '/'):
            for file in files:
                print(file)
                read_file_content(dir_+file)


if __name__ == '__main__':
    open_directory()
