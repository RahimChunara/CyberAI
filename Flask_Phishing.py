from flask import Flask
from flask import jsonify,request
from flask import render_template
from flask import request
import tensorflow
import pandas as pd
import numpy as np
from urllib.parse import urlparse
from feature_extraction import generate_data_set
pred_model = tensorflow.keras.models.load_model("model1.h5")

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == "POST":
    print(request.json['data'])
    csv_file = urlparse(request.json['data']).netloc
    # print('%s.csv'%csv_file)
    generate_data_set(request.json['data'])
    test=pd.read_csv('./gg.csv')
    test.head() #remove this line later
    X_test = test.iloc[:,0:30].values.astype(int)
    predictions = pred_model.predict(X_test)
    df = pd.DataFrame(predictions)
    print(df)
    gg=df.values.tolist()
    if gg[0][0]>0.5:
      output="The Site is CLEAR" 
      print(output)    
      return jsonify({"response":output})
    else:
      output="This Site is PHISHING"
      print(output)
      return jsonify({"response":output})

if __name__ == "__main__":
    app.run(threaded=False)
