import glob
import nltk
import pandas as pd
import os
import string
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.stem.snowball import GermanStemmer

directories = ['After_Pendamic_Admin_User' , 'After_Pendamic_Regular_User', 'Before_Pendamic_Admin_User','Before_Pendamic_Regular_User']

post = []
post_comment_data = []
post_comment_data_lower_case = []
post_comment_data_token = []
post_comment_data_remove_stop_words = []
complete_data = {
    'raw_data': [],
    'lower_case': [],
    'token_sents': [],
    'token_words': [],
    'remove_stop_words': [],
    'stem_words': [],
    'lemm_words': []
}


def remove_punctuation(text):
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    punctuation_free = "".join([i for i in text if i not in string.punctuation])
    return punctuation_free


def read_file(file):
    try:
        data = pd.read_csv(file)
    except FileNotFoundError as err:
        print(err)
    except Exception as err:
        print(err)
    data.fillna("", inplace=True)
    x, y = data.shape

    for i in range(0, x):
        temp_data = []
        # for j in range(3, y, 4):
        length = len(data.iloc[i][str(3)])
        if length > 0:
            raw_data = data.iloc[i][str(3)]
            post.append(raw_data)

            # remove_punc_data = remove_punctuation(data.iloc[i][str(j)])
            # temp_data.append(remove_punc_data)
        # else:
        #         break
        # post_comment_data.append(temp_data)


#

#
# for i in range(len(post_comment_data)):
#     temp_data = []
#     for j in range(len(post_comment_data[i])):
#         temp_data.append(0)
#     post_comment_data_token.append(temp_data)
# # post_comment_data_token = [0 for i in range(len(post_comment_data) for j in range(len(post_comment_data[i])))]
# # print(post_comment_data_token)
#
#
# # def word_tokenize(text):
# #     return word_tokenize(text)
#
#
# lower_case()
#
# for i in range(0, len(post_comment_data)):
#     for j in range(0, len(post_comment_data[i])):
#         post_comment_data_token[i][j] = word_tokenize(post_comment_data[i][j])
#
#
def remove_stop_words(text):
    stop_words = stopwords.words('english')
    stop_words.append(["i've", 'ive', "they've"])
    output_text = [i for i in text if i not in stop_words]
    return output_text


#
#
# for i in range(0, len(post_comment_data_token)):
#     temp_data = []
#     for j in range(0, len(post_comment_data_token[i])):
#         d = remove_stop_words(post_comment_data_token[i][j])
#         temp_data.append(d)
#     post_comment_data_remove_stop_words.append(temp_data)


# print(post_comment_data_remove_stop_words)


def get_raw_data():
    for directory in directories:
        try:
            files = glob.glob(os.path.normpath(directory + "/clean_data/*.xlsx"))
            for file in files:
                xl_file_name = file.split("\\")[2]
                xl_file_name = xl_file_name[0:xl_file_name.index(".")] + ".xlsx"
                # print(xl_file_name)
                # writer = pd.ExcelWriter(directory + "/clean_data/" + xl_file_name, engine='xlsxwriter')
                d = pd.read_excel(file, sheet_name="raw_data")
                d.fillna("", inplace=True)
                # print(d.head())
                x, y = d.shape
                for i in range(0, x):
                    temp_data = []
                    for j in range(0, y):
                        text_data = d.iloc[i][j]
                        length = len(text_data)
                        if length > 0:
                            temp_data.append(text_data.lower())
                        else:
                            break
                post_comment_data_lower_case.append(temp_data)
                print(post_comment_data_lower_case)
                df = pd.DataFrame(post_comment_data_lower_case)
                df.to_excel(file, sheet_name="lower_case_data")
                post_comment_data_lower_case.clear()
        except Exception as err:
            err
        except FileNotFoundError as err:
            print(err)


def get_data_from_directory():
    for directory in directories:
        try:
            files = glob.glob(os.path.join(directory + "/", "*.csv"))
            for file in files:
                xl_file_name = file.split("\\")[1]
                xl_file_name = xl_file_name[0:xl_file_name.index(".")] + ".xlsx"
                writer = pd.ExcelWriter(directory + "/clean_data/" + xl_file_name, engine='xlsxwriter')
                read_file(file)
                for p in post:
                    complete_data['raw_data'].append(p)
                    complete_data['lower_case'].append(p.lower())
                    sents = sent_tokenize(p.lower(), 'english')
                    complete_data['token_sents'].append(sents)
                    words = word_tokenize(p.lower(), "english", preserve_line=False)
                    words = [w for w in words if w.isalnum()]
                    complete_data['token_words'].append(words)
                    re_sp_wd = remove_stop_words(words)
                    complete_data['remove_stop_words'].append(re_sp_wd)
                    wn = nltk.WordNetLemmatizer()
                    lemma = [wn.lemmatize(t) for t in re_sp_wd]
                    complete_data['lemm_words'].append(lemma)
                    prstem = nltk.PorterStemmer()
                    stems = [prstem.stem(t) for t in lemma]
                    complete_data['stem_words'].append(stems)

                df = pd.DataFrame.from_dict(complete_data)
                df.to_excel(writer, sheet_name="post_data", startcol=0, startrow=0, index=True)
                for key in complete_data.keys():
                    complete_data[key].clear()
                post.clear()
                writer.save()


                # df = pd.DataFrame(post_comment_data)
                # df.to_excel(writer, sheet_name="raw_data", startrow=0, startcol=0, index=True)
                # for data in post_comment_data:
                #     temp_data = []
                #     temp_data_token = []
                #     temp_data_token_wsw = []
                #     for d in data:
                #         lower_case_data = d.lower()
                #         temp_data.append(lower_case_data)
                #         sent_tokens = sent_tokenize(lower_case_data)
                #         tokens = word_tokenize(lower_case_data)
                #         with_out_stop_words = remove_stop_words(tokens)
                #         temp_data_token_wsw.append(with_out_stop_words)
                #         temp_data_token.append(tokens)
                #     post_comment_data_lower_case.append(temp_data)
                #     post_comment_data_token.append(temp_data_token)
                #     post_comment_data_remove_stop_words.append(temp_data_token_wsw)
                # df = pd.DataFrame(post_comment_data_lower_case)
                # df.to_excel(writer,sheet_name="lower_case",startrow=0,startcol=0,index=True)
                # df = pd.DataFrame(post_comment_data_token)
                # df.to_excel(writer,sheet_name="tokens",startrow=0,startcol=0,index=True)
                # df = pd.DataFrame(post_comment_data_remove_stop_words)
                # df.to_excel(writer, sheet_name="with_out_stop_words", startrow=0, startcol=0, index=True)
                # post_comment_data_remove_stop_words.clear()
                # post_comment_data_token.clear()
                # post_comment_data_lower_case.clear()
                # post_comment_data.clear()


        except Exception as err:
            print(err)


# if __name__ == "main":
get_data_from_directory()
# get_raw_data()
