# -*- coding:utf-8 -*-
import math
#λ - >t1  μ -> t2 ζ-->t3 β -> t4 ñ -> t5
t1=3.4879
t2=2.2119
t4=1.5724*(10**-7)
t5=0.72751
A=1393.6
B=346.7
R=1.8
S=2.1
h=-0.57058
c=38049
d=4.384
atom_list=[]

# ---------------------公式-----------------------

# 计算 E
def get_E():
    temp_E=0
    # 因为是这样的没有重复的循环,所以不用乘 1/2
    for atom1 in atom_list:
        for atom2 in atom_list:
            temp_E=temp_E+get_V(atom1,atom2)
    return temp_E

# 计算 V
def get_V(atom1, atom2):
    fc=get_fc(atom1,atom2)
    fr=get_fr(atom1,atom2)
    b=get_b(atom1, atom2)
    fa=get_fa(atom1, atom2)
    temp_v=fc*(fr+b*fa)
    return temp_v

# 计算fr
def get_fr(atom1, atom2):
    r=get_r(atom1,atom2)
    temp_fr=A*math.exp(-t1*r)
    return temp_fr

# 计算 fa
def get_fa(atom1, atom2):
    r = get_r(atom1, atom2)
    temp_fa=-B*math.exp(-t2*r)
    return temp_fa

# 计算fc
def get_fc(i,j):
    r=get_r(i,j)
    if r<R:
        return 1
    if r>S:
        return 0
    else:
        return 0.5+0.5*math.cos(math.pi*(r-R)/(S-R))

# 计算b --?????
def get_b(atom1, atom2):
    x=1 # ----??????
    t3=get_t3()
    temp_b=x*((1+(t4**t5)*(t3**t5))**(-1/(2*t5)))
    return  temp_b

# 计算 ζ #---????????
def get_t3(atom1,atom2):
    temp_t3=0
    fc=get_fc(atom1,atom2)
    for atom3 in atom_list:
        rik=get_r(atom1,atom3)
        wik=1 #---????????
        g = get_g(atom1, atom2, atom3)
        temp_t3=temp_t3+fc*rik*wik*g
    return temp_t3

# 计算g
def get_g(i,j,k):
    # ij和ik的角度
    angle=get_angle(i,j,k)
    res=1+(c**2)/(d**2)-(c**2)/((d**2)+(h-math.cos(angle))**2)
    return res

# --------------------辅助方法---------------------

# 获得三个原子的角度
def get_angle(i, j, k):
    return 0


# 获得两原子距离
def get_r(i, j):
    return 0

def get_atom_list():
    return 0