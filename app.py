import numpy as np
from flask import Flask, request, render_template

import pickle
import pandas as pd
import numpy as np

# Create flask app
app = Flask(__name__)
pipe = pickle.load(open('./pipe.pkl','rb'))
df = pd.read_csv("./weatherAUS.csv")




@app.route("/")
@app.route("/home")
def Home():
    locations = sorted(df['Location'].unique())
   
    new_loc = []
    i=0
    for x in locations:
        new_loc.append([x,i])
        i+=1
    
    wind9ams = df['WindDir9am'].unique()
    wind9ams = np.delete(wind9ams,8)
    wind9ams = sorted(wind9ams)
    new_wind9ams = []
    i=0
    for x in wind9ams:
        new_wind9ams.append([x,i])
        i+=1

    wind3pms = df['WindDir3pm'].unique()
    wind3pms = np.delete(wind3pms,15)
    wind3pms = sorted(wind3pms)
    new_wind3pms = []
    i=0
    for x in wind3pms:
        new_wind3pms.append([x,i])
        i+=1

    windgusts = df['WindGustDir'].unique()
    windgusts = np.delete(windgusts,8)
    windgusts = sorted(windgusts)
    new_gusts = []
    i=0
    for x in windgusts:
        new_gusts.append([x,i])
        i+=1
    
    return render_template("index.html",locations = new_loc,wind9ams=new_wind9ams,wind3pms=new_wind3pms,windgusts=new_gusts )

@app.route("/predict", methods = ["POST"])
def predict():
    features1 = [float(x) for x in request.form.values()]
    features3  = [np.array(features1)]  
   
    feat = df.iloc[103,1:-1].values
    prediction = pipe.predict(features3)[0]
    if prediction==1:
        return render_template("Rain.html")
    else: return render_template("NoRain.html")
    
    # return render_template("index.html", prediction_msg = f"Rainfall will be there :  {prediction}")

if __name__ == "__main__":
    app.run(debug=True)
