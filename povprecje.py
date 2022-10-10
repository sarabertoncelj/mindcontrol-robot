import pandas as pd
import numpy as np

if __name__ == '__main__':
    primeri1 = pd.read_csv('sara1501/desnaFinalAvg.csv')
    #primeri2 = pd.read_csv('desnaQuality.1912.csv')
    #primeri3 = pd.read_csv('levaQuality.1501.csv')
    #primeri4 = pd.read_csv('levaQuality.1912.csv')
    #primeri5 = pd.read_csv('neutralQuality.1501.csv')
    #primeri6 = pd.read_csv('neutralQuality.1912.csv')
    #frames = [primeri1, primeri2, primeri3]
    #rawData = pd.concat(frames)
    #print(len(rawData))


    for key in primeri1.keys():
        print(key)
        print(pd.DataFrame(primeri1)[key].mean())


    #print(data)
    #data.to_csv('neutralValue.csv', index=False)

    #print(rawData)
    #rawData.to_csv('allQuality.csv', index=False)
