import numpy as np
def EMG_Interpretation(EMG):
    # {"up":0,"down":1,"left":2,"right":3}
    V_y = EMG[0] - EMG[1] 
    V_x = EMG[3] - EMG[2]
    return np.array([V_x,V_y])