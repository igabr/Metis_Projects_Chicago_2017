This folder contains Jupyter notebooks for Project Luthur of the Metis Data Science Bootcamp - Chicago Summer 2017.

The blog associated to this project can be found [here](https://www.ibrahimgabr.com/blog/2017/7/23/project-2-metis-complete).

The order of the notebooks below, follow my general train of throught and process throughout this project. 

- [Web Scraping Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/02-Project-Luther/Web_scraping_notebook.ipynb) - This notebook contains the code that I used to scrape Rotten Tomatoes.

- [Wikipedia API Scraping Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/02-Project-Luther/Wikipedia_api_scraping.ipynb) - This notebook contains code that interfaced with Wikipedia's API in order to obtain wikipedia.page. These objects then allowed me to access the unique URL's for each movie.

- [Extracting Inforbox Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/02-Project-Luther/Extracting_infobox.ipynb) - This notebook contains code that traversed through all of the wikipedia.page objects, navigated to unique movie URL's and then extracted their respective infobox's. An infobox is usually a short summary of key information on the right hand side of a wikipedia page.

- [Dataframe Construction Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/02-Project-Luther/Dataframe_construction_notebook.ipynb) - This notebook contains code that was used to do a final clean up of my data before it was ready to be placed in a dataframe. This was the last stage of date cleaning/prep before I started my analysis.

- [Model Creation and Analysis Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/02-Project-Luther/Model_Creation_and_Analysis.ipynb) - This notebook contains the final models and analysis for this project.

Additional files:

- [`grid.py`](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/02-Project-Luther/grid.py) - this file contains all the code used in the construction of my Linear Models.

- [`imports.py`](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/02-Project-Luther/imports.py) - this file contains imports to libraries I often use.

- [`helper_functions.py`](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/02-Project-Luther/helper_functions.py) - this file contains helper functions I wrote to speed up common tasks

The focus of this project was data cleaning/munging(ETL) in addition to a first pass at linear regression models using the sklearn library.

You can find my website [here](https://www.ibrahimgabr.com "Ibrahim Gabr").
