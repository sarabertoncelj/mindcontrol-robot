import pandas as pd
import numpy as np

if __name__ == '__main__':
    primeri1 = pd.read_csv('desnaQuality.1501.csv')
    primeri2 = pd.read_csv('desnaQuality.1912.csv')
    primeri3 = pd.read_csv('levaQuality.1501.csv')
    primeri4 = pd.read_csv('levaQuality.1912.csv')
    primeri5 = pd.read_csv('neutralQuality.1501.csv')
    primeri6 = pd.read_csv('neutralQuality.1912.csv')
    frames = [primeri1, primeri2, primeri3, primeri4, primeri5, primeri6]
    rawData = pd.concat(frames)
    #print(len(rawData))


    #uporabi samo vrstice s quality in izpusti tiste z value
    for key in rawData.keys():
        print(key)
        print(pd.DataFrame(rawData)[key].mean())


    #print(data)
    #data.to_csv('neutralValue.csv', index=False)

    #print(rawData)
    #rawData.to_csv('allQuality.csv', index=False)
