from prophet_helper import *
from sklearn.metrics import mean_squared_error
def prophet_baseline_BTC(df, window, col_name):
	"""
	This function creates the Prophet Baseline Model for 
	predicting the price of BTC on the basis of the BTC Time Series alone.
	"""

	pred_lst = []
	true_lst = []
	MSE_lst = []

	cnt = 0

	all_rows = df.shape[0]

	while cnt < window:
		start = df.iloc[cnt:all_rows-window+cnt, :].index[0].date()
		end = df.iloc[cnt:all_rows-window+cnt, :].index[-1].date()
		predicting = df.iloc[all_rows-window+cnt, :].name.date()

		print("Running model from {} to {} and predicting on {}".format(start,end,predicting))
		print()

		prophet_forecast_df = df.iloc[:all_rows-window+cnt, :][col_name]

		y_true = df.iloc[all_rows-window+cnt, :][col_name]
		
		print("True value of {} on {} is {}".format(col_name, predicting, y_true))
		
		y_pred = prophet_forecast(prophet_forecast_df)
		
		print()
		pred_lst.append(y_pred)
		
		true_lst.append(y_true)

		cnt += 1
	overall_mse = mean_squared_error(true_lst, pred_lst)
	print("This TS model for BTC has an MSE score of {}".format(overall_mse))

	return true_lst, pred_lst
