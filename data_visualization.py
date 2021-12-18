import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

directories = ['After_Pendamic_Regular_User', 'Before_Pendamic_Regular_User']


def draw_pie_chart(directory, file_name):

    file_path = directory + "/" + file_name
    try:
        xls = pd.ExcelFile(file_path)
        num_bins = 3
        for i in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=i)
            x = []
            y = []
            d = df.groupby("user_count")
            for k in d:
                x.append(k[0])
                y.append(len(k[1]))

            # x = ['Nuclear', 'Hydro', 'Gas', 'Oil', 'Coal', 'Biofuel']
            # energy = [5, 6, 15, 22, 24, 8]
            # variance = [1, 2, 7, 4, 2, 3]

            x_pos = [i for i, _ in enumerate(x)]

            plt.barh(x_pos, y, color='green')
            plt.ylabel("Commenter")
            plt.xlabel("Total Commented")
            plt.title(i)

            plt.yticks(x_pos, x)
            plt.savefig(directory + "/poster_graphics/" + i + ".pdf")
            plt.show()
            # n, bins, patches = plt.hist(y, num_bins, facecolor='blue', alpha=0.5)
            # plt.title(i)
            # plt.show()

            # plt.pie(y, labels=x, labeldistance=1.20)
            # plt.title(i)
            # plt.legend()
            # plt.savefig(directory+"/comment_graphics/"+i+".pdf")
            # plt.show()
    except FileNotFoundError as err:
        print(err)
    except Exception as err:
        print(err)


# df = pd.read_excel("Before_Pendamic_Regular_User/user_count_post_wise.xlsx")
# df = pd.read_excel("Before_Pendamic_Regular_User/user_count_post_wise.xlsx",xls.sheet_names[1])
# print(df.head())
#
# x = []
# y = []
# total = []
# d = df.groupby("user_count")
# for i in d:
#     x.append(i[0])
#     y.append(len(i[1]))
#
# print(x,y)
#
# explode = np.zeros(len(x))
# explode[0] = 0.1
# print(explode)
# plt.pie(len(x))

# fig1, ax1 = plt.subplots()
# ax1.pie(y, explode=explode, labels=x, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#
# plt.show()
# plt.pie(y, labels=x, labeldistance=1.20)
# plt.legend()
# plt.show()

for d in directories:
    draw_pie_chart(d,"user_count_post_wise.xlsx")
