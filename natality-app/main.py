import json
import os
import pandas as pd

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


# credentials = GoogleCredentials.get_application_default()
# api = discovery.build('ml', 'v1',
#         credentials=credentials, cache_discovery=False)
# project = os.environ['GOOGLE_CLOUD_PROJECT']
# model_name = os.getenv('MODEL_NAME', 'babyweight')


app = Flask(__name__)


def get_prediction(features):
  # input_data = {'instances': [features]}
  # parent = 'projects/%s/models/%s' % (project, model_name)
  # prediction = api.projects().predict(body=input_data, name=parent).execute()

    trained_model = XGBRegressor()
    trained_model.load_model("xgb_model.json")
    feature_df = pd.DataFrame.from_dict(features,orient='index').T
    prediction = trained_model.predict(feature_df)
    
  return prediction[0]


@app.route('/')
def index():
  return render_template('index.html')


# @app.route('/form')
# def input_form():
#   return render_template('form.html')


@app.route('/api/predict', methods=['POST'])
def predict():
  def gender2int(val):
    genders = {'male': 1, 'female': 0}
    return genders[val]

  data = json.loads(request.data.decode())
  mandatory_items = ['baby_gender', 'mother_age',
                     'plurality', 'gestation_weeks']
  for item in mandatory_items:
    if item not in data.keys():
      return jsonify({'result': 'Set all items.'})

  features = {}
  features['is_male'] = gender2int(data['baby_gender'])
  features['mother_age'] = int(data['mother_age'])
  features['plurality'] = int(data['plurality'])
  features['gestation_weeks'] = float(data['gestation_weeks'])

  prediction = get_prediction(features)
  return jsonify({'result': '{:.2f} lbs.'.format(prediction)})