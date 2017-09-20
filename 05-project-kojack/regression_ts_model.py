import numpy as np
import math
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from prophet_helper import *

## Keep sklearn implementation as you want beta plots. Could possibly just do with stats models.

def master(df, window):
	"""
	Drop open and close
	You need to have the date as the index in this dataframe.
	"""
	betas_to_graph = []
	pred_lst = []
	true_lst = []

	cnt = 0

	all_rows = df.shape[0]

	while cnt < window:
		start = df.iloc[cnt:all_rows-window+cnt, :].index[0].date()
		end = df.iloc[cnt:all_rows-window+cnt, :].index[-1].date()
		predicting = df.iloc[all_rows-window+cnt, :].name.date()

		print("---- Running model from {} to {} and predicting on {} ----".format(start,end,predicting))

		training_df = df.iloc[cnt:all_rows-window+cnt, :]

		testing_df = df.iloc[all_rows-window+cnt, :]

		prophet_df = df.iloc[:all_rows-window+cnt, :]

		print("Creating Time series models: ")
		
		prophet_predictions = [] #needs to be instantiated for every window

		for column in prophet_df.columns[:-1]:
			true_feature = testing_df[column]
			print("The real value for {} on {} is {}".format(column, testing_df.name.date(), true_feature))
			prophet_predictions.append(prophet_forecast(training_df[column]))

		
		prophet_sm_predictions = prophet_predictions[:] #making exact copy
		prophet_sm_predictions.insert(0,1) #adding the constant

		X_train = training_df.iloc[:, :-1].values #good dimensions

		X_test = np.array(prophet_predictions).reshape(1,-1)
		X_test_sm = np.array(prophet_sm_predictions).reshape(1,-1) #for sm model.

		# print("This is the X_test array: {}".format(X_test))

		y_train = training_df.iloc[:, -1].values.reshape(-1,1) #good dimensions

		y_true = np.array(testing_df[-1]).reshape(1,1) #good dimensions

		lm = LinearRegression()

		X_train_sm = sm.add_constant(X_train)

		model = sm.OLS(y_train, X_train_sm)

		fit = model.fit()

		fitted_model = lm.fit(X_train, y_train)

		coef_lst = []
		best_features = []
		val_lst = []

		for index, value in enumerate(fitted_model.coef_[0]):
			coef_lst.append((index, value))

		coef_lst = sorted(coef_lst, key=lambda x: x[1], reverse=True)

		for index, value in coef_lst:
			if value != 0: #just want features that have an effect.
				best_features.append(index)
				val_lst.append(value)

		betas_to_graph.append(list(zip(df.iloc[:, best_features].columns, val_lst)))

		y_pred = fitted_model.predict(X_test)

		print("The real value of {} was {} on {}".format(testing_df.index[-1], y_true, testing_df.name.date()))
		print("The predicted value of {} was {} on {}".format(testing_df.index[-1], y_pred, testing_df.name.date()))
		print()
		print(fit.summary())
		print()

		pred_lst.append(y_pred)
		true_lst.append(y_true)

		cnt += 1

	pred_lst = [float(x) for x in pred_lst]
	true_lst = [float(x) for x in true_lst]

	overall_rmse = mean_squared_error(true_lst, pred_lst)**0.05 
	
	print("This model architecture with {} features has an RMSE score of {}".format(df.shape[1], overall_rmse))

	return betas_to_graph, pred_lst, true_lst
