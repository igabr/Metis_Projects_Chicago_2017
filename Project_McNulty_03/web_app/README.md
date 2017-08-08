This is the simple web app folder.

In order to run the app in your browser ensure that you have the packages listed in requirements.txt installed.

Also install: https://github.com/imiric/flask-sass

You will also need to download the follwing data files from an Amazon S3 Bucket:

- https://s3.amazonaws.com/project-3-data-files/data_dict.pkl
- https://s3.amazonaws.com/project-3-data-files/rf_35_final_model.pkl
- https://s3.amazonaws.com/project-3-data-files/rf_df_35.pkl
- https://s3.amazonaws.com/project-3-data-files/scaler_35_features.pkl

These data files can be placed in the same place as `main.py`

To run the app, go to your terminal and type `python3 main.py`

This is a very simple app - however, I learned the following things:

- How to download and incorporate bootstrapped HTML/CSS/js files into a flask application.
- How to integrate a machine learning model with a flask application.
- How to write Jinja2 code that runs in tandem with Python.

Potential Next Steps:

- I would like to load a database on the backend in order to store all the information submitted via the form. This would allow me to periodically re-train my machine learning model!

I really hope you enjoy this simple web app!

**NOTE:** Flask is very particular about file structure, should you rename folders or move files around, this may break the app.