def develop_pattern(pat_str):
    length = len(pat_str)
    if(length>2):
        p01 = develop_pattern(pat_str[:length//2])
        p02 = develop_pattern(pat_str[length//2:])
        return p01+p02

    return pat_str*2

def repeate_every(seq, step, times=2):
    s = []
    for i in range(len(seq)):
        s.append(seq[i])
        if i%step==0:
            s.append(seq[i])
    return "".join(s)

my_str = input("enter your string: \n")
x = repeate_every(develop_pattern(my_str), 4)
z = repeate_every(develop_pattern(my_str[::-1]), 4)
print(develop_pattern(x)+develop_pattern(z)[::-1])
