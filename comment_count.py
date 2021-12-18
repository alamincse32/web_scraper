import pandas as pd
import os

directory_list = ['After_Pendamic_Admin_User']


# 'After_Pendamic_Regular_User', 'Before_Pendamic_Regular_User','Before_Pendamic_Admin_User'
def count_comment_in_post(file_name):
    post_and_comment = pd.read_csv(file_name, index_col=None, header=0)
    print(post_and_comment)


for directory in directory_list:
    for directories, _, files in os.walk(directory + "/"):
        for file in files:
            print(file)
            count_comment_in_post(file)
