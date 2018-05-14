def updateXYZ(s):
    f = open(s)
    strs = f.readlines()
    strs[1]="SLF\n"
    for i in range(len(strs)):
        if(i>1):
          strs[i]="C"+strs[i][1:]
    f = open(s, 'w')
    for str_temp in strs:
        f.write(str_temp)
    f.truncate()
    f.close()


for i in range(200):
  f = updateXYZ('xyzs/out' + str(i) + '.xyz')
