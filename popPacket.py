# -*- coding: utf-8 -*-
# This is an example of popping a packet from the Emotiv class's packet queue

import time
import predict
import numpy as np

from emokit.emotiv import Emotiv

if __name__ == "__main__":
    with Emotiv(display_output=True, verbose=True) as headset:
        while True:
            packet = headset.dequeue()
            #print(packet)
            if packet is not None:
                #print(dir(packet))
                #ps = packet.sensors
                #print(ps['F3']['value'])
                #data = flattenDict(ps)
                #print(data)

                #print(predict.predict([[ps['F3']['value'], ps['F3']['quality'], ps['FC6']['value'], ps['FC6']['quality'], ps['P7']['value'], ps['P7']['quality'],ps['T8']['value'], ps['T8']['quality'],
                    #ps['F7']['value'], ps['F7']['quality'], ps['F8']['value'], ps['F8']['quality'], ps['T7']['value'], ps['T7']['quality'], ps['P8']['value'], ps['P8']['quality'],
                    #ps['AF4']['value'], ps['AF4']['quality'], ps['F4']['value'], ps['F4']['quality'], ps['AF3']['value'], ps['AF3']['quality'], ps['O2']['value'], ps['O2']['quality'],
                    #ps['O1']['value'], ps['O1']['quality'], ps['FC5']['value'], ps['FC5']['quality'], ps['X']['value'], ps['X']['quality'], ps['Y']['value'], ps['Y']['quality'],
                    #ps['Z']['value'], ps['Z']['quality'], ps['Unknown']['value'], ps['Unknown']['quality']]]))
                pass
            time.sleep(0.01)
