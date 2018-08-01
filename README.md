# Crawling the boards on http://forum.mods.de/bb/

### Description
With this crawler, you can get all the posts of a specific sub-board on http://forum.mods.de/bb/ in csv files. Several options are included to adjust the crawler's behavior.

### Installation
You'll need to have **Python3** with the following dependencies on your machine:
- Pandas
- BeautifulSoup
- numpy
- several other modules which should come with a standard Python installation.

In general, I would advise you to install the Python distribution Anaconda which already has all of the software pre-installed.

### Usage
Copy the source files into a directory, open up a terminal (e.g. Bash in GNU/Linux or cmd in Windows), and cd into this directory. You can now start the script *crawl_board.py* from your console. Note that the program takes several arguments: Enter `--board_id=` and the number of the board you'd like to crawl.

To speed up the crawling, multi-threading is used. That means multiple instances (called spiders) will crawl the desired board at the same time. You must set the number of spiders with `--spiders=`. However, you should be careful how many spiders you use since the crawl must not generate too much traffic. Else, you might get blocked by the server. `--board_id=` and `--spiders=` are obligatory arguments and represent the bare minimum for a job to start. For example, if you want to crawl board number 99 (codnation) with four spiders, the code would look like this: `python crawl_board.py --board_id=99 --spiders=4`. 

If you want to make sure that you don't send too many requests to the server, you can use both `--pause_breaks=` and `--pause_duration=`. With those commands, you can tell your spiders to  rest for a certain amount of seconds after crawling a certain amount of threads. `--pause_breaks=` will set the number of threads to crawl before resting for a certain amount of seconds specified in `--pause_duration=`. Note that breaks might not occur due to concurrency. If you decide to abort your crawl or your jobs stops for some other reason, you can always continue a once started job with the `--continue_job=` command. This option becomes extremely valuable when you have jobs that you want to split across multiple sessions on your computer. After running the first job, there will be a folder called *Jobs* that contains all the jobs you ran in the form of board_BOARDID_YYYY-MM-DD_HHMMSS. Assume you want to continue the job board_16_2018-01-01_220000, here's how the syntax would look like: `python crawl_board.py --continue_job=board_16_2018-01-01_220000`.

When a job is done and you would like to merge all the csv files into one larger one, you can use the `merge_job` function with its arguments `--job_name=` and `--output_path=` arguments. The first argument specifies the name of the job, not the path. The second argument is the path (including the name of the csv file) where you would like to save the csv file. If you forget to add a ".csv" at the end, the program will do that for you. 

### Output
While crawling, the crawler will output how many threads have already been crawled in your current job. If you choose to continue a job, it will pick up where it left. If the number of threads passes the threshold defined in pause_breaks, the waiting time will be displayed. The data is saved for every page in every thread. Inside the folder Jobs/JOBNAME you will find different folders representing each thread. In every folder there will be one or multiple csv files representing the pages in a given thread. The following variables are included:
- PostText (original post text, no quotes)
- PostSite (site of post in thread)
- PostTime (datetime of post in format DD.MM.YYYY HH:MM:SS)
- Thread (thread id)
- User (the user that published a given post)
- UserQuoted (the last user that was quoted inside the post) 

### Use Case
You can find a comprehensive analysis of the Public Offtopic [pOT] sub-board at: https://s3.eu-central-1.amazonaws.com/hruzik89/pot_data/report.html
