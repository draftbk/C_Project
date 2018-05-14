# -*- coding:utf-8 -*-
import os
import re
import random

def get_energy():
    h=0
    s = os.popen("./sh")
    info = s.readlines()
    s.close()
    print "-------输出焓--------"
    str= info[-1]
    # 提取能量值
    h= re.findall(r"F= (.+?) E0", str)[0]
    print float(h)
    return h

def get_atoms():
    print "-------输出原子信息--------"
    f=open('POSCAR')
    strs=f.readlines()
    f.close()
    for str in strs[8:]:
        print str

def get_atom_by_id(id):
    print "-------输出 id 为"+str(id)+"的原子坐标--------"
    f=open('POSCAR')
    strs=f.readlines()
    pattern = re.compile(r'\S+')
    xyz = re.findall(pattern, strs[id+7])
    print strs[id+7]
    print "x:"+xyz[0]
    print "y:" + xyz[1]
    print "z:" + xyz[2]
    return xyz

def change_atoms(id):
    step=0.1/15
    print "-------更改原子:"+str(id)+"--------"
    f=open('POSCAR','r')
    strs=f.readlines()
    f.close()
    xyz=get_atom_by_id(id)
    x_step=random.uniform(-step,step)
    y_step = random.uniform(-step, step)
    z_step = random.uniform(-step, step)
    x=float(xyz[0])+float(x_step)
    y = float(xyz[1]) + float(y_step)
    z = float(xyz[2]) + float(z_step)
    strs[id+7]=" "+str(x)+" "+str(y)+" "+str(z)+"\n"
    f=open('POSCAR','w')
    f.truncate()
    for str_temp in strs:
        f.write(str_temp)
    f.close()

def SA_Test():
    T=100 # 初始化温度

    initEnergy=get_energy()


def main():
    # get_atoms()
    get_energy()
    change_atoms(1)
    get_atom_by_id(1)
    get_energy()
main()