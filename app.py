from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components 

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

#ticker = ''
@app.route('/graph', methods = ['POST'])
def graph():
    ticker = request.form['ticker']
    print("The requested ticker is '" + ticker + "'")
    r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '.json?rows=30')
    df = pd.read_json(r.text, convert_dates=True)
    #print(df.head())
    df = pd.DataFrame( data = df['dataset']['data'], columns = df['dataset']['column_names'])
    y = df['Close'].tolist()
    x = df['Date'].tolist()
    x = np.array(x, dtype=np.datetime64)
    month = x[0] - np.timedelta64(30,'D')
    x=x[x>=month]
    y=y[0:len(x)]
    print('starting to graph')
    title = ticker+' closing prices over past month'
    p = figure(x_axis_type="datetime", title=title)
    p.grid.grid_line_alpha = 0.5
    p.xaxis.axis_label = 'Date (m-d)'
    p.yaxis.axis_label = 'Price ($)'
    p.ygrid.band_fill_color = "olive"
    p.ygrid.band_fill_alpha = 0.1
    p.line(x, y, color='navy')
    print('starting to render')
    script, div = components(p)
    return render_template('graph.html', script=script, div=div)
    #return redirect('/index')

#ticker = request.form.get('ticker')

if __name__ == '__main__':
  app.run(port=33507)#localhost=33507)


'''
print("say hi...")
print(ticker)
url='https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '.json?rows=30'
print(url)
r = requests.get(url)

df = pd.read_json(r.text, convert_dates=True)
print(df.head())

df = pd.DataFrame( data = df['dataset']['data'], columns = df['dataset']['column_names'])

y = df['Close'].tolist()
x = df['Date'].tolist()

x = np.array(x, dtype=np.datetime64)

month = x[0] - np.timedelta64(30,'D')
x=x[x>=month]
y=y[0:len(x)]


from bokeh.plotting import figure
from bokeh.embed import components 

title = ticker+' Closing Price'
p = figure(x_axis_type="datetime", title=title)
p.grid.grid_line_alpha = 0.5
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'Price'
p.ygrid.band_fill_color = "olive"
p.ygrid.band_fill_alpha = 0.1

p.line(x, y, color='navy')


script, div = components(p)
@app.route('/graph')
def graph():
	return render_template('graph.html', script=script, div=div)
'''

