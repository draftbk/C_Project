# -*- coding:utf-8 -*-
import os
import matplotlib.pyplot as plt

def drawLineText(dir):
    x=[]
    y1=[]
    y2=[]
    y=[]
    f = open(dir+'/'+'energy')
    strs = f.readlines()
    j = 0
    for str in strs:
        print str
        for i in str.split(","):
            if j==0:
                y1.append(float(i))
            if j==1:
                y2.append(float(i))
        j=j+1
    f.close()

    for i in range(len(y1)):
        y.append(y2[i])
        y.append(y1[i])
        x.append(i*2)
        x.append(i * 2+1)
    plt.figure(figsize=(8, 4))  # 创建绘图对象
    plt.plot(x, y, "r--", linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.xlabel("Time(s)")  # X轴标签
    plt.ylabel("Energy")  # Y轴标签
    plt.title("energy line")  # 图标题
    plt.savefig("Figure_1.png")


def drawLineText_front(number,dir):
    x=[]
    y1=[]
    y2=[]
    y=[]
    f = open(dir + '/' + 'energy')
    strs = f.readlines()
    j = 0
    for str in strs:
        print str
        for i in str.split(","):
            if j==0:
                y1.append(float(i))
            if j==1:
                y2.append(float(i))
        j=j+1
    f.close()

    for i in range(number):
        y.append(y2[i])
        y.append(y1[i])
        x.append(i*2)
        x.append(i * 2+1)
    plt.figure(figsize=(8, 4))  # 创建绘图对象
    plt.plot(x, y, "r--", linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.xlabel("Time(s)")  # X轴标签
    plt.ylabel("Energy")  # Y轴标签
    plt.title("energy line")  # 图标题
    plt.savefig("Figure_2.png")


def main(name):
    dir="../Data_Saving/"+name
    drawLineText(dir)
    drawLineText_front(10,dir)
    print os.popen("cp -R Figure_1.png " + dir)
    print os.popen("cp -R Figure_2.png " + dir)

for i in range(1,6):
    main(str(i))