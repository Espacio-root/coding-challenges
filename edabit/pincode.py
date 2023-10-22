import numpy as np
import math

def get_combinations(*lst):
    if len(lst) == 1:
        return lst[0]
    elif len(lst) == 2:
        return [e1 + e2 for e1 in lst[0] for e2 in lst[1]]
    return get_combinations(get_combinations(*lst[:-1]), lst[-1])


def crack_pincode(num):
    layout = np.array([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['-', '0', '-']])
    get_cords = lambda n: (3, 1) if n == 0 else ((n-1) // 3, (n-1) % 3)
    distance = lambda x, y: math.sqrt((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2)

    res = [[] for _ in range(len(num))]

    for idx, n in enumerate(num):
        n = int(n)
        x, y = get_cords(n)
        for i in range(4):
            for j in range(3):
                if layout[i][j] != '-' and distance((x, i), (y, j)) <= 1:
                    res[idx].append(layout[i][j])
    return sorted(get_combinations(*res), key=lambda x: int(x))

# Elegant
def crack_pincode(c):
	d,L="08,124,1235,236,1457,24568,3569,478,05789,689".split(','),[""]
	for p in c:L=[y+x for y in L for x in d[int(p)]]
	return L

print(crack_pincode('123'))
