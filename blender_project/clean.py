import re
import subprocess
import os
import sys

filepath = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, filepath)

from parser import *

relations = ["right of ", "left of ", "in front of ", "behind ", "above ", "below ", "between ", "touching ", "over ", "under ", "at ", "on ", "near "]
out=open("annotations", "w")
tests = []
count = 0
dict = {}
for subm in open('dump').read().split('###'):
    subm = subm.strip().lower().split(':')
    if len(subm) >= 11:
        if subm[9] == '1':
            scene_file = "description/" + subm[4].split(".")[0] + ".blend"
        else:
            scene_file = "truth_judgment/" + subm[4].split(".")[0] + ".blend"
        if subm[1] not in dict:
                dict[subm[1]] = 0
        for resp in subm[10].split('\n'):
            rcount = sum([1 for rel in relations if rel in resp])
            if subm[2] != "1" and rcount <= 1 and "close " not in resp and "be the" not in resp and "by " not in resp and "next to" not in resp and any(char.isdigit() for char in resp) == False and ("between " in resp or " and " not in resp):
                str = "id=" + subm[0] + ":testcase=" + subm[1] + ":user_id=" + subm[2] + ":scene_id=" + subm[3] + ":scene_path=" + scene_file + ":relation=" + subm[5] + ":relatum=" + subm[6] + ":referent1=" + subm[7] + ":referent2=" + subm[8] + ":task_type=" + subm[9] + ":response=" + resp             
                str = str.replace("cube", "block")
#            else:                
 #               print (resp, rcount)
                #if len(resp) > 9:
                #    print (resp," ", scene_file, subm[6])
                print(str, file=out)                
                count += 1
print (count)
