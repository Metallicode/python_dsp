import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
##    g = np.blackman(200)
##    b = np.hanning(200)
##    k = np.kaiser(200,1)
##    v = np.bartlett(200)

    #draw
##    plt.plot(range(len(g)),-g+1)
##    plt.plot(range(len(b)),b)
##    plt.plot(range(len(k)),k)
    
##    plt.plot(range(len(v)),v)

    t = np.linspace(-50.0,50.0,100)
    s = np.cosh(t)
    plt.plot(range(len(s)),s)

    plt.show()
