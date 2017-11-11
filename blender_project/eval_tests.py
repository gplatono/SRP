import re
import subprocess
import os
import sys
import numpy as np
import math

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
yn_to_index = {"yes": 4, "rather yes": 3, "uncertain": 2, "rather no": 1, "no": 0}
rel_to_index = {"right": 0, "left": 1, "in front of": 2, "behind": 3, "above": 4, "below": 5, "over": 6, "under": 7, "in": 8, "on": 9, "at": 10, "touching": 11, "between": 12, "near": 13}
        
def map_response_to_index(resp):
    for key in rel_to_index:
        if key in resp:
            return rel_to_index[key]
    return -1

def weighted_cohen_kappa(resp1, resp2):
    #print (resp1, resp2)
    weights = np.zeros((5,5))
    for i in range(weights.shape[0]):
        for j in range(weights.shape[1]):
            weights[i][j] = abs(i - j)
    y1 = []
    y2 = []
    for testcase in resp1:
        if testcase in resp2:
            y1 += [resp1[testcase]]
            y2 += [resp2[testcase]]
    #print (y1, y2)
    y1 = [yn_to_index[y] for y in y1]
    y2 = [yn_to_index[y] for y in y2]

    if len(y1) > 0 and len(y2) > 0:
        resp_distr = np.zeros((5, 5))
        for i in range(len(y1)):
            resp_distr[y1[i]][y2[i]] += 1
        total_resp = np.sum(resp_distr)
        observed_agreement = sum([resp_distr[i][i] for i in range(resp_distr.shape[0])]) * 1.0
        observed_agreement /= total_resp
        total_coincidence = 1.0 * sum([np.sum(resp_distr[i:]) * np.sum(resp_distr[:i]) for i in range(resp_distr.shape[0])])
        total_coincidence /= total_resp * total_resp
        kappa = (observed_agreement - total_coincidence) / (1 - total_coincidence)
        print (resp_distr, total_resp, total_coincidence, observed_agreement, kappa)

def cohen_kappa(resp1, resp2):
    y1 = []
    y2 = []
    for testcase in resp1:
        if testcase in resp2:
            y1 += [resp1[testcase]]
            y2 += [resp2[testcase]]
    y1 = [rel_to_index[y] for y in y1]
    y2 = [rel_to_index[y] for y in y2]

    if len(y1) > 0 and len(y2) > 0:
        resp_distr = np.zeros((13, 13))
        for i in range(len(y1)):
            resp_distr[y1[i]][y2[i]] += 1
        total_resp = np.sum(resp_distr)
        observed_agreement = sum([resp_distr[i][i] for i in range(resp_distr.shape[0])]) * 1.0
        observed_agreement /= total_resp
        total_coincidence = 1.0 * sum([np.sum(resp_distr[i:]) * np.sum(resp_distr[:i]) for i in range(resp_distr.shape[0])])
        total_coincidence /= total_resp * total_resp
        kappa = (observed_agreement - total_coincidence) / (1 - total_coincidence)
        print (resp_distr, total_resp, total_coincidence, observed_agreement, kappa)        


tests = []
count = 0
trc = 0
desc = 0
dict = {}
dict["1"] = 0
dict["0"] = 0
tcounts = {}
ur_yn = {}
ur_relations = {}
system_yn = {}
for subm in open('annotations').readlines():
#    print (subm)
    subm = subm.strip().split(":")
#    print (subm)
    testcase = subm[1].split("=")[1]
    user = subm[2].split("=")[1]
    scene_path = subm[4].split("=")[1]
    relation = subm[5].split("=")[1]
    relatum = subm[6].split("=")[1]
    referent1 = subm[7].split("=")[1]
    referent2 = subm[8].split("=")[1]
    task_type = subm[9].split("=")[1]
    resp = subm[10].split("=")[1].lower()
    if user not in ur_yn:
        ur_yn[user] = {}
    if user not in ur_relations:
        ur_relations[user] = {}    
    resp_code = map_response_to_index(resp)
#    print ("RESP_CODE:", resp_code)
    if resp_code != -1:
        ur_relations[user][testcase] = resp_code
    else:
        ur_yn[user][testcase] = resp#yn_to_index[resp]
    tests += [[scene_path, relation, relatum, referent1, referent2, task_type, resp]]

    
    if task_type == "0" and (relation == "to the left of" or relation == "to the right of"):
        print ("ID:", subm[0].split("=")[1])
        #subprocess.call(["blender", test[0], "--background", "--python", "main.py", "--", test[1], test[2], test[3], test[4], test[5], test[6]])
        res = subprocess.check_output(["blender", scene_path, "--background", "--python", "main.py", "--", relation, relatum, referent1, referent2, task_type, resp])
        res = res.decode("utf-8").split("\n")
        print (res)
        for item in res:
            if "RESULT" in item:
                res = item.split(":")[1]
                break
        res = float(res)
        res = math.floor(5 * res)
        print ("RESULT:", res, "USER RESULT:", ur_yn[user][testcase])
        system_yn[testcase] = res

for user in ur_yn:
    print (weighted_cohen_kappa(ur_yn[user], system_yn))
        
#Interannotator agreement
'''print(ur_yn.keys())
keys = [key for key in iter(ur_yn)]
for us1 in range(len(keys)):
    for us2 in range(us1, len(keys)):
        if us1 != us2:            
            weighted_cohen_kappa(ur_yn[keys[us1]], ur_yn[keys[us2]])
'''         
desc_corr = 0
total_succ = 0
print ("description task resp:", dict["1"], "\ntruth judgment task resp:", dict["0"], "\n# of responses:", len(tests), count, "testcases: ", len(tcounts))
'''for test in tests:
    print (test)
    if test[5] == "0" and (test[1] == "to the left of" or test[1] == "to the right of"):
        #subprocess.call(["blender", test[0], "--background", "--python", "main.py", "--", test[1], test[2], test[3], test[4], test[5], test[6]])
        res = subprocess.check_output(["blender", test[0], "--background", "--python", "main.py", "--", test[1], test[2], test[3], test[4], test[5], test[6]])
        res = res.decode("utf-8").split("\n")
        print (res)
        for item in res:
            if "RESULT" in item:
                res = item.split(":")[1]
                break
        print (res)
        
        if res == " True" or res == " False":
            total_succ += 1
            if res == " True":
                desc_corr += 1
            print ("TEST RESULT:", test[2], res, desc_corr, 100.0 * desc_corr / total_succ)
'''
