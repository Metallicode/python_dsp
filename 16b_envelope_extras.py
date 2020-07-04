import numpy as np
import matplotlib.pyplot as plt

#x is the value at z & zb intercept. p is z curve power. b is z volume. a is zc curve.
def func(length, x, b, p, a):
    
    t = np.arange(0,1.0*length,1/44100)   
    z = np.zeros_like(t)
    zb = np.zeros_like(t)
    zc = np.zeros_like(t)

    hashaka_index = 0
    
    for i in range(len(t)):
        z[i] = b*t[i]**p
  
    nigzeret = b*p
    shipoa = nigzeret*x**(p-1)

    nekodat_hashaka = (x, b*x**p)

    for i in range(len(t)):
        zb[i] = shipoa*t[i] + (nekodat_hashaka[1] - (shipoa*nekodat_hashaka[0]))
   
    for i in range(len(t)):
        zc[i] =  (a*t[i]**2) + (shipoa*t[i]) + (nekodat_hashaka[1] - (shipoa*nekodat_hashaka[0]))

    plt.plot(t, z)
    plt.plot(t, zb)
    plt.plot(t, zc)
    plt.show()



#shut up and drive...
length = 3

func(length, 0.7, 10, 2, -6)




