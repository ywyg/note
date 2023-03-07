def generator_f(max):
    list_l = [1]
    index = 1
    while index <= max:
        tmp_list = []
        for ii in range(index):
            value = 0
            if ii - 1 >= 0 and ii <= len(list_l) - 1:
                value = list_l[ii - 1] + list_l[ii]
            elif ii - 1 >= 0:
                value = value + list_l[ii - 1]
            elif ii <= len(list_l) - 1:
                value = value + list_l[ii]
            tmp_list.append(value)
        yield tmp_list
        list_l = tmp_list
        index += 1

def triangles(size):
    if size < 1:
        return None
    L = []
    for i in range(1, size+1):
        if i < 3:
            L.append(1)
            yield L
        else:
            L2 = [1]
            for j in range(1, i-1):
                L2.append(L[j-1] + L[j])
            L2.append(1)
            yield L2
            L = L2


if __name__ == '__main__':
    for i in triangles(5):
        print(i)
