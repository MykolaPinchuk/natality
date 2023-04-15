#import Flask 
from flask import Flask, render_template, request
import numpy as np
import joblib, sklearn
from xgboost import XGBRegressor
#create an instance of Flask
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/predict/', methods=['GET','POST'])
def predict():
    if request.method == "POST":
        #get form data
        # tv = request.form.get('tv')
        # radio = request.form.get('radio')
        # newspaper = request.form.get('newspaper')
        is_male = request.form.get('is_male')
        mother_age = request.form.get('mother_age')
        plurality = request.form.get('plurality')
        gestation_weeks = request.form.get('gestation_weeks')
        #call preprocessDataAndPredict and pass inputs
        try:
            prediction = preprocessDataAndPredict(is_male, mother_age, plurality, gestation_weeks)
            #pass prediction to template
            return render_template('predict.html', prediction = prediction)
        except ValueError:
            return "Please Enter valid values"
        pass        
    pass
def preprocessDataAndPredict(is_male, mother_age, plurality, gestation_weeks):
    #put all inputs in array
    test_data = [is_male, mother_age, plurality, gestation_weeks]
    print(test_data)
    #convert value data into numpy array and type float
    test_data = np.array(test_data).astype(np.float) 
    #reshape array
    test_data = test_data.reshape(1,-1)
    print(test_data)
    # LR model:
    # file = open("lr_model.pkl","rb")
    # trained_model = joblib.load(file)
    # # XGB model:
    trained_model = XGBRegressor()
    trained_model.load_model("xgb_model.json")
    prediction = trained_model.predict(test_data)
    return prediction
    pass
if __name__ == '__main__':
    app.run(debug=True)