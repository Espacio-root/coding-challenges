def int_to_vlq(n,i=0):
    if n < 128:
        return [n+(128*i)]
    return int_to_vlq(n//128, 1) + [n%128+(i*128)]

def vlq_to_int(lst):
    if len(lst) == 1:
        return lst[0]
    return (lst.pop(0) - 128) * 128 ** (len(lst)) + vlq_to_int(lst)

print(int_to_vlq(12))
