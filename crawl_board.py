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

#create temporary and final DataFrame#
temp_data = pd.DataFrame()
master_data = pd.DataFrame()

#walk through threads and collect data#
i = 1
for thread in threads:
    print("Parsing Thread #"+str(i)+"of "+str(len(threads)))
    i += 1
    pages = modsDE_parser._get_thread_pages(thread)
    for page in pages:
        temp_data = modsDE_parser._get_posts(page)
        temp_data["thread"] = thread
        temp_data["board"] = board_id
        master_data = master_data.append(temp_data)
        master_data.reset_index()
        
#arrange final data#
master_data = master_data[["board",
                           "thread",
                           "page",
                           "user",
                           "post_time",
                           "quoted",
                           "text"]]

#export data#
now = datetime.now().strftime("%Y-%m-%d_%H%M%S")

if not os.path.isdir(os.path.join(os.getcwd(),"Results")):
    os.makedirs(os.path.join(os.getcwd(),"Results"))

write_path = os.path.join(os.getcwd(),"Results", "boardid"+
                          str(board_id)+"_"+now+".csv")
master_data.to_csv(write_path, sep = ";", index = False, encoding = "utf-8")
