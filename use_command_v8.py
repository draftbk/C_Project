# -*- coding:utf-8 -*-
import os
import re
import random
import time
from random import choice
import shutil
import Queue
import numpy



def initDeal():
    # 清空roads文件夹
    shutil.rmtree('roads')
    os.mkdir('roads')
    # 清空xyzs文件夹
    shutil.rmtree('xyzs')
    os.mkdir('xyzs')
    shutil.rmtree('xyzs2')
    os.mkdir('xyzs2')
    shutil.rmtree('xyzs3')
    os.mkdir('xyzs3')
    # 清空energy
    f = open('energy', 'w')
    f.truncate()
    f.close()
    # 把coo_init复制回coo
    f = open('coo_init')
    strs = f.readlines()
    f = open('coo', 'w')
    f.truncate()
    for str_temp in strs:
        f.write(str_temp)
    f.close()

def get_coo():
    f = open('coo')
    strs = f.readlines()
    f.close()
    return strs

def set_coo(strs):
    f=open('coo','w')
    f.truncate()
    for str_temp in strs:
        f.write(str_temp)
    f.close()

def saveToFinal():
    f = open('coo')
    strs = f.readlines()
    f = open('coo_final', 'w')
    f.truncate()
    for str_temp in strs:
        f.write(str_temp)
    f.close()

def saveToXYZ(n,atomNumber):
    f = open('out.xyz')
    strs = f.readlines()
    f = open('xyzs/out'+str(n)+'.xyz', 'w')
    f.truncate()
    for str_temp in strs:
        f.write(str_temp)
    f = open('out.xyz', 'w')
    f.truncate()
    f.close()
    pattern = re.compile(r'\S+')
    xyzs = []
    for i in strs[-atomNumber:]:
        xyz = re.findall(pattern, i)
        xyzs.append("1" + " " + xyz[1] + " " + xyz[2] + " " + xyz[3])

    f = open('xyzs2/out_'+str(n)+'_after'+'.xyz', 'w')
    f.truncate()
    f.write(str(atomNumber)+"\nAtoms. Timestep: 0\n")
    for str_temp in xyzs:
        f.write(str_temp + "\n")
    f.close()
    xyzs = []
    for i in strs[2:atomNumber+2]:
        xyz = re.findall(pattern, i)
        xyzs.append("1" + " " + xyz[1] + " " + xyz[2] + " " + xyz[3])

    f = open('xyzs2/out_'+str(n)+'_0'+'.xyz', 'w')
    f.truncate()
    f.write(str(atomNumber) + "\nAtoms. Timestep: 0\n")
    for str_temp in xyzs:
        f.write(str_temp + "\n")
    f.close()

def saveToRoad(i):
    f = open('coo')
    strs = f.readlines()
    f = open('roads/coo_final'+str(i), 'w')
    f.truncate()
    for str_temp in strs:
        f.write(str_temp)
    f.close()

def saveToRoadLog(strs):
    f = open('log_road', 'w')
    f.writelines(strs)
    f.close()

def get_enthalpy():
    # s = os.popen("lmp_mpi <lammps.in")
    # info = s.readlines()
    # s.close()
    # # print "-------输出焓--------"
    # tag = 0
    # for line in info:  # 按行遍历
    #     line = line.strip('\r\n')
    #     if (tag == 1):
    #         # print "energy: "+line
    #         return line
    #     if (line == "enthalpy"):
    #         tag = 1
    # return 0
    a,b=get_0_and_after_enthalpy()
    return b

def get_0_and_after_enthalpy():
    s = os.popen("lmp_intel_cpu_intelmpi <lammps.in")
    energy_0=0
    energy_after=0
    info = s.readlines()
    s.close()
    # print "-------输出焓--------"
    tag = 0
    for line in info:  # 按行遍历
        line = line.strip('\r\n')
        if (tag == 2):
            # print "energy: "+line
            regex = re.compile('\s+')
            energy_after=regex.split(line)[3]
            return energy_0,energy_after
        if (tag == 1):
            # print "energy: "+line
            regex = re.compile('\s+')
            energy_0=regex.split(line)[3]
            tag=2
        if (line == "Step Temp E_pair E_mol TotEng Press "):
            tag = 1
    return 0

def get_atoms():
    # print "-------输出原子信息--------"
    strs=get_coo()
    tagStart=0
    for str in strs:
        if(tagStart==1):
            pattern = re.compile(r'\S+')
            atom= re.findall(pattern, str)
            if len(atom)>0:
                print atom
        if str.find("Atoms")==0:
            tagStart=1


def get_atom_by_id(id):
    strs=get_coo()
    pattern = re.compile(r'\S+')
    xyz = re.findall(pattern, strs[id+11])
    return xyz

def get_atoms_center(number):
    # print "-------输出原子信息--------"
    strs=get_coo()
    tagStart=0
    x=[]
    y=[]
    z=[]
    center=[]
    for str in strs:
        if(tagStart==1):
            pattern = re.compile(r'\S+')
            atom= re.findall(pattern, str)
            if len(atom)>0:
                x.append(float(atom[2]))
                y.append(float(atom[3]))
                z.append(float(atom[4]))
        if str.find("Atoms")==0:
            tagStart=1
    center.append(numpy.mean(x))
    center.append(numpy.mean(y))
    center.append(numpy.mean(z))
    return center

def change_atom_by_id(id):
    step=0.3
    # print "-------更改原子:"+str(id)+"--------"
    strs=get_coo()
    xyz=get_atom_by_id(id)
    x_step=random.uniform(-step,step)
    y_step = random.uniform(-step, step)
    z_step = random.uniform(-step, step)
    x=float(xyz[2])+float(x_step)
    y = float(xyz[3]) + float(y_step)
    z = float(xyz[4]) + float(z_step)
    strs[id+11]=str(id)+" "+"1"+" "+str(x)+" "+str(y)+" "+str(z)+"\n"
    set_coo(strs)

def change_all_atoms(number):
    center=get_atoms_center(number)
    strs=get_coo()
    for i in range(number):
        id=i+1
        pattern = re.compile(r'\S+')
        xyzs= re.findall(pattern, strs[id+11])
        distance_2=pow(float(xyzs[2])-center[0],2)+pow(float(xyzs[3])-center[1],2)+pow(float(xyzs[4])-center[2],2)
        distance=pow(distance_2,1.0/2.0)
        step = distance / 400.0+0.02
        x_step = random.uniform(-step, step)
        y_step = random.uniform(-step, step)
        z_step = random.uniform(-step, step)
        step_dis=pow(pow(x_step,2)+pow(y_step,2)+pow(z_step,2), 1.0 / 2.0)
        x_step=x_step*step/step_dis
        y_step = y_step * step / step_dis
        z_step = z_step * step / step_dis
        x = float(xyzs[2]) + float(x_step)
        y = float(xyzs[3]) + float(y_step)
        z = float(xyzs[4]) + float(z_step)
        strs[id + 11] = str(id) + " " + "1" + " " + str(x) + " " + str(y) + " " + str(z) + "\n"
    set_coo(strs)

def get_xyz_after_optimization(lastNUmber):
    f = open('out.xyz')
    strs = f.readlines()
    f.close()
    j=0
    pattern = re.compile(r'\S+')
    xyzs=[]
    for i in strs[-lastNUmber:]:
        j=j+1
        xyz = re.findall(pattern, i)
        xyzs.append(str(j) + " " + "1" + " " + xyz[1] + " " + xyz[2] + " " + xyz[3])
    return xyzs

def get_coo_after_optimization(lastNUmber):
    xyzs=get_xyz_after_optimization(lastNUmber)
    strs=get_coo()
    j=0
    for i in xyzs:
        j=j+1
        strs[j + 11] = i+"\n"
    return strs

def saveToEnergy(y1, y2):
    f = open('energy', 'w')
    j=0
    for i in y1:
        if j==0:
            f.writelines(i)
            j=1
        else:
            f.writelines(","+i)
    f.writelines("\n")
    j = 0
    for i in y2:
        if j == 0:
            f.writelines(i)
            j = 1
        else:
            f.writelines("," + i)
    f.close()

def run():
    atomNumber = 4000
    # 一些初始化操作
    initDeal()
    # 计算时间用
    start = time.clock()
    # 初始化最大值
    total_max = get_enthalpy()
    print "初始能量是: " + total_max
    # get_atoms()
    choose_list = []
    for i in range(atomNumber):
        choose_list.append(i + 1)
    # 一个元素选中后多少次以后才能被重新选中
    unpickTime = 10
    q = Queue.Queue(maxsize=unpickTime)
    not_better_length = 0
    total_length = 0
    # 初始化折线图的xy
    y = []
    y1 = []
    y2 = []
    while not_better_length < 100:
        not_better_length = not_better_length + 1
        total_length = total_length + 1
        print "循环进行到: " + str(total_length) + "  连续未找到更优解的长度为: " + str(not_better_length)
        initStr = get_coo()
        tempStr = get_coo()
        id = choice(choose_list)
        choose_list.remove(id)
        if (q.full()):
            choose_list.append(q.get())
        q.put(id)
        print id
        temp_max = 10000
        # 把现在文件状态保存到roads文件夹
        saveToRoad(total_length)
        # 保存x,y
        # x.append(total_length)
        y.append(get_enthalpy())
        e_0, e_after = get_0_and_after_enthalpy()
        y1.append(e_0)
        y2.append(e_after)
        # 清空out.xyz
        f = open('out.xyz', 'w')
        f.truncate()
        f.close()
        # 产生out
        get_enthalpy()
        # 把现在xyz文件保存到xyzs文件夹
        saveToXYZ(total_length, atomNumber)
        for j in range(20):
            # change_atom_by_id(id)
            change_all_atoms(atomNumber)
            f = get_enthalpy()
            # print f
            if float(f) < temp_max:
                temp_max = float(f)
                tempStr = get_coo_after_optimization(atomNumber)
                if float(f) < total_max:
                    total_max = float(f)
                    saveToFinal()
                    not_better_length = 0
                    print "留下改变" + "此时能量为: " + f
            set_coo(initStr)
        set_coo(tempStr)
    saveToEnergy(y1, y2)
    elapsed = (time.clock() - start)
    print("Time used:", elapsed)


def save_to_data(name):
    dir="../Data_Saving_3/"+str(name)
    print os.popen("mkdir "+dir)
    # print os.popen("cp -R roads "+dir)
    print os.popen("cp -R xyzs2 "+dir)
    print os.popen("cp -R energy "+dir)


def main():
    for i in range(8,100):
        run()
        save_to_data(i)

main()
