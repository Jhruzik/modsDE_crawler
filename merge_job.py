import sys
import os
import re


sys_args_col = " ".join(sys.argv[1:])
allowed_params = re.compile("(--job_name=\S+|--output_path=\S+)")

if not all([re.search(allowed_params, x) for x in sys.argv[1:]]):
    raise ValueError("One of your arguments is unkown. Please consult the documentation.")
    
job_name = re.search("(?<=--job_name=)\S+", sys_args_col).group()
job_path = os.path.join(os.getcwd(), "Jobs", job_name, "Results/")
output_path = re.search("(?<=--output_path=)\S+", sys_args_col).group()
if not output_path.endswith(".csv"): output_path = output_path+".csv"


walk = os.walk(job_path)
file_list = []


for part in walk:
    for csv in part[2]:
        file_list.append(os.path.join(part[0], csv))
        
with open(output_path, mode = "w", encoding = "utf-8") as output:
    output.write(open(file_list[1], mode = "r", encoding = "utf-8").readline())
        
with open(output_path, mode = "a", encoding = "utf-8") as output:
    i = 1
    pars_len = str(len(file_list))
    for file in file_list:
        print("Parsing file #"+str(i)+" of "+pars_len)
        i += 1
        with open(file, mode = "r", encoding = "utf-8") as input_file:
            next(input_file)
            for line in input_file:
                output.write(line)
