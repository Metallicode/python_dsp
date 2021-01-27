while 1:
    BASE = input("Enter base pattern: \n")

    part_a = BASE[:len(BASE)//2]
    part_b = BASE[len(BASE)//2:]

    outro = part_a[:len(part_a)//2][::-1]

    pattern = part_a*2 + part_b + part_b[:-len(outro)] + outro

    #pattern = (part_a + part_b)*2 + part_b[:-len(outro)] + outro*3

    print(pattern)
