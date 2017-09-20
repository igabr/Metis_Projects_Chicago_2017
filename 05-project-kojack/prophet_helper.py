import pandas as pd
import numpy as np
from fbprophet import Prophet
from datetime import date

def prophet_forecast(row_of_df):
	holidays = []
	df = pd.DataFrame(row_of_df)
	col_name = df.columns[0]
	# print("Creating time series model for {}".format(col_name))
	# print("Starting_date passed to prophet is {}.".format(df.index[0]))
	# print("End date passed to prophet is {}".format(df.index[-1]))

	for d in df.index:
		val = d.weekday()

		if val == 5 or val == 6:
			holidays.append("Weekend")
		else:
			holidays.append("Weekday")

	hol_df = pd.DataFrame(holidays, index=df.index, columns=["holiday"])
	hol_df.reset_index(inplace=True)
	hol_df.rename(columns={"date":"ds"}, inplace=True)

	df.reset_index(inplace=True)
	df.rename(columns={"date":"ds", df.columns[-1]:"y"}, inplace=True)

	m = Prophet(holidays=hol_df, daily_seasonality=False, yearly_seasonality=False)
	m.fit(df)

	future = m.make_future_dataframe(periods=1) #predicting only 1 day into the future
	forecast = m.predict(future)

	y_pred = forecast.yhat[-1:].values[0]

	print("The predicted value for {} on {} is {}".format(col_name, future.iloc[-1, :]['ds'].date(), y_pred))

	return y_pred