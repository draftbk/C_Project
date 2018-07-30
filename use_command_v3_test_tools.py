# -*- coding:utf-8 -*-
import os
import re
import random
import time
from random import choice
import shutil
import math
import Queue
from termcolor import *
import numpy
import matplotlib.pyplot as plt


def get_atom_by_id_and_name(id,name):
    f = open(name)
    strs = f.readlines()
    f.close()
    pattern = re.compile(r'\S+')
    xyz = re.findall(pattern, strs[id+11])
    return xyz

def find_direction_smalldirection_by_two_point(i,xyz_init,xyz_best):
    direction = 0
    direction_small = 0
    # 输出位置变动
    # print str(i)+","+str(float(xyz_best[0]) - float(xyz_init[0]))+","+str(float(xyz_best[1]) - float(xyz_init[1]))+","+str(float(xyz_best[2]) - float(xyz_init[2]))
    print str(i) + "," + str(round((float(xyz_best[0]) - float(xyz_init[0])) / 0.386,2)) + "," + str(round((float(xyz_best[1]) - float(xyz_init[1])) / 0.386,2)
        ) + "," + str(round((float(xyz_best[2]) - float(xyz_init[2])) / 0.386,2))
    # 输出在哪个象限
    if float(xyz_best[0]) - float(xyz_init[0]) > 0 and float(xyz_best[1]) - float(xyz_init[1]) > 0 and float(
            xyz_best[2]) - float(xyz_init[2]) > 0:
        direction = 1
    if float(xyz_best[0]) - float(xyz_init[0]) < 0 and float(xyz_best[1]) - float(xyz_init[1]) > 0 and float(
            xyz_best[2]) - float(xyz_init[2]) > 0:
        direction = 2
    if float(xyz_best[0]) - float(xyz_init[0]) > 0 and float(xyz_best[1]) - float(xyz_init[1]) < 0 and float(
            xyz_best[2]) - float(xyz_init[2]) > 0:
        direction = 3
    if float(xyz_best[0]) - float(xyz_init[0]) > 0 and float(xyz_best[1]) - float(xyz_init[1]) > 0 and float(
            xyz_best[2]) - float(xyz_init[2]) < 0:
        direction = 4
    if float(xyz_best[0]) - float(xyz_init[0]) < 0 and float(xyz_best[1]) - float(xyz_init[1]) < 0 and float(
            xyz_best[2]) - float(xyz_init[2]) > 0:
        direction = 5
    if float(xyz_best[0]) - float(xyz_init[0]) < 0 and float(xyz_best[1]) - float(xyz_init[1]) > 0 and float(
            xyz_best[2]) - float(xyz_init[2]) < 0:
        direction = 6
    if float(xyz_best[0]) - float(xyz_init[0]) > 0 and float(xyz_best[1]) - float(xyz_init[1]) < 0 and float(
            xyz_best[2]) - float(xyz_init[2]) < 0:
        direction = 7
    if float(xyz_best[0]) - float(xyz_init[0]) < 0 and float(xyz_best[1]) - float(xyz_init[1]) < 0 and float(
            xyz_best[2]) - float(xyz_init[2]) < 0:
        direction = 8
    k=0.4
    # 输出在哪个小象限
    if abs(float(xyz_best[0]) - float(xyz_init[0])) > k and abs(float(xyz_best[1]) - float(xyz_init[1])) > k and abs(
                    float(xyz_best[2]) - float(xyz_init[2])) > k:
        direction_small = 1
    if abs(float(xyz_best[0]) - float(xyz_init[0])) <= k and abs(float(xyz_best[1]) - float(xyz_init[1])) > k and abs(
                    float(xyz_best[2]) - float(xyz_init[2])) > k:
        direction_small = 2
    if abs(float(xyz_best[0]) - float(xyz_init[0])) > k and abs(float(xyz_best[1]) - float(xyz_init[1])) <= k and abs(
                    float(xyz_best[2]) - float(xyz_init[2])) > k:
        direction_small = 3
    if abs(float(xyz_best[0]) - float(xyz_init[0])) > k and abs(float(xyz_best[1]) - float(xyz_init[1])) > k and abs(
                    float(xyz_best[2]) - float(xyz_init[2])) <= k:
        direction_small = 4
    if abs(float(xyz_best[0]) - float(xyz_init[0])) <= k and abs(float(xyz_best[1]) - float(xyz_init[1])) <= k and abs(
                    float(xyz_best[2]) - float(xyz_init[2])) > k:
        direction_small = 5
    if abs(float(xyz_best[0]) - float(xyz_init[0])) <= k and abs(float(xyz_best[1]) - float(xyz_init[1])) > k and abs(
                    float(xyz_best[2]) - float(xyz_init[2])) <= k:
        direction_small = 6
    if abs(float(xyz_best[0]) - float(xyz_init[0])) > k and abs(float(xyz_best[1]) - float(xyz_init[1])) <= k and abs(
                    float(xyz_best[2]) - float(xyz_init[2])) <= k:
        direction_small = 7
    if abs(float(xyz_best[0]) - float(xyz_init[0])) <= k and abs(float(xyz_best[1]) - float(xyz_init[1])) <= k and abs(
                    float(xyz_best[2]) - float(xyz_init[2])) <= k:
        direction_small = 8
    return direction, direction_small


def find_direction_smalldirection(init_point_list):
    directions = []
    direction_smalls = []
    for i in init_point_list:
        xyz_init = get_atom_by_id_and_name(i,'coo_init')
        xyz_best = get_atom_by_id_and_name(i,'coo_-156')
        direction, direction_small=find_direction_smalldirection_by_two_point(i,xyz_init[2:], xyz_best[2:])
        # 保存方向
        directions.append(direction)
        direction_smalls.append(direction_small)
    return directions, direction_smalls

def change_to_form():
    f = open('init_coo_opted4')
    strs = f.readlines()
    f.close()
    pattern = re.compile(r'\S+')
    j=0
    for i in strs:
        j=j+1
        xyz = re.findall(pattern, i)
        print str(j)+" "+"1"+" "+xyz[0]+" "+xyz[1]+" "+xyz[2]

def change_to_form2():
    f = open('out_before_transfer.txt')
    strs = f.readlines()
    f.close()
    pattern = re.compile(r'\S+')
    j=0
    for i in strs:
        j=j+1
        if j > 2:
            xyz = re.findall(pattern, i)
            print str(j-2)+" "+"1"+" "+xyz[1]+" "+xyz[2]+" "+xyz[3]

def drawLineText():
    x=[ ]
    y=['-832.96909', '-1019.2499', '-1129.0721', '-1215.433', '-1264.2686', '-1293.0325', '-1310.3575', '-1324.9266', '-1333.7545', '-1340.2927', '-1344.7617', '-1348.8601', '-1352.8911', '-1356.3862', '-1358.9189', '-1360.5536', '-1362.2869', '-1363.5301', '-1364.5607', '-1365.391', '-1366.2816', '-1367.118', '-1367.8296', '-1368.3546', '-1368.7009', '-1369.1273', '-1369.4986', '-1369.7982', '-1370.2542', '-1370.6496', '-1370.9252', '-1371.2637', '-1371.629', '-1371.8541', '-1372', '-1372.0909', '-1372.4939', '-1372.7242', '-1372.9066', '-1373.4434', '-1373.4032', '-1373.3526', '-1373.3895', '-1373.4911', '-1373.6843', '-1373.8458', '-1373.7604', '-1373.9205', '-1373.9435', '-1374.158', '-1374.3435', '-1374.5083', '-1374.5122', '-1374.5813', '-1374.488', '-1374.441', '-1374.516', '-1374.5557', '-1374.6206', '-1374.8058', '-1374.9164', '-1375.0631', '-1375.0266', '-1375.1411', '-1375.1238', '-1375.3447', '-1375.4454', '-1375.4088', '-1375.5053', '-1375.7474', '-1375.7073', '-1375.8649', '-1375.719', '-1375.73', '-1375.7992', '-1375.8062', '-1375.7943', '-1375.992', '-1376.0754', '-1376.2138', '-1376.2602', '-1376.2661', '-1376.0874', '-1376.1506', '-1376.2089', '-1376.2656', '-1376.4274', '-1376.4918', '-1376.3835', '-1376.3568', '-1376.4318', '-1376.6368', '-1376.6135', '-1376.5794', '-1376.7839', '-1376.7133', '-1376.7512', '-1376.7123', '-1376.8208', '-1376.7681', '-1376.7571', '-1376.8553', '-1376.8799', '-1376.9863', '-1377.0046', '-1376.9397', '-1376.8682', '-1376.9034', '-1376.8333', '-1376.8658', '-1376.854', '-1377.0753', '-1377.162', '-1377.0767', '-1377.1521', '-1377.1086', '-1377.0143', '-1376.9984', '-1377.2397', '-1377.331', '-1377.1392', '-1380.3563', '-1380.7707', '-1381.0639', '-1381.225', '-1381.1114', '-1381.3268', '-1381.2708', '-1381.1107', '-1381.1434', '-1381.3451', '-1381.3746', '-1381.4452', '-1381.5156', '-1381.7056', '-1381.5856', '-1381.5414', '-1381.4475', '-1381.3725', '-1381.3245', '-1381.2302', '-1381.4258', '-1381.4339', '-1381.5135', '-1381.5851', '-1381.5408', '-1381.6092', '-1381.5424', '-1381.7383', '-1381.6433', '-1381.6775', '-1381.5823']
    y1 = ['-469.94839', '-833.88651', '-1024.4167', '-1130.4151', '-1216.5752', '-1264.6811', '-1293.5162', '-1310.7254', '-1324.7307', '-1333.7408', '-1339.753', '-1344.3644', '-1348.6009', '-1352.5815', '-1356.0471', '-1358.2153', '-1360.1455', '-1361.7307', '-1363.0837', '-1364.0824', '-1365.0773', '-1365.9206', '-1366.6735', '-1367.2914', '-1367.6698', '-1368.1287', '-1368.6069', '-1368.8987', '-1369.4173', '-1369.7784', '-1370.0893', '-1370.4273', '-1370.7629', '-1370.9314', '-1371.2309', '-1371.3427', '-1371.8609', '-1372.007', '-1372.2611', '-1372.7812', '-1372.7505', '-1372.6889', '-1372.7851', '-1372.824', '-1373.0764', '-1373.0932', '-1373.0653', '-1373.2915', '-1373.3724', '-1373.5091', '-1373.7626', '-1373.8177', '-1373.9113', '-1373.9915', '-1373.8739', '-1373.8332', '-1373.8302', '-1373.9326', '-1373.9924', '-1374.1609', '-1374.2963', '-1374.5029', '-1374.4571', '-1374.5458', '-1374.5092', '-1374.6531', '-1374.8032', '-1374.7678', '-1374.8604', '-1375.0629', '-1375.1053', '-1375.2572', '-1375.1536', '-1375.2097', '-1375.1589', '-1375.1554', '-1375.2256', '-1375.4385', '-1375.4565', '-1375.6165', '-1375.6216', '-1375.5941', '-1375.503', '-1375.6258', '-1375.6506', '-1375.6737', '-1375.8597', '-1375.8251', '-1375.7698', '-1375.7204', '-1375.7486', '-1375.9561', '-1375.9507', '-1375.9101', '-1376.1924', '-1376.1871', '-1376.1303', '-1376.1849', '-1376.1565', '-1376.1471', '-1376.1889', '-1376.2402', '-1376.2653', '-1376.434', '-1376.3774', '-1376.3149', '-1376.2547', '-1376.237', '-1376.2068', '-1376.2811', '-1376.1853', '-1376.4563', '-1376.539', '-1376.4997', '-1376.5064', '-1376.4751', '-1376.3893', '-1376.4173', '-1376.6685', '-1376.6694', '-1376.5232', '-1379.0317', '-1380.0279', '-1380.3522', '-1380.5911', '-1380.5026', '-1380.6374', '-1380.6132', '-1380.4854', '-1380.5003', '-1380.7425', '-1380.642', '-1380.8251', '-1380.867', '-1381.0311', '-1381.0178', '-1380.9207', '-1380.8522', '-1380.7626', '-1380.8036', '-1380.7336', '-1380.7681', '-1380.7738', '-1380.8836', '-1380.9776', '-1380.9866', '-1381.0784', '-1381.0149', '-1381.0947', '-1381.099', '-1381.0629', '-1380.9585']
    y2=[]
    for i in range(50):
        y2.append(float(y[i]))
        y2.append(float(y1[i]))
        y[i]=float(y[i])
        y1[i] = float(y1[i])
        x.append(i*2)
        x.append(i * 2+1)

    plt.figure(figsize=(8, 4))  # 创建绘图对象
    plt.plot(x, y2, "r--", linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.xlabel("Time(s)")  # X轴标签
    plt.ylabel("Energy")  # Y轴标签
    plt.title("energy line")  # 图标题
    plt.show()  # 显示图

def get_xyz_after_optimization(lastNUmber):
    f = open('out.xyz')
    strs = f.readlines()
    f.close()
    j=0
    pattern = re.compile(r'\S+')
    for i in strs[-lastNUmber:]:
        j=j+1
        xyz = re.findall(pattern, i)
        print str(j) + " " + "1" + " " + xyz[1] + " " + xyz[2] + " " + xyz[3]



def main():
    # drawLineText()
    change_to_form2()
    # print "0"
    # init_point_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # find_direction_smalldirection(init_point_list)
    # print math.sqrt((4.186-6.996)*(4.186-6.996)+(5.118-7.764)*(5.118-7.764)+(6.729-6.781)*(6.729-6.781))
    print ""
    # get_xyz_after_optimization(256)

main()