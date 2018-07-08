#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import modules#
import modsDE_parser
import pandas as pd
import sys
from datetime import datetime
import os
import re
import threading
from time import sleep

#read in current time#
now = datetime.now().strftime("%Y-%m-%d_%H%M%S")

#read in command line arguements#
sys_args_col = " ".join(sys.argv[1:])
allowed_params = re.compile("(--board_id=\d+|--max_len=\d+|--continue_job=\S+|--spiders=\d+|--pause_breaks=\d+|--pause_duration=\d+)")

if not all([re.search(allowed_params, x) for x in sys.argv[1:]]):
    raise ValueError("One of your arguments is unkown. Please consult the documentation.")


board_id = re.search("(?<=--board_id=)\d+", sys_args_col)
max_len = re.search("(?<=--max_len=)\d+", sys_args_col)
job_old = re.search("(?<=--continue_job=)\S+", sys_args_col)
spiders = re.search("(?<=--spiders=)\d+", sys_args_col)
pause_duration = re.search("(?<=--pause_duration=)\d+", sys_args_col)
pause_breaks = re.search("(?<=--pause_breaks=)\d+", sys_args_col)

if max_len is not None: max_len = max_len.group()
if board_id is not None: board_id = board_id.group()
if job_old is not None: job_old = job_old.group()
if pause_duration is not None: pause_duration = int(pause_duration.group())
if pause_breaks is not None: pause_breaks = int(pause_breaks.group())
if spiders is not None: 
    spiders = int(spiders.group())
else:
    spiders = 1


#create folders for job#
if not os.path.isdir(os.path.join(os.getcwd(),"Jobs")):
    os.makedirs(os.path.join(os.getcwd(),"Jobs"))

if job_old is None:
    job_new = "_".join(["board", str(board_id), now])
    job_path = os.path.join(os.getcwd(),"Jobs", job_new)
    result_path = os.path.join(job_path, "Results")
    log_path = os.path.join(job_path, "Logs")
    os.makedirs(job_path)
    os.makedirs(result_path)
    os.makedirs(log_path)
else:
    job_path = os.path.join(os.getcwd(),"Jobs", job_old)
    result_path = os.path.join(job_path, "Results")
    log_path = os.path.join(job_path, "Logs")
    
    
#collect threads#
if job_old is None:
    threads = modsDE_parser._get_threads(board_id, max_len)
    with open(os.path.join(log_path, "jobs_total.txt"), 
              mode = "w", encoding = "utf-8") as log_total:
        log_total.write('\n'.join(threads))
    total_length = len(threads)
else:
    with open(os.path.join(log_path, "jobs_total.txt"), 
              mode = "r", encoding = "utf-8") as log_total:
        threads_total = [thread.strip() for thread in log_total.readlines()]
    with open(os.path.join(log_path, "jobs_done.txt"), 
              mode = "r", encoding = "utf-8") as threads_done:
        threads_done = [thread.strip() for thread in threads_done.readlines()]
    threads = [thread for thread in threads_total if thread not in threads_done]
    total_length = len(threads_total)


#define crawler#
def crawler(threads):
    
    global total_length
    total_length = str(total_length)
    
    for thread in threads:
        try:
            
            thread_counter = len(os.listdir(result_path))
            print("Crawled: "+str(thread_counter)+" of "+total_length)
            
            if pause_breaks is not None and thread_counter%pause_breaks == 0 and thread_counter > 0:
                print("Timeout pause breakpoint reached. Will pause for "+
                      str(pause_duration)+" seconds.")
                sleep(pause_duration)
                
            pages = modsDE_parser._get_thread_pages(thread)
            thread_id = re.search("\d+$", thread).group()
            os.makedirs(os.path.join(result_path, thread_id), exist_ok = True)
            
            for page in pages:
                page_num = re.search("\d+$", page).group()
                tmp_data = modsDE_parser._get_posts(page)
                
                tmp_user = tmp_data[0]
                tmp_date = tmp_data[1]
                tmp_quoted = tmp_data[2]
                tmp_text = tmp_data[3]
                
                page_data = pd.DataFrame({"User":tmp_user,
                                          "PostTime":tmp_date,
                                          "UserQuoted":tmp_quoted,
                                          "PostText":tmp_text,
                                          "PostSite":page_num,
                                          "Thread":thread_id})
                page_data.to_csv(os.path.join(result_path, thread_id, page_num+".csv"),
                                              sep = ";", encoding = "utf-8", 
                                              index = False)
            
            with open(os.path.join(log_path, "jobs_done.txt"),
                      mode = "a", encoding = "utf-8") as threads_done:
                threads_done.write(thread+"\n")
                
        except Exception:
            pass
        

#init multi-threading#
if spiders > 1:
    spider_list = []
    spider_num = round(len(threads)/int(spiders))
    
    spider_borders = list(range(0, len(threads), spider_num))
    border_list = []
    
    for i in range(0, len(spider_borders)):
        try:
            border_list.append((spider_borders[i], spider_borders[i+1]))
        except IndexError:
            break
    
    if border_list[-1][1] != len(threads):
        border_list.append((border_list[-1][1], len(threads)))
        
    for border in border_list:
        spider = threading.Thread(target = crawler, args=((threads[border[0]:border[1]],)))
        spider_list.append(spider)
        spider.start()
        
    for spider in spider_list:
        spider.join()
        
    print("Done")
else:
    crawler(threads)