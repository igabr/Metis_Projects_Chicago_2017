from flask import Flask, render_template, request
# from flask.ext.bootstrap import Bootstrap
# from flask.ext.scss import Scss
from flaskext.sass import sass
# from flaskext.lesscss import lesscss
from sklearn.externals import joblib
from helper_functions import *
import numpy as np

# sass(app, input_dir='assets/scss', output_dir='static/css')

rf_clf = joblib.load("rf_35_final_model.pkl")
scaler = unpickle_object("scaler_35_features.pkl")
print("model loaded")
order = ('int_rate', 'dti','term_ 60 months','bc_open_to_buy','revol_util','installment','avg_cur_bal','tot_hi_cred_lim','revol_bal','funded_amnt_inv','bc_util','tot_cur_bal','total_bc_limit','total_rev_hi_lim','funded_amnt','loan_amnt','mo_sin_old_rev_tl_op','total_bal_ex_mort','issue_d_Dec-2016','total_acc','mo_sin_old_il_acct','mths_since_recent_bc','total_il_high_credit_limit','inq_last_6mths','acc_open_past_24mths','mo_sin_rcnt_tl','mo_sin_rcnt_rev_tl_op','percent_bc_gt_75','num_rev_accts','mths_since_last_delinq','open_acc','mths_since_recent_inq','grade_B','num_bc_tl','loan_status_Late')


app = Flask(__name__)

sass(app, input_dir='assets/scss', output_dir='static/css')


@app.route('/')

def index():
	return render_template('index.html')

@app.route('/data_entry')
def data_entry():
	return render_template("data_entry.html")

@app.route('/predict', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		dict_of_data = dict(result.items())
		dict_of_data['loan_status_Late'] = 1
		# print(dict_of_data)
		entries = []
		for label in order:
			entries.append(dict_of_data[label])
		array_entries = np.array(entries)
		scaled_entries = np.array(scaler.transform(array_entries).reshape(1,-1)[0][:-1])
		prediction = rf_clf.predict(scaled_entries)[0]

		if prediction == 0:
			prediction = "Result: Will pay on time"
		else:
			prediction = "Result: Will not pay on time"
		return render_template("predict.html", result = result, prediction=prediction)



if __name__ == '__main__':
	app.run()
