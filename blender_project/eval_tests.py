import re
import subprocess
import os
import sys

filepath = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, filepath)

from parser import *

tests = []
count = 0
dict = {}
for subm in open('dump').read().split('###'):
    subm = subm.strip().split(':')
    if len(subm) >= 11 and subm[9] == '1':
        scene_file = "description/" + subm[4].split(".")[0] + ".blend"
        if subm[1] not in dict:
                dict[subm[1]] = 0
        for resp in subm[10].split('\n'):
            dict[subm[1]] += 1
            tests += [[scene_file, subm[6], resp]]
            #response = [subm[6], resp]            
            count += 1

for test in tests:
    #parse(test[2])
    subprocess.call(["blender", test[0], "--background", "--python", "main.py", "--", test[1], test[2]])
    #res = subprocess.check_output(["blender", test[0], "--background", "--python", "main.py", "--", test[1], test[2]])
    #res = res.decode("utf-8").split("\n")
    #print (res)
