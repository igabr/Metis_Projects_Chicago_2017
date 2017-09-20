import pandas as pd


def clean_blockchain_csv(df, lst_of_cols):
	assert len(lst_of_cols) == 2, "csv's from blockchain.info only contain 2 columns!"

	df.rename(columns={0: lst_of_cols[0], 1:lst_of_cols[1]}, inplace=True)

	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

	mask = (df['date'] > "2016-10-25") & (df['date'] <= "2017-02-22")

	subset_df = df[mask]

	return subset_df





