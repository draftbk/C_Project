
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re

def get_atom_by_id(id,load):
    print "-------输出 id 为"+str(id)+"的原子坐标--------"
    f = open(load)
    strs=f.readlines()
    pattern = re.compile(r'\S+')
    xyz = re.findall(pattern, strs[id+8])
    print strs[id+8]
    return xyz

def add_point(load,position,ax):
    for i in range(31):
        xyz=get_atom_by_id(i,load)
        if(i<=17):
            ax.scatter(position+float(xyz[0]), float(xyz[1]), float(xyz[2]), c='y')  # 绘制数据点
        else:
            ax.scatter(position+float(xyz[0]), float(xyz[1]), float(xyz[2]), c='r')  # 绘制数据点


def draw():
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    for i in range(1):
        add_point('draw/coordinates/0'+str(i)+'/CONTCAR',i*2,ax)
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()
draw()
