from keras.models import model_from_json
import numpy as np
# Feature Scaling
from sklearn.externals import joblib

def predict(sensorData):
    # # load json and create model
    json_file = open('model2012-sara1912.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model2012-sara1912.h5")
    print("Loaded model from disk")

    #from sklearn.preprocessing import StandardScaler
    sc = joblib.load('scaler.save')
    sensorData = sc.transform(sensorData)

    return loaded_model.predict(sensorData)

if __name__ == "__main__":

    tmp = np.array([[-142496,-299280,-760760,-1344,-77504,-560720,-4584,-856680,0,-1425240,-228528,-966240,-1224608,-320112,0,0,0,256]])

    print(predict(tmp))
