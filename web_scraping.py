import re
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
import pandas as pd

column_data = []
forum_data = []
BASE_URL = 'https://www.nationaleatingdisorders.org'
HEADER = {'User-Agent': 'Mozilla/5.0'}
# get_request = Request(BASE_URL,headers=header)
# web_page = urlopen(get_request).read()
#
# soup = BeautifulSoup(web_page,'lxml')
# view = soup.find('div', {"id" : "forum"})
# header_ = view.find('thead', class_ = "forum-header")
# data.append([header_.find("th",class_ = "forum-name").text,"Link",header_.find("th",class_ = "forum-topics").text,header_.find("th",class_ = "forum-posts").text,header_.find("th",class_ = "forum-last-post").text ])
# body_ = view.find('tbody', {"id" : "forum-table-263-content"})
# for row in body_.findAll('tr'):
#     print(row)
# forum_link = 'https://www.nationaleatingdisorders.org'
# for row in view.findAll('tr'):
#     columns = row.findAll('td')
#     if len(columns) > 0:
#         link = columns[1].find('a')['href']
#         link = forum_link+link
#         print(link)
#         inner_request = Request(link,headers=header)
#         post_page = urlopen(inner_request).read()
#         post_soup = BeautifulSoup(post_page,'lxml')
#         post = post_soup.find('div',class_ = 'field-item even')
#         print(post.text)
#         data.append(post.text)
#         column_data.append(link)
#         # column_cell = columns.find('a')
#         # print(column_cell)
#
# data_frame = pd.DataFrame(data)
# data_frame.to_csv('post_data.csv',index=True,header=['post'])
# print(data_frame)
def load_forum(forum_link):
    get_request = Request(BASE_URL+forum_link,headers=HEADER)
    forum_page = urlopen(get_request).read()
    soup = BeautifulSoup(forum_page, 'lxml')
    next_url = None
    cur_page = soup.find('a', {'class': 'active'}, href=re.compile('/forums/covid-19'))

    print(soup)






def create_url_for_next_page(url):
    get_request = Request(url, headers=HEADER)
    web_page = urlopen(get_request).read()
    soup = BeautifulSoup(web_page, 'lxml')

    forum_table = soup.find('div',{"id" : "forum"})
    forum_body = forum_table.find('tbody',{"id" : "forum-table-263-content"})
    for row in forum_body.findAll("tr"):
        forum_name = row.find('a').text
        forum_link = row.find('a')['href']
        forum_topic_number = str(row.find('div',{"class" : "forum-number-topics"}).text).replace(" ","").replace("\n","")
        forum_post_number = str(row.find('td', {"class" : "forum-number-posts"}).text).replace(" ","").replace("\n","")
        forum_data.append([forum_name,forum_link,forum_topic_number,forum_post_number])
        load_forum(forum_link)
    forum_data_frame = pd.DataFrame(forum_data, columns=['Forum Name','Forum Link','Forum Topic Number','Forum Post Numer'])

    forum_data_frame.to_csv('forum_data_frame.csv')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_url_for_next_page(BASE_URL+"/forum")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
