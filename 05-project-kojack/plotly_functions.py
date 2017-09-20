import plotly.plotly as py
import plotly.graph_objs as go

def bar_graph(x_values, y_values, title, xlabel, ylabel, filename):
	"""
	This function returns the plot. It will not automatically display in Jupyter notebook!
	"""
	data = [go.Bar(x=x_values, y=y_values)]

	layout = go.Layout(title=title, yaxis=dict(title=ylabel), xaxis=dict(title=xlabel))

	fig = go.Figure(data=data, layout=layout)

	return py.iplot(fig, filename=filename)

def horizontal_bar_graph(x_values, y_values, title, xlabel, ylabel, filename):
	"""
	This function returns the plot. it will notautomatically display in Jupyter Notebook!
	"""
	data = [go.Bar(x=x_values, y=y_values, orientation='h',)]

	layout = go.Layout(title=title, yaxis=dict(title=ylabel), xaxis=dict(title=xlabel))

	fig = go.Figure(data=data, layout=layout)

	return py.iplot(fig, filename=filename)

def line_graph(x_values, y_values, title, xlabel, ylabel, filename):
	"""
	This function returns the plot. it will notautomatically display in Jupyter Notebook!
	"""
	data = [go.Scatter(x=x_values, y=y_values)]

	layout = go.Layout(title=title, yaxis=dict(title=ylabel), xaxis=dict(title=xlabel))

	fig = go.Figure(data=data, layout=layout)

	return py.iplot(fig, filename=filename)