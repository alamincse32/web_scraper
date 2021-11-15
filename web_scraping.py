import re
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

post_and_comment_text = []
column_data = []
forum_data = []
BASE_URL = 'https://www.nationaleatingdisorders.org'
HEADER = {'User-Agent': 'Mozilla/5.0'}
START_DATE = datetime.strptime('02/29/2020','%m/%d/%Y')
END_DATE = datetime.strptime('07/01/2018','%m/%d/%Y')


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

def scrape_data(post_link):
    post_data_comment = []
    post_text = ""
    url = BASE_URL + post_link
    get_post_request = Request(url, headers=HEADER)
    post_page = urlopen(get_post_request)

    post_page = BeautifulSoup(post_page, 'lxml')
    # post_number = post_link.split('/')
    post_container = post_page.find('div', {'about':  post_link})#'post-' + post_number[len(post_number) - 1]})

    if post_container is not None:
        post_date = post_container.find('div', {'class': 'forum-posted-on'})
        date = str(post_date.text).split(" ")[1]
        post_title = str(post_container.find('div', {'class': 'forum-post-title'}).text).replace(" ", "").replace("\n",
                                                                                                               "")
        print(datetime.strptime(date,'%m/%d/%Y'))
        if END_DATE <= datetime.strptime(date,'%m/%d/%Y') <= START_DATE:
            post_data_comment.append(date)
            if len(post_title) > 0:
                post_data_comment.append(post_title)
            post_author = post_container.find('div',{'class' : 'author-pane'})
            author_name = post_author.find('span',{'class' : 'username'}).text
            if len(author_name) > 0:
                post_data_comment.append(author_name)
            posts = post_container.find('div', {'class': 'forum-post-content'}).findAll('p')

            for post in posts:
                post_text = post_text + str(post.text)

            if len(post_text) > 0:
                post_data_comment.append(post_text)

            comment_container = post_page.find('div', {'id': 'forum-comments'})
            if comment_container is not None:
                comments_date_panel = comment_container.findAll('div', {'class':'forum-post-info clearfix'})
                comments_body_panel = comment_container.findAll('div', {'class': 'forum-post-wrapper'})

                for i in range(len(comments_date_panel)):
                    date_panel = comments_date_panel[i].find('div',{'class' : 'forum-posted-on'})
                    date = str(date_panel.text).replace("\n","").replace(" ","")
                    user_name_spane = comments_body_panel[i].find('span',{'class' : 'username'})
                    user_name = str(user_name_spane.text)
                    comment_data = ""
                    for p in comments_body_panel[i].findAll('p'):
                        comment_data += str(p.text)
                    post_data_comment.append(user_name)
                    post_data_comment.append(date)
                    post_data_comment.append(comment_data)
                # print(len(comments_date_panel) == len(comments_body_panel))
                # for comment in comment_container.findAll('div', {'class': ['forum-post-info clearfix','forum-post-wrapper']}):
                #     comment_date_panel = comment_container.find('div',{'class' : 'forum-posted-on'})
                #     comment_date = str(comment_date_panel.text).replace("\n","").replace(" ","")
                #     if len(comment_date) > 0:
                #         post_data_comment.append(comment_date)
                #     comment_author_panel = comment_container.find('span',{'class' : 'username'})
                #     comment_author_name = str(comment_author_panel.text)
                #     if len(comment_author_name) > 0:
                #         post_data_comment.append(comment_author_name)
                #     comment_data = ""
                #     for p in comment.findAll('p'):
                #         comment_data += str(p.text)
                #     if len(comment_data) > 0:
                #         post_data_comment.append(comment_data)
            # else:
            #     print("The date limit has been crossed")
            #     print(len(post_data_comment))
        print(post_data_comment)
    return post_data_comment


def next_page(link):
    get_request = Request(BASE_URL + link, headers=HEADER)
    forum_page = urlopen(get_request).read()
    soup = BeautifulSoup(forum_page, 'lxml')
    table_body = soup.find('tbody')
    ret_variable = True
    for row in table_body.findAll('tr'):
        post_link = row.find('a')['href']
        data = scrape_data(post_link)
        if len(data) > 0:
            post_and_comment_text.append(data)
        else:
            # print(post_link)
            ret_variable = False
            # break
    # return ret_variable


def load_forum_next_page(next_link):
    link = next_link.split("=")
    page_count = int(link[len(link) - 1])
    for i in range(1, page_count + 1):
        print("Page number: " + str(i))
        next_page(link[0] + "=" + str(i))
        # if not get_ret:
        #     break


def load_forum(forum_link):
    get_request = Request(BASE_URL + forum_link, headers=HEADER)
    forum_page = urlopen(get_request).read()
    soup = BeautifulSoup(forum_page, 'lxml')
    item_list = soup.find('ul', {'class': 'pager'})
    if item_list is None:
        return
    else:
        item = item_list.find('a', {'title': 'Go to last page'})
        link = str(item['href'])
        table_body = soup.find('tbody')
        for row in table_body.findAll('tr'):
            post_link = row.find('a')['href']
            data = scrape_data(post_link)
            if len(data) > 0:
                post_and_comment_text.append(data)
        load_forum_next_page(link)
        if len(post_and_comment_text) > 0:
            data_frame = pd.DataFrame(post_and_comment_text)
            file_name = str(forum_link).split("/")
            file_name = file_name[len(file_name) - 1]
            print(file_name)
            data_frame.to_csv("Before_Pendamic/" + file_name + ".csv")
            post_and_comment_text.clear()
        else:
            print("There is no data in this forum. Thanks for trying to scrape data from this site\n")


def create_url_for_next_page(url):
    get_request = Request(url, headers=HEADER)
    web_page = urlopen(get_request).read()
    soup = BeautifulSoup(web_page, 'lxml')

    forum_table = soup.find('div', {"id": "forum"})
    forum_body = forum_table.find('tbody', {"id": "forum-table-263-content"})
    for row in forum_body.findAll("tr"):
        forum_name = row.find('a').text
        forum_link = row.find('a')['href']
        forum_topic_number = str(row.find('div', {"class": "forum-number-topics"}).text).replace(" ", "").replace("\n",
                                                                                                                  "")
        forum_post_number = str(row.find('td', {"class": "forum-number-posts"}).text).replace(" ", "").replace("\n", "")
        forum_data.append([forum_name, forum_link, forum_topic_number, forum_post_number])
        load_forum(forum_link)
    forum_data_frame = pd.DataFrame(forum_data,
                                    columns=['Forum Name', 'Forum Link', 'Forum Topic Number', 'Forum Post Numer'])
    forum_data_frame.to_csv('forum_data_frame.csv')


if __name__ == '__main__':
    # scrape_data('/forum/35214')
    create_url_for_next_page(BASE_URL + "/forum")

