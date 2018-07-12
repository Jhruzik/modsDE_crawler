#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import os
import re

#read in command line arguments#
sys_args_col = " ".join(sys.argv[1:])
allowed_params = re.compile("(--job_name=\S+|--output_path=\S+)")

if not all([re.search(allowed_params, x) for x in sys.argv[1:]]):
    raise ValueError("One of your arguments is unkown. Please consult the documentation.")
    
job_name = re.search("(?<=--job_name=)\S+", sys_args_col).group()
job_path = os.path.join(os.getcwd(), "Jobs", job_name, "Results/")
output_path = re.search("(?<=--output_path=)\S+", sys_args_col).group()
if not output_path.endswith(".csv"): output_path = output_path+".csv"
#read in command line arguments#

#prepare for population of data frame#
data_master = pd.DataFrame()
thread_list = os.listdir(job_path)
thread_len = str(len(thread_list))
i = 1
#prepare for population of data frame#

#loop through every single csv file#
for thread in thread_list:
    print("Parsing Thread #"+str(i)+" of "+thread_len)
    pages = os.listdir(os.path.join(job_path, thread))
    i += 1
    for page in pages:
        page_path = os.path.join(job_path, thread, page)
        data_tmp = pd.read_csv(page_path, sep = ";", encoding = "utf-8")
        data_master = data_master.append(data_tmp)
#loop through every single csv file#

#export data#        
data_master.to_csv(output_path, sep = ";", encoding = "utf-8", index = False)
#export data#