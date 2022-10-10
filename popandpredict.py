import time
import numpy as np
import pandas as pd
from keras.models import model_from_json
from emokit.emotiv import Emotiv
from sklearn.externals import joblib

if __name__ == "__main__":

    # # load json and create model
    json_file = open('modeli/model1601F-sara1501.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("modeli/model1601F-sara1501.h5")
    print("Loaded model from disk")

    #from sklearn.preprocessing import StandardScaler
    sc = joblib.load('modeli/scaler1601F.save')

    with Emotiv(display_output=False, verbose=True) as headset:
        #levo = 0
        #desno = 0
        nmbPackets = 0
        prejsnjePovprecje = 0
        packets = pd.DataFrame()
        while True:
            packet = headset.dequeue()
            if packet is not None:

                if nmbPackets < 4:
                    df = pd.DataFrame(packet.sensors)

                    #drop T8, AF4, Unknown, X, Y, Z
                    blacklist = ["T8", "AF4", "Unknown", "X", "Y", "Z", "F3", "FC6", "P7", "F7", "F8", "F4", "AF3"]
                    #blacklist = ["T8", "AF4", "Unknown", "X", "Y", "Z"]
                    for key in df.keys():
                        if key.split(" ")[0] in blacklist:
                             df.pop(key)

                    #ce je kvaliteta vec kot 5 senzorjev slaba ne upostevaj paketa
                    qualityLimit = 1000
                    badSensorsLimit = 5
                    nmbLowQuality = 0
                    for key in df.keys():
                        if df[key]['quality'] < qualityLimit:
                            nmbLowQuality = nmbLowQuality + 1
                    if nmbLowQuality < badSensorsLimit:
                        #uporabi samo vrstice z value in izpusti tiste s kvaliteto
                        packets = packets.append(df.loc[['value']], ignore_index = True)
                        nmbPackets = nmbPackets + 1

                else:
                    nmbPackets = 0

                    #print(packets)

                    #za zaznavo sprememb na senzorjih
                    packets = packets.reset_index(drop=True)
                    df_tran = packets.T
                    povprecje = (df_tran[0] + df_tran[1] + df_tran[2] + df_tran[3])/4

                    #razlika med tem in prejsnjim paketom
                    #razlika = povprecje - prejsnjePovprecje
                    #prejsnjePovprecje = povprecje


                    #razlika = sc.transform([razlika])
                    razlika = sc.transform([povprecje])
                    addedResult = loaded_model.predict(razlika)[0]
                    print(addedResult)
                    # addedResult = addedResult + loaded_model.predict(sensorData)
                    #
                    # if addedResult[0] > addedResult[1] and addedResult[0] > addedResult[2]:
                    #     print("levo")
                    # elif addedResult[1] > addedResult[2]:
                    #     #print("nevtralno")
                    #     pass
                    # else:
                    #     print("desno")


                    packets = pd.DataFrame()





            time.sleep(0.01)
