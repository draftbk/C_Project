# -*- coding:utf-8 -*-
import os
import re
import random
import time
from random import choice
import shutil
import Queue




def initDeal():
    # 清空roads文件夹
    shutil.rmtree('roads')
    os.mkdir('roads')
    # 清空xyzs文件夹
    shutil.rmtree('xyzs')
    os.mkdir('xyzs')
    # 清空log_road
    f = open('log_road', 'w')
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

def saveToXYZ2(i):
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
    s = os.popen("lmp_mpi <lammps.in")
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

def change_atom_by_id(id):
    step=0.5
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

def change_other_atom_by_id(id):
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

# def drawLine(x,y):
#     plt.figure(figsize=(8, 4))  # 创建绘图对象
#     plt.plot(x, y, "b--", linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
#     plt.xlabel("Time(s)")  # X轴标签
#     plt.ylabel("Energy")  # Y轴标签
#     plt.title("energy line")  # 图标题
#     plt.show()  # 显示图
#     plt.savefig("energy_line.jpg")  # 保存图

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

def main():
    atomNumber=256
    # 一些初始化操作
    initDeal()
    # 初始化log_roads,保存到log_road里
    log_roads=[]
    # 计算时间用
    start = time.clock()
    # 初始化最大值
    total_max=get_enthalpy()
    print "初始能量是: "+total_max
    # get_atoms()
    choose_list=[]
    for i in range(atomNumber):
        choose_list.append(i+1)
    # 一个元素选中后多少次以后才能被重新选中
    unpickTime = 10
    q = Queue.Queue(maxsize = unpickTime)
    not_better_length=0
    total_length=0
    # 初始化折线图的xy
    x = []
    y = []
    y1=[]
    y2=[]
    while not_better_length < 50:
        print y
        print y1
        print y2
        not_better_length=not_better_length+1
        total_length=total_length+1
        print "循环进行到: " + str(total_length) + "  连续未找到更优解的长度为: " + str(not_better_length)
        initStr = get_coo()
        tempStr = get_coo()
        id = choice(choose_list)
        choose_list.remove(id)
        if(q.full()):
            choose_list.append(q.get())
        q.put(id)
        print id
        temp_max=10000
        # 把现在文件状态保存到roads文件夹
        saveToRoad(total_length)
        # 保存x,y
        # x.append(total_length)
        y.append(get_enthalpy())
        e_0,e_after=get_0_and_after_enthalpy()
        y1.append(e_0)
        y2.append(e_after)
        # 把现在xyz文件保存到xyzs文件夹
        saveToXYZ(total_length)
        # saveToXYZ2(i)
        # 保存每步改了什么_start
        start_road_temp=get_atom_by_id(id)
        start_road_temp_str=start_road_temp[2]+","+start_road_temp[3]+","+start_road_temp[4]
        for j in range(15):
          change_atom_by_id(id)
          for x in range(atomNumber):
              if x is not id:
                  change_other_atom_by_id(id)
          f=get_enthalpy()
          # print f
          if float(f)<temp_max:
              temp_max=float(f)
              tempStr=get_coo_after_optimization(atomNumber)
              if float(f)<total_max:
                  total_max=float(f)
                  saveToFinal()
                  not_better_length=0
                  print "留下改变" + "此时能量为: " + get_enthalpy()
          set_coo(initStr)
        set_coo(tempStr)
        # 保存每步改了什么_end
        end_road_temp = get_atom_by_id(id)
        end_road_temp_str = end_road_temp[2] + "," + end_road_temp[3] + "," + end_road_temp[4]
        log_roads.append(str(id)+"号原子坐标 from " +start_road_temp_str+" to "+end_road_temp_str+"\n")
    print get_enthalpy()
    print y
    print "[",
    for i in y:
        print i + ",",
    print "]"
    print x
    # drawLine(x,y)
    saveToRoadLog(log_roads)
    elapsed = (time.clock() - start)
    print("Time used:", elapsed)

main()