# -*- coding:utf-8 -*-
import os
import re
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

def get_xyz_after_optimization(lastNUmber):
    f = open('xyzs2/out45.xyz')
    strs = f.readlines()
    f.close()

    pattern = re.compile(r'\S+')
    xyzs=[]
    for i in strs[-lastNUmber:]:
        xyz = re.findall(pattern, i)
        xyzs.append("1"+" "+xyz[1] + " " + xyz[2] + " " + xyz[3])

    f = open('xyzs2/coo_45.xyz', 'w')
    f.truncate()
    f.write("256\nAtoms. Timestep: 0\n")
    for str_temp in xyzs:
        f.write(str_temp+"\n")
    f.close()

    return xyzs

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

def out_x(n):
    print "[",
    for i in range(n):
        print str(i)+",",
    print "]"

def out_y(arrs):
    print "[",
    for i in arrs:
        print i+",",
    print "]"

get_xyz_after_optimization(256)