import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import copy

def get_colore_gradient(data, revers=False):
    # data = {'A-B4': 9, 'Jopa': 1, 'Huy': 5, 'Lol': 4, 'Ebat1': 9, 'Jopa1': 1, 'Huy1': 5, 'Lol1': 4}
    data = copy.deepcopy(data)

    color1 = 'green'
    color2 = 'red'

    if revers:
        color1 = 'red'
        color2 = 'green'
    n = len(data)

    # print(min(values))
    # print(max(values))
    # print(sorted(data.items(), key=lambda item: item[1]))

    values = list(data.values())
    try:
        _min = min(values)
        _max = max(values)
    except:
        _min = 0
        _max = 1
    sort_list = sorted(data.items(), key=lambda item: item[1])

    def color(color1, color2, mix=0):
        c1 = np.array(mpl.colors.to_rgb(color1))
        c2 = np.array(mpl.colors.to_rgb(color2))
        return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

    fig, ax = plt.subplots(figsize=(8, 5))

    for x in range(n):
        key_name = {i for i in data if data[i] == min(values)}
        ax.axvline(x, color=color(color1, color2, x/n), linewidth=4)
        data.update({list(key_name)[0]: color(color1, color2, x/n)})
        values.remove(min(values))

    return data, _max, _min 
# print(data)
# plt.show()

test_grad = {
 'D8-D4': 0,
 'D4-C3/E': 1,
 'C3/E-X4': 2,
 'C3/E-C2/E': 3,
 'H7/D14-C3/E': 4,
 'H7/D14-D9': 5,
 'D9-C3': 6,
 'D20-C3': 7,
 'D6-C3': 8,
 'D6-C2/D2': 9,
 'D1/10-C2/D2': 10,
 'D5-C2/D2': 11,
 'C2/D2-I3/E': 12,
 'G1-C2/D2': 13,
 'C2/D2-G1': 14,
 'D3-D2': 15,
 'D3-G1': 16,
 'D2-D3': 17,
 'G9-D3': 18,
 'G8-G9': 19,
 'G8-G1': 20,
 'G1-G8': 21,
 'Y2-G8': 22,
 'G10-G9': 23,
 'G10-G5': 24,
 'G4-G8': 25,
 'D15-G10': 26,
 'G7-G5': 27,
 'G5-G3': 28,
 'G3-G4': 29,
 'G4-G9': 30,
 'G6-G4': 31,
 'Y1-G6': 32,
 'K-G-6': 33,
 'D19-K': 34,
 'D21-K': 35,
 'F1-D14': 36,
 'D16-D14': 37,
 'A-B4': 38,
 'B4-B5': 39,
 'B5-J1': 40,
 'B6-J1': 41,
 'J1-KX6': 42,
 'J1-KX3': 43,
 'Z1-J2': 44,
 'J2-KX3/X6': 45,
 'B3-J2': 46,
 'J3-J2': 47
 }

if __name__ == "__main__":
    print(get_colore_gradient({'A-B4': 9, 'J3-J2': 1, 'J1-KX6': 5, 'J1-KX3': 4, 'J2-KX3/X6': 9, 'B3-J2': 1, 'J3-J2': 5, 'G3-G4': 4}))



