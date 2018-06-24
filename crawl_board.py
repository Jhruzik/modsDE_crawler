#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import modules#
import modsDE_parser
import pandas as pd
import sys
from datetime import datetime
import os
import re

#read in current time#
now = datetime.now().strftime("%Y-%m-%d_%H%M%S")

#read in command line arguments#
sys_args_col = " ".join(sys.argv)

board_id = re.search("(?<=--board_id=)\d+", sys_args_col).group()
max_len = re.search("(?<=--max_len=)\d+", sys_args_col)
incremental = re.search("--incremental", sys_args_col)

if max_len is not None:
    max_len = max_len.group()
    
if incremental is not None:
    incremental = True
else:
    incremental = False
    
#collect all threads inside board#
threads = modsDE_parser._get_threads(board_id, max_len)

#create lists for data#
user_list = []
datetime_list = []
current_page_list = []
quoted_user_list = []
post_text_list = []
thread_list = []

#create temporary folder for incremental crawl
if incremental:
    incremental_resultpath = os.path.join(os.getcwd(),"Results", 
                                          "boardid"+str(board_id)+"_"+
                                          now+"_incremental")
    
    if not os.path.isdir(incremental_resultpath):
        os.makedirs(incremental_resultpath)

#walk through threads and collect data#
i = 1
try:
    
    for thread in threads:
        print("Parsing Thread #"+str(i)+"of "+str(len(threads)))
        i += 1
        pages = modsDE_parser._get_thread_pages(thread)
        
        if incremental == False:
            for page in pages:
                temp_data = modsDE_parser._get_posts(page)
                for x in temp_data[0]: user_list.append(x)
                for x in temp_data[1]: datetime_list.append(x)
                for x in temp_data[2]: quoted_user_list.append(x)
                for x in temp_data[3]: post_text_list.append(x)
                for x in temp_data[4]: current_page_list.append(x)
                for x in [thread]*len(temp_data[0]): thread_list.append(x)
        
        else:
            incremental_csv_path = os.path.join(incremental_resultpath,
                                                "Thread"+str(i)+".csv")
            incr_data = pd.DataFrame()
            for page in pages:
                temp_data = modsDE_parser._get_posts(page)
                user_list = temp_data[0]
                datetime_list = temp_data[1]
                quoted_user_list = temp_data[2]
                post_text_list = temp_data[3]
                thread_list = [thread]*len(temp_data[0])
                temp_data = pd.DataFrame({"Thread":thread_list,
                                          "User":user_list,
                                          "PostTime":datetime_list,
                                          "QuotedUser":quoted_user_list,
                                          "PostText":post_text_list})
            incr_data = incr_data.append(temp_data)
            incr_data["Board"] = board_id
            incr_data.to_csv(incremental_csv_path, 
                             sep = ";", index = False, encoding = "utf-8")

        
except Exception:
    print("Error while handling Thread "+thread+". Will skip this Thread.")
    i += 1

            
#Export final data if not incremental#
if incremental == False:
    
    master_data = pd.DataFrame({
            "Thread":thread_list,
            "User":user_list,
            "PostTime":datetime_list,
            "QuotedUser":quoted_user_list,
            "PostText":post_text_list})
    
    master_data["Board"] = board_id
    
    if not os.path.isdir(os.path.join(os.getcwd(),"Results")):
        os.makedirs(os.path.join(os.getcwd(),"Results"))
        
    write_path = os.path.join(os.getcwd(),"Results", "boardid"+
                              str(board_id)+"_"+now+".csv")
    
    master_data.to_csv(write_path, sep = ";", index = False, encoding = "utf-8")
