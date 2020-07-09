import numpy as np

class Modifier:
    def __init__(self, speed):
        self.speed = speed


    def modifier(self, clip):
        clip_length = clip[1] - clip[0]
        fade_length = clip_length//self.speed
        
        ones = np.ones(clip_length)
        
        t = np.arange(0, 1.0, 1/fade_length)
        
        pa = np.sin(np.pi * 0.5 * t)
        ones[:len(pa)] = pa

        ones[clip_length-len(pa):] = pa[::-1]
            
        return ones*-1+1




if __name__ == '__main__':
    import matplotlib.pyplot as plt

    g = (10,256)
    m = Modifier(15)
    mod = m.modifier(g)
 
    #draw
    plt.plot(range(len(mod)),mod)
    plt.show()
