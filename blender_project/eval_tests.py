import re
import subprocess
import os
import sys

filepath = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, filepath)

from parser import *

class Testcase:
    def __init__(self, scene_file, task_type, relation, relatum, referent1, referent2, response):
        self.scene_file = scene_file
        self.task_type = task_type
        self.relation = relation
        self.relatum = relatum
        self.referent1 = referent1
        self.referent2 = referent2
        self.response = response

tests = []
count = 0
dict = {}
for subm in open('dump').read().split('###'):
    subm = subm.strip().split(':')
    if len(subm) >= 11 and subm[9] == '1':
        if subm[9] == '1':
            scene_file = "description/" + subm[4].split(".")[0] + ".blend"
        else:
            scene_file = "truth_judgment/" + subm[4].split(".")[0] + ".blend"
        if subm[1] not in dict:
                dict[subm[1]] = 0
        for resp in subm[10].split('\n'):
            dict[subm[1]] += 1
            tests += [[scene_file, subm[5], subm[6], subm[7], subm[8], subm[9], resp]]
            #response = [subm[6], resp]            
            count += 1

for test in tests:
    #parse(test[2])
    subprocess.call(["blender", test[0], "--background", "--python", "main.py", "--", test[1], test[2], test[3], test[4], test[5], test[6]])
    #res = subprocess.check_output(["blender", test[0], "--background", "--python", "main.py", "--", test[1], test[2]])
    #res = res.decode("utf-8").split("\n")
    #print (res)
