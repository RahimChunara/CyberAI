from flask import Flask
from flask import jsonify,request
from flask import render_template
import tensorflow
import pandas as pd
import numpy as np
pred_model = tensorflow.keras.models.load_model("model1.h5")
test=pd.read_csv('test.csv')
test.head() #remove this line later
X_test = test.iloc[:,0:30].values.astype(int)
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
  if request.method == "POST":
    predictions = pred_model.predict(X_test)
    df = pd.DataFrame(predictions)
    print(df)
    gg=df.values.tolist()
    output="The Site is Phishing"
    if gg[0][0]>0.5:
      output=="The Site is CLEAR"     
    return jsonify({"response":output})
       
  else:

      return jsonify({"response":"HIIIIII"})

if __name__ == "__main__":
    app.run(threaded=False)
