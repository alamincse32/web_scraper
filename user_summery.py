# This file contains the user summery like how users are active to post and comments
import glob

import pandas as pd
import numpy as np
import os
from xlsxwriter import Workbook

directories = ['After_Pendamic_Admin_User', 'After_Pendamic_Regular_User','Before_Pendamic_Admin_User',
               'Before_Pendamic_Regular_User']

user_data_frame = []
user_data_frame_comment = []
comment_user_count = {}


def get_files_from_directory(file_name):
    user_dic = []
    try:

        data = pd.read_csv(file_name)
        row, column = data.shape
        df2 = data.groupby('0')['0'].apply(list).reset_index(name="User_list")
        for user_list in df2["User_list"]:
            user_dic.append(len(list(user_list)))

        df2["user_count"] = user_dic
        user_data_frame.append(df2)

        column = int(column/4)
        for i in range(1,column):
            df_comment = data.groupby(str(i*4))[str(i*4)].apply(list).reset_index(name="comment_user_list")
            for comment_user,comment_user_list in zip(df_comment[str(i*4)],df_comment["comment_user_list"]):
                if comment_user not in comment_user_count:
                    comment_user_count[comment_user] = len(list(comment_user_list))
                else:
                    count = comment_user_count[comment_user]
                    count += len(list(comment_user_list))
                    comment_user_count[comment_user] = count
        comment_data_frame = pd.DataFrame.from_dict(comment_user_count,orient="index",columns=["users_count"])
        comment_data_frame["users"] = comment_user_count.keys()
        user_data_frame_comment.append(comment_data_frame)
        # print(comment_data_frame.head())
        comment_user_count.clear()

    except FileNotFoundError as err:
        print(err)
    except Exception as err:
        print(err)


def open_directory():
    for directory in directories:
        files = glob.glob(os.path.join(directory + "/", "*.csv"))
        writer = pd.ExcelWriter(directory + "/" + "user_count_post_wise.xlsx", engine='xlsxwriter')
        writer_comment = pd.ExcelWriter(directory + "/" + "user_count_comment_wise.xlsx", engine='xlsxwriter')
        for file in files:
            # print(file)
            # print(file[file.index("\\")+1:file.index("-")])
            get_files_from_directory(file)

        for file_name, data in zip(files, user_data_frame):
            sheet_name = file_name[file_name.index("\\") + 1:file_name.index("-")]
            data.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0, index=False)
        writer.save()

        for file_name, data in zip(files, user_data_frame_comment):
            sheet_name = file_name[file_name.index("\\") + 1:file_name.index("-")]
            data.to_excel(writer_comment, sheet_name=sheet_name, startrow=0, startcol=0, index=False)
        writer_comment.save()

        user_data_frame.clear()
        user_data_frame_comment.clear()


if __name__ == '__main__':
    open_directory()
