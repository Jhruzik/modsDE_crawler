# Crawling the boards on http://forum.mods.de/bb/

### Description
With this crawler, you can get all the posts of a specific sub-board on http://forum.mods.de/bb/ in a csv file. Optionally, you could limit the search to a specific maximum depth (number of pages).

### Installation
You'll need to have **Python3** with the following dependencies on your machine:
⋅⋅* Pandas
⋅⋅* BeautifulSoup
⋅⋅* numpy

In general, I would advise you to install the Python distribution Anaconda which already has all of the software pre-installed.

### Usage
Copy the source files into a directory, open up a terminal (e.g. Bash in GNU/Linux or cmd in Windows), and cd into this directory. You can now start the script *crawl_board.py* from your console. However, note that the program takes two arguments: one obligatory and one optional. After calling the script within your console, enter the number of the board you'd like to crawl. If you would like to crawl board number 14 (codnation.de), the command would look like this: `python crawl_board.py 99`.
You can find the board number within the url of a board. If you'd like to limit the crawl to a certain number of pages enter this number after the board id. For example, if we want to crawl the first 100 pages of board number 14, we would enter the following syntax into our terminal: `python crawl_board.py 14 100`.

### Output
While crawling, the crawler will print the current status and the remaining workload to the terminal. After finishing the process, you'll find a (new) folder within your program's directory called *Results*. This folder contains your finished job as a csv file. This file contains every single post with the following variables:
⋅⋅* PostText: The post's original text, excluding text from quoted posts.
⋅⋅* PostTime: The date and time when the post was published.
⋅⋅* QuotedUser: If someone was quoted in this post, you'll find the name right here.
⋅⋅* Thread: The link to the thread where the post was submitted to.
⋅⋅* User: The original poster.
⋅⋅* Board: The board's id.

Please note that a semicolon ";" was used as the field separator for the csv. Also, the data is encoded in utf-8.
