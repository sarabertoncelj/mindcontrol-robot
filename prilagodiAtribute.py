import pandas as pd
import numpy as np

if __name__ == '__main__':
    primeri1 = pd.read_csv('sara1601/rawData/frownyface1.csv')
    primeri2 = pd.read_csv('sara1601/rawData/frownyface2.csv')
    #primeri3 = pd.read_csv('sara1601/rawData/leva3.csv')
    #primeri4 = pd.read_csv('sara1912/rawData/desna4.csv')

    frames = [primeri1, primeri2]
    rawData = pd.concat(frames)
    df = pd.DataFrame(rawData)
    df = df.reset_index(drop=True)

    #drop T8, AF4, Unknown, X, Y, Z
    blacklist = ["T8", "AF4", "Unknown", "X", "Y", "Z"]
    #blacklist = ["T8", "AF4", "Unknown", "X", "Y", "Z", "F3", "FC6", "P7", "F7", "F8", "F4", "AF3"]
    for key in df.keys():
        if key.split(" ")[0] in blacklist:
            df.pop(key)
    print("Izbrisani so bili stolpci s slabo kvaliteto.")


    #ce je kvaliteta vec kot 5 senzorjev slaba izbrisi vrstico(paket)
    qualityLimit = 1000
    badSensorsLimit = 3
    todrop = []
    for index, row in df.iterrows():
        nmbLowQuality = 0
        for key in row.keys():
            if key.split(" ")[1] == "Quality" and row[key] < qualityLimit:
                nmbLowQuality = nmbLowQuality + 1
        if nmbLowQuality > badSensorsLimit:
            todrop.append(index)

    #print(todrop)
    df = df.drop(todrop)
    print(("Zaradi slabe kvalitete je bilo izpuscenih %d paketov.") % len(todrop))


    #uporabi samo stolpce z value in izpusti tiste s kvaliteto
    for key in df.keys():
        if key.split(" ")[1] == "Quality":
            df.pop(key)
    print("Izbrisani so bili stolpci Quality.")

    #uporabi samo vrstice s quality in izpusti tiste z value
    # for key in rawData.keys():
    #     if key.split(" ")[1] == "Value":
    #         pd.DataFrame(rawData).pop(key)
    # print("Izbrisani so bili stolpci Value.")


    novdf = pd.DataFrame()
    #za zaznavo sprememb na senzorjih
    df = df.reset_index(drop=True)
    df_tran = df.T
    for i in range(int(len(df_tran.keys())/4)):
        #povprecje stirih paketov
        if i * 4 < len(df)-3:
            novdf[i] = (df_tran[i*4] + df_tran[i*4 + 1] + df_tran[i*4 + 2] + df_tran[i*4 + 3])/4
        #razlika med tem in prejsnjim paketom
        #if i > 0:
            #novdf[i] = novdf[i] - novdf[i -1]
    novdf = novdf.T
    print("Izracunano je bilo povprecje paketov.")
    #print(novdf)

    #normaliziramo z odstevanjem povprecne vrednosti za vsak senzor
    averages = {}
    for key in novdf.keys():
        averages[key] = novdf[key].mean()
        #print(averages)
        #print(novdf[key].mean())
    for key in novdf.keys():
        novdf[key] = novdf[key].sub(averages[key])


    #zapis v datoteko
    #print(data)
    #rawData.to_csv('neutralValueDroped.csv', index=False)

    #print(rawData)
    #novdf.to_csv('sara1601/frownyfaceSub.csv', index=False)
