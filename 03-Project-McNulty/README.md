This folder contains Jupyter notebooks for Project McNulty of the Metis Data Science Bootcamp - Chicago Summer 2017.

The focus of this project was classification - I specifically focused on Random Forests as they represent a powerful ensemble method. If I had more time, I would have also considered boosted trees.

# Learning Overview

At a high level, this project taught me the following:

- Flask python backend web development

- Intimate familiarity with Sci-Kit Learn's numerous classification modules in addition to hyper-parameter tuning.

- I had problems with GridSearchCV on AWS EC2 (job would hang for hours), however, this forced me to manually write the loops that GridSearchCV does automatically. This was an excellent exercise. The downside was that I could not truly optimize my hyper-parameters.

- AWS EC2. Instance set up, memory/core management. My data was extremely large, as such, I had to implement various techniques for processing data that doesn't fit in memory. This was a mixture of batch processing and spinning up very large EC2 instances (64 cores/256GB RAM)

- AWS S3, integration with any and all EC2 instances in addition to transporting files from instances to local machine.
  - I wrote my own wrapper around [`boto3`](https://boto3.readthedocs.io/en/latest/) in order to flawlessly use AWS S3. You can view this in [`s3.py`](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/s3.py).
  - I will write a detailed [blog](https://www.ibrahimgabr.com/blog) post about how to use this script with both EC2 and on your local machine.
  
- Simultaneous data pre-processing for classification algorithms, both linear and non-linear. Contrary to popular belief, categorical data must be turned into numbers before being fed to random forests. Labelencoding is not enough, categorical data must be made into dummies! Just Labelencoding will not allow the algorithm to discern between categories. 

- Advanced Imputation Methods: Instead of imputing based on statistical characteristics of mean/median/mode - create a Random Forest Model to predict what the missing values should be. This is an iterative process, as you predict one column at a time - this will create a feedback loop that will certainly bias your data, however, it would be a far more accurate imputation than using statistical characteristics alone. This method is not possible when you have LOTS of missing data (as I did).

- Advanced Plotting: specifically via [plot.ly](https://plot.ly/). This makes for fantastic interative plots in Jupyer Notebooks. They could also be easily rendered on web pages.

# Folders and Notebooks.

The [`web_app`](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/web_app) folder contains all the files and code needed to run a simple web application in your browser.

[Random Forest Parameter Tuning Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/Random_Forest_Parameter_Tuning.ipynb): This notebook contains the code that loops through various Random Forest Hyper-parameters. Ideally, this would be done via GridSearchCV - however, I encountered issues with this on AWS. Most likely due to the size of my data and my stubborness in not just 'randomly' dropping features. _NOTE:_ I have had to include a _static_ picture of my ROC curve. If viewing the notebook on your local machine, the plot will be _interactive_.

[Cleaning and Dummies Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/Cleaning_and_dummies.ipynb): This notebook contains the code used to clean and transform my data into a format compatiable with sklearn algorithms - both classification and generalized linear models (logisitic regression). This process is ciritical for compatibility with sklearn algorithms. For an excellent discussion of difference in datatypes between pandas and Sci-Kit Learn see [here](https://www.safaribooksonline.com/oriole/the-pandas-scikit-learn-data-type-divide).

[Imputation Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/Imputation_Notebook.ipynb): This notebook contains the code I used to impute missing data. I had LOTS of missing data. Ideadlly, I wanted to create a random forest model that would give me an 'intelligent' estimation of what the missing data would be. I have included some pseudo-code of what this would look like. I was unable to implment this as just had too much missing data! As such, I imputed most of the data with the median in addition to employing some 'human' logic. Imputation is critical for sklearn algorithms.

[Baseline Classification Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/Baseline_Classification_Notebook.ipynb): This notebook showcases sklearns [DummyClassifier module](http://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html). Essentially, this notebooks gives me a sense of how my model needs to perform in order for it to be considered better than a 'dumb' algorithm, that is, predicting a particular class always.

[Feature Reduction 35 Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/feature_reduction_35.ipynb): This notebook has the code used to construct the final 35 features that will be used in my final Random Forest model. I extracted there top 35 features using the  `.feature_importances_` method. It also shows how I pickled the standard scaler for later use in my flask app! I also demonstrate how to load a pandas dataframe into a PostgreSQL database and subsequently query the database directly. I hope to have a blog up shortly, describing how to set up a PostgreSQL database on AWS. You can find my blog [here](https://ibrahimgabr.com/blog).

[RF 35 Final Model Notebook](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/rf_35_final_model.ipynb): This notebook contains the final model used in prediction. I had to substantially reduce my feature space in order to make the model 'user friendly' via the flask app. In an ideal world, the customer would fill out a very large online form for a loan, and our code would parse all that information and predict an outcome. I could _easily_ implement this in the future as all the peices of code are present. This notebook also show how to adjust the _cutoff threshold_ for a Random Forest (in fact, all sklearn algorithms). Unfortunately, there is no hyper-parmeter for this.

[Helper Functions Python File](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/helper_functions.py): This file contains helper functions used throughout the project.

[Show Cnf Matrix Python File](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/show_cnf_matrix.py): This python file was oobtained from [here](https://notmatthancock.github.io/2015/10/28/confusion-matrix.html).


**Addendum: Some notebooks may import `helper_loans.py` into the notebook - change this to [`helper_functions.py`](https://github.com/igabr/Metis_Projects_Chicago_2017/blob/master/03-Project-McNulty/helper_functions.py) to avoid the error.**
