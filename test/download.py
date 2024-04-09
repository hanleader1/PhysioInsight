import neurokit2 as nk
import numpy as np


rsp=nk.data(dataset="rsp_1000hz")
np.savetxt("../data/unknownSignal/rsp0_100s_1000hz_down.txt", rsp[0:100000])