from flask import render_template, request, jsonify,Flask
import flask
import numpy as np
#from flask_restful import Resource, Api
import traceback
import pickle
import pandas as pd
#import datetime
from datetime import datetime, timedelta
from pmdarima import auto_arima
# App definition
app = Flask(__name__)
#api = Api(app)
 
# importing models
with open('model_fit1.pkl', 'rb') as f:
   model = pickle.load(f)
 
#with open('webapp/model/model_columns.pkl', 'rb') as f:
   #model_columns = pickle.load (f)
 
 
@app.route('/')
def welcome():
   return render_template('home.html')
 
@app.route('/predict', methods=['POST','GET'])
def predict():
   if flask.request.method == 'GET':
       return "Date"
 
   elif flask.request.method == 'POST':
       Date = request.form['Date']
       #datetime.strptime
       ndate1 =datetime.strptime(Date,"%Y-%m-%d").date()
       list_of_dates = []
       #date_obj = datetime.strptime(Date, '%Y-%m-%d')
       for i in range(1,11):
           dates = ndate1 + timedelta(days = i)
           list_of_dates.append(dates)
           #return list_of_dates
       mdate1 = datetime.strptime('2019-09-28', "%Y-%m-%d").date()
       #ndate1 =datetime.strptime(Date,"%Y-%m-%d").date()
       time_delta =  (ndate1 - mdate1).days
       count = time_delta +10
       try:
           future_forecast = model.predict(start = 0, end= count)
           tan_preds = list(reversed(future_forecast))
           new_tan_preds = []
           for i in range(0,10):
               new_tan_preds.append(tan_preds[i])
           prediction = pd.DataFrame(new_tan_preds,columns = ['Predicted price of Tandoori'])
           dates = pd.DataFrame(list_of_dates,columns = ['Dates'])
           final_dataframe = pd.concat([dates,prediction],axis = 1)
           final_dataframe['Date'] = final_dataframe['Dates'].astype(str)
           final_dataframe.drop(['Dates'],axis = 1,inplace = True)
           a = final_dataframe.to_json(orient = 'records')
           return a
           #result = {}
           #for index, row in df2.iterrows():
            #result[index] = row.to_json() 
              # result[index] = dict(row)
         #  return jsonify(result)
           #api.add_resource(prediction,'/predict')
 
       except:
           return jsonify({
               "trace": traceback.format_exc()
               })
#api.add_resource(prediction,'/predict')    
 
if __name__ == "__main__":
   app.run(debug = True)