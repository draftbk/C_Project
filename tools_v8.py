# -*- coding:utf-8 -*-
import os
import re
import pandas as pd

# atom number
ATOM_NUMBER = 4000


def get_type_xyz(name):
    f = open(name)
    strs = f.readlines()
    f.close()
    return strs


def get_atom_xyz_list(name):
    xyz_list = []
    strs = get_type_xyz(name)
    pattern = re.compile(r'\S+')
    # add one line for the convince of id
    xyz_list.append("xyz_list")
    for i in range(ATOM_NUMBER):
        xyz_str = re.findall(pattern, strs[i + 2])
        xyz = []
        xyz.append(i + 1)
        xyz.append(float(xyz_str[1]))
        xyz.append(float(xyz_str[2]))
        xyz.append(float(xyz_str[3]))
        xyz_list.append(xyz)
    return xyz_list


# parameter:id1,id2,xyz list
def getDistanceFromID(id_1, id_2, xyz_list):
    xyz_1 = xyz_list[id_1]
    xyz_2 = xyz_list[id_2]
    distance_2 = pow(xyz_1[1] - xyz_2[1], 2) + pow(xyz_1[2] - xyz_2[2], 2) + pow(
        xyz_1[3] - xyz_2[3], 2)
    distance = pow(distance_2, 1.0 / 2.0)
    return distance


def saveCSV(type_list, connected_type_list, sp3_list, sp3_connect_list):
    a=[str(len(sp3_connect_list))]
    b=[str(sp3_connect_list)]
    dataframe = pd.DataFrame({'pair_number': a, 'pairs': b})
    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("test.csv", index=False, sep=',')

    # 字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'point_id': type_list[1:], 'point_type': connected_type_list[1:]})
    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("test.csv",mode='a', index=False, sep=',')


def search(name):
    # atom xyz list
    xyz_list = get_atom_xyz_list(name)
    # type list
    type_list = []
    type_list.append("type")
    # connect point list
    connected_list = []
    connected_list.append("connected point")
    # connect point's type list
    connected_type_list = []
    connected_type_list.append("connected type")
    # list sp3
    sp3_list = []
    # get type,and its connect atoms
    for i in range(1, ATOM_NUMBER + 1):
        # print("number "+str(i)+" atom searching")
        # ﻿0~1.3 -> n
        # ﻿1.3~1.5 -> m
        # 1.5~1.6 -> l
        n = 0
        m = 0
        l = 0
        connect_point = []
        for j in range(1, ATOM_NUMBER + 1):
            distance = getDistanceFromID(i, j, xyz_list)
            if distance > 0 and distance <= 1.3:
                connect_point.append(j)
                n = n + 1
            elif distance > 1.3 and distance <= 1.5:
                connect_point.append(j)
                m = m + 1
            elif distance > 1.5 and distance < 1.6:
                connect_point.append(j)
                l = l + 1
        if n == 1 and m == 0 and l == 1:
            type_list.append([i, "sp"])
            print [i, "sp1"]
        elif n == 0 and m == 3 and l == 0:
            type_list.append([i, "sp2"])
            print [i, "sp2"]
        elif n == 0 and m == 0 and l == 4:
            type_list.append([i, "sp3"])
            sp3_list.append(i)
            print [i, "sp3"]
        else:
            if n + m + l >= 4:
                type_list.append([i, "maybe_sp3"])
                print [i, "maybe_sp3"]
                sp3_list.append(i)
            else:
                type_list.append([i, "edge"])
        connected_list.append(connect_point)
    sp3_connect_list = []
    # match connect point and its type
    for i in range(1, ATOM_NUMBER + 1):
        id_list = connected_list[i]
        temp_connected_type_list = []
        for id in id_list:
            if (id in sp3_list and i in sp3_list):
                print ".........3______sp3.............."
                sp3_connect_list.append([id, i])
                print id
                print i
            temp_connected_type_list.append(type_list[id])
        connected_type_list.append(temp_connected_type_list)
    print sp3_list

    saveCSV(type_list, connected_type_list, sp3_list, sp3_connect_list)


def main():
    search("Data_Saving_3/6/xyzs2/out_1180_after.xyz")


main()
