#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import modules#
from pandas import DataFrame
from bs4 import BeautifulSoup
import requests
import re

######Functions for Data Extraction (internal)######

#helper functions#
def _get_page(url):
    page = requests.get(url)
    page = BeautifulSoup(page.text, "lxml")
    return page
    
def _find_last_page(first_page, max_len = None):
    if first_page.find("a", string = "letzte »") is not None:
        last_page_num = first_page.find("a", string = "letzte »")["href"]
        last_page_num = int(re.search("\d+$", last_page_num).group())
    else:
        temp_page_list = first_page.find_all("a", string = re.compile("^\d+$"))
        temp_page_list = [page for page in temp_page_list if page["href"].startswith("thread")]
        if len(temp_page_list) > 0:
            last_page_num = max([int(x.get_text()) for x in temp_page_list])
        else:
            last_page_num = 1
    if isinstance(max_len, int) and max_len < last_page_num:
        last_page_num = max_len
    return last_page_num


#parse board#
def _get_threads(board_id, max_len = None):
    url = "http://forum.mods.de/bb/board.php?BID="+str(board_id)
    first_page = _get_page(url)
    last_page_num = _find_last_page(first_page, max_len)

    #get all threads on all pages#
    page_link_list = [url+"&page="+str(i) for i in range(1, last_page_num+1)]
    thread_link_list = []
    for link in page_link_list:
        temp_page = requests.get(link)
        temp_page = BeautifulSoup(temp_page.text, "lxml")
        temp_link_list = temp_page.find_all("tr", {"bgcolor":"#222E3A"})
        temp_link_list = [thread.find("a")["href"] for thread in temp_link_list]
        for link in temp_link_list:
            thread_link_list.append("http://forum.mods.de/bb/"+link)
    thread_link_list = list(set(thread_link_list))#delete duplicates
    
    return thread_link_list
    

#parse threads#
def _get_thread_pages(thread_link):
    first_page = _get_page(thread_link)
    last_page_num = _find_last_page(first_page)
    
    #get all page links#
    page_link_list = [thread_link+"&page="+str(i) for i in range(1, last_page_num+1)]
    
    return page_link_list

#parse posts#
def _get_posts(page_link):
    page = _get_page(page_link)
    if page.find("b", string = re.compile("\[\d+\]")) is not None:
        current_page_num = page.find("b", string = re.compile("\[\d+\]")).get_text()
        current_page_num = re.search("\d+", current_page_num).group()
    else:
        current_page_num = 1
    
    #get all posts
    posts = page.find_all("tr", {"username": True})
    
    #get original posters
    user_list = []
    for post in posts:
        user = post.find("a", {"onclick":re.compile("openProfile.*")})
        user_list.append(user.get_text())
    
    #get post date#
    dates = page.find_all("a", {"class": "nu wht postlink"})
    datetime_list = [date.get_text().strip() for date in dates]
    
    #get quoted users
    quoted_user_list = []
    for post in posts:
        if post.find("td", {"class": "quote"}) is not None:
            try:
                quote_text = post.find("td", {"class": "quote"}).get_text()
                quoted_user = re.search("Zitat von (.*)\n", quote_text).group(1)
                quoted_user_list.append(quoted_user.strip())
            except Exception:
                quoted_user_list.append(None)
        else:
            quoted_user_list.append(None)
    
    #get list of original post text#
    post_text_list_temp = [post.find("span", {"class":"posttext"}) for post in posts]
    post_text_list = []
    for post in post_text_list_temp:
        if post.table is not None:
            post.table.decompose()
        post_text_list.append(post.get_text())
    
    #merge data into one data frame
    page_df = DataFrame({"user":user_list,
                         "post_time":datetime_list,
                         "page":current_page_num,
                         "quoted":quoted_user_list,
                         "text":post_text_list})
    
    return page_df