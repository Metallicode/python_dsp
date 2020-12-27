import math

length = 100
t = [i/length for i in range(length)]

s = [math.sin(j*2*math.pi) for j in t]

while True:
        for i in s:
                print('*'*int(((i+1)/2)*60))








    
    
