# -*- coding:utf-8 -*-
import os
import re
import random
import time
from random import choice
import shutil
import math
import Queue
import numpy


def initDeal():
    # 清空roads文件夹
    shutil.rmtree('roads')
    os.mkdir('roads')
    # 清空xyzs文件夹
    shutil.rmtree('xyzs')
    os.mkdir('xyzs')
    # 清空xyzs2文件夹
    shutil.rmtree('xyzs2')
    os.mkdir('xyzs2')
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

def saveToXYZ(i):
    f = open('out.xyz')
    strs = f.readlines()
    f = open('xyzs/out'+str(i)+'.xyz', 'w')
    f.truncate()
    for str_temp in strs:
        f.write(str_temp)
    f = open('out.xyz', 'w')
    f.truncate()
    f.close()

def saveToXYZ2():
    f = open('xyzs2/out0' + '.xyz', 'a')
    # f.truncate()
    number=14
    f.write(str(number)+"\n")
    f.write("SLF"+ "\n")
    for i in range(number):
        xyz=get_atom_by_id(i+1)
        f.write("C"+" "+xyz[2]+" "+xyz[3]+" "+xyz[4]+"\n")
    f.truncate()
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
    s = os.popen("lmp_mpi <lammps.in")
    info = s.readlines()
    s.close()
    # print "-------输出焓--------"
    tag = 0
    for line in info:  # 按行遍历
        line = line.strip('\r\n')
        if (tag == 1):
            # print "energy: "+line
            return line
        if (line == "enthalpy"):
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

def get_atom_by_id_and_name(id,name):
    f = open(name)
    strs = f.readlines()
    f.close()
    pattern = re.compile(r'\S+')
    xyz = re.findall(pattern, strs[id+11])
    return xyz

def change_atom_by_id(id):
    step=0.1
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
#
def get_atom_change_direction(num,id,weightsArr,directionsArr):
    # 八个方向的向量空间
    randomArr=random_weight(id,weightsArr[id-1],num,directionsArr)
    return randomArr

def random_weight(id,weightsArrById,num,directionsArr):
    weightList=[]
    for i in range(len(weightsArrById)):
        # 用 UCB公式的变种计算权值
        k=1
        weightList.append(weightsArrById[i]+k*math.sqrt(1/directionsArr[id-1][i]))    # 权重求和
    total = 0
    # id-1是因为编号是从1开始的
    for i in range(len(weightList)):
        total = total + weightList[i]   # 权重求和
    ret = []
    keys = [1,2,3,4,5,6,7,8]
    while len(ret)<num:
        ra = random.uniform(0, total)  # 在0与权重和之前获取一个随机数
        curr_sum = 0
        for k in keys:
            curr_sum += weightList[k - 1]  # 在遍历中，累加当前权重值
            if ra <= curr_sum:  # 当随机数<=当前权重和时，返回权重key
                if(k not in ret):
                    ret.append(k)
                break
    return ret

def change_atom_by_id_and_direction(id,direction):
    step=0.1
    # print "-------更改原子:"+str(id)+"--------"
    strs=get_coo()
    xyz=get_atom_by_id(id)
    x_step = 0
    y_step = 0
    z_step = 0
    if direction==1:
        x_step = random.uniform(0, step)
        y_step = random.uniform(0, step)
        z_step = random.uniform(0, step)
    if direction==2:
        x_step = random.uniform(-step, 0)
        y_step = random.uniform(0, step)
        z_step = random.uniform(0, step)
    if direction==3:
        x_step = random.uniform(0, step)
        y_step = random.uniform(-step, 0)
        z_step = random.uniform(0, step)
    if direction==4:
        x_step = random.uniform(0, step)
        y_step = random.uniform(0, step)
        z_step = random.uniform(-step, 0)
    if direction==5:
        x_step = random.uniform(-step, 0)
        y_step = random.uniform(-step, 0)
        z_step = random.uniform(0, step)
    if direction==6:
        x_step = random.uniform(-step, 0)
        y_step = random.uniform(0, step)
        z_step = random.uniform(-step, 0)
    if direction==7:
        x_step = random.uniform(0, step)
        y_step = random.uniform(-step, 0)
        z_step = random.uniform(-step, 0)
    if direction==8:
        x_step = random.uniform(-step, 0)
        y_step = random.uniform(-step, 0)
        z_step = random.uniform(-step, 0)
    x=float(xyz[2])+float(x_step)
    y = float(xyz[3]) + float(y_step)
    z = float(xyz[4]) + float(z_step)
    strs[id+11]=str(id)+" "+"1"+" "+str(x)+" "+str(y)+" "+str(z)+"\n"
    set_coo(strs)

def find_direction_by_two_point(xyz_init,xyz_final):
    direction=0
    if float(xyz_final[0]) - float(xyz_init[0]) > 0 and float(xyz_final[1]) - float(xyz_init[1]) > 0 and float(
            xyz_final[2]) - float(xyz_init[2]) > 0:
        direction=1
    if float(xyz_final[0]) - float(xyz_init[0]) < 0 and float(xyz_final[1]) - float(xyz_init[1]) > 0 and float(
            xyz_final[2]) - float(xyz_init[2]) > 0:
        direction=2
    if float(xyz_final[0]) - float(xyz_init[0]) > 0 and float(xyz_final[1]) - float(xyz_init[1]) < 0 and float(
            xyz_final[2]) - float(xyz_init[2]) > 0:
        direction=3
    if float(xyz_final[0]) - float(xyz_init[0]) > 0 and float(xyz_final[1]) - float(xyz_init[1]) > 0 and float(
            xyz_final[2]) - float(xyz_init[2]) < 0:
        direction=4
    if float(xyz_final[0]) - float(xyz_init[0]) < 0 and float(xyz_final[1]) - float(xyz_init[1]) < 0 and float(
            xyz_final[2]) - float(xyz_init[2]) > 0:
        direction=5
    if float(xyz_final[0]) - float(xyz_init[0]) < 0 and float(xyz_final[1]) - float(xyz_init[1]) > 0 and float(
            xyz_final[2]) - float(xyz_init[2]) < 0:
        direction=6
    if float(xyz_final[0]) - float(xyz_init[0]) > 0 and float(xyz_final[1]) - float(xyz_init[1]) < 0 and float(
            xyz_final[2]) - float(xyz_init[2]) < 0:
        direction=7
    if float(xyz_final[0]) - float(xyz_init[0]) < 0 and float(xyz_final[1]) - float(xyz_init[1]) < 0 and float(
            xyz_final[2]) - float(xyz_init[2]) < 0:
        direction=8
    direction_length=abs(float(xyz_final[0]) - float(xyz_init[0]))+abs(float(xyz_final[1]) - float(xyz_init[1]))+abs(float(xyz_final[2]) - float(xyz_init[2]))
    return direction,direction_length

def find_direction_value(init_point_list):
    directions=[]
    direction_lengths=[]
    for i in init_point_list:
        xyz_init = get_atom_by_id_and_name(i,'coo_init')
        xyz_final = get_atom_by_id_and_name(i,'coo_final')
        direction, direction_length=find_direction_by_two_point(xyz_init[2:], xyz_final[2:])
        # 保存方向
        directions.append(direction)
        direction_lengths.append(direction_length)
    return directions,direction_lengths

def out_directionsArr(directionsArr):
    f = open('directionsArr.txt', 'a')
    for str_temp in directionsArr:
        for i in str_temp:
            f.write(str(i)+",")
        f.write("\n")
    f.write("----------------------------------------" + "\n")
    f.close()
def out_weightsArr(weightsArr):
    f = open('weightsArr.txt', 'a')
    for str_temp in weightsArr:
        for i in str_temp:
            f.write(str(i)+",")
        f.write("\n")
    f.write("----------------------------------------"+"\n")
    f.close()

def run_one_step(weightsArr,directionsArr):
    # 一些初始化操作
    initDeal()
    # 初始化最大值
    total_max=get_enthalpy()
    print "初始能量是: "+total_max
    # get_atoms()
    # 选择所有原子
    init_point_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    choose_list = [1,2,3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # 一个元素选中后多少次以后才能被重新选中
    unpickTime = 6
    q = Queue.Queue(maxsize = unpickTime)
    not_better_length=0
    run_length=0
    # 若20步找不到更优解(更低能量)则停止
    while not_better_length<20:
        not_better_length=not_better_length+1
        run_length=run_length+1
        print "循环进行到: "+str(run_length)+"  连续未找到更优解的长度为: "+str(not_better_length)
        # 保存开始的值
        initStr = get_coo()
        # 保存中间的值
        tempStr = get_coo()
        # 选择这次要操作的值,并且把它从候选list移除加入休息队列
        id = choice(choose_list)
        choose_list.remove(id)
        if(q.full()):
            choose_list.append(q.get())
        q.put(id)
        print id
        # 设置暂时的最大值
        temp_max=10000
        # 保存xyz,为了得到xyz文件来动画显示
        saveToXYZ2()
        # 获得要变的atom方向,参数是返回几个方向
        directionArr=get_atom_change_direction(4,id,weightsArr,directionsArr)
        # 最终走的方向
        temp_direction=0
        # 开始改这个c原子的坐标, 每次都往八个方向里按权重随机选四个方向
        for direction in directionArr:
            # 先设为初始位置
            set_coo(initStr)
            #  改atom的位置
            change_atom_by_id_and_direction(id, direction)
            f = get_enthalpy()
            # print f
            if float(f) < temp_max:
                # 保存较大的值以及此时的str(位置)以及此时走的方向(direction)
                temp_max = float(f)
                tempStr = get_coo()
                temp_direction=direction
                if float(f) < total_max:
                    total_max = float(f)
                    saveToFinal()
                    not_better_length = 0
                    print "在" + str(direction) + " 方向留下改变" + "此时能量为: " + get_enthalpy()
        # 选择这一步走
        set_coo(tempStr)
        # 给走的方向加一次 -1是因为从1开始
        directionsArr[id-1][temp_direction-1]=directionsArr[id-1][temp_direction-1]+1
        print str(id)+"的方向"+str(temp_direction)+"加1,变为: "+str(directionsArr[id-1][temp_direction-1])
    #更新weight值
    directions,direction_lengths=find_direction_value(init_point_list)
    for i in range(len(directions)):
        weightsArr[i][directions[i]-1]=round(weightsArr[i][directions[i]-1]+direction_lengths[i],3)

def main():
    # 一些初始化操作
    # initDeal()
    # 计算时间用
    start = time.clock()
    # 设置权值
    weightsArr=numpy.ones([14,8])
    # 每个方向走的次数
    directionsArr = numpy.ones([14, 8])
    # 开始计算
    for i in range(20):
        print '.................'+str(i)+'........................'
        run_one_step(weightsArr,directionsArr)
        out_weightsArr(weightsArr)
        out_directionsArr(directionsArr)

    # 显示用时
    elapsed = (time.clock() - start)
    print("Time used:", elapsed)
main()