#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import modules#
import modsDE_parser
import pandas as pd
import sys
from datetime import datetime
import os

#read in command line arguments#
board_id = sys.argv[1]

if len(sys.argv) > 2 and isinstance(int(sys.argv[2]), int):
    max_len = int(sys.argv[2])
else:
    max_len = None
#read in command line arguments#    
    
#collect all threads inside board#
threads = modsDE_parser._get_threads(board_id, max_len)

#create lists for data#
user_list = []
datetime_list = []
current_page_list = []
quoted_user_list = []
post_text_list = []
thread_list = []

#walk through threads and collect data#
i = 1
try:
    
    for thread in threads:
        print("Parsing Thread #"+str(i)+"of "+str(len(threads)))
        i += 1
        pages = modsDE_parser._get_thread_pages(thread)
        for page in pages:
            temp_data = modsDE_parser._get_posts(page)
            for x in temp_data[0]: user_list.append(x)
            for x in temp_data[1]: datetime_list.append(x)
            for x in temp_data[2]: quoted_user_list.append(x)
            for x in temp_data[3]: post_text_list.append(x)
            for x in temp_data[4]: current_page_list.append(x)
            for x in [thread]*len(temp_data[0]): thread_list.append(x)
        
except Exception:
    print("Error while handling Thread "+thread+". Will skip this Thread.")
    i += 1

            
#arrange final data#
master_data = pd.DataFrame({
        "Thread":thread_list,
        "User":user_list,
        "PostTime":datetime_list,
        "QuotedUser":quoted_user_list,
        "PostText":post_text_list
        })
    
master_data["Board"] = board_id

#export data#
now = datetime.now().strftime("%Y-%m-%d_%H%M%S")

if not os.path.isdir(os.path.join(os.getcwd(),"Results")):
    os.makedirs(os.path.join(os.getcwd(),"Results"))

write_path = os.path.join(os.getcwd(),"Results", "boardid"+
                          str(board_id)+"_"+now+".csv")
master_data.to_csv(write_path, sep = ";", index = False, encoding = "utf-8")
