def ecg_seq_index(n):
    ecg = [1, 2]
    def common_factor(i, j):
        for n in range(2, min(i, j) + 1):
            if i%n==0 and j%n==0:
                return True
        return False
    while n not in ecg:
        i = min(ecg)
        while True:
            if i not in ecg and common_factor(i, ecg[-1]):
                ecg.append(i)
                break
            i += 1
    return ecg.index(n)

def get_gcd(a, b):
    while b:
        a, b = b, a%b
        print(a, b)
    return a

print(get_gcd(4, 5))

