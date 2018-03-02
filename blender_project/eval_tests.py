import re
import subprocess
import os
import sys
import numpy as np
import math

filepath = os.path.dirname(os.path.abspath(__file__))
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

#Dictionaries mapping the responses to numerical values
yn_to_index = {"yes": 4, "rather yes": 3, "uncertain": 2, "rather no": 1, "no": 0}
rel_to_index = {"right": 0, "left": 1, "in front of": 2, "behind": 3, "above": 4, "below": 5, "over": 6, "under": 7, "in": 8, "on": 9, "at": 10, "touching": 11, "between": 12, "near": 13}

rel_accuracy = {"right": [0,0], "left": [0,0], "front": [0,0], "behind": [0,0], "above": [0,0], "over": [0,0], "below": [0,0], "under": [0,0], "between": [0,0], "at": [0,0], "touching": [0,0], "near": [0,0], "in ": [0,0], "on ": [0, 0]}

#Maps the response to its numerical value
def map_response_to_index(resp):
    for key in rel_to_index:
        if key in resp:
            return rel_to_index[key]
    return -1

#Computes the weighted Cohen's Kappa interannotator agreement metric
#Inputs: resp1, resp2 - response sequences for two users
#Return value: the Kappa coefficient (from [0, 1])
def weighted_cohen_kappa(resp1, resp2):
    #print (resp1, resp2)
    weights = np.zeros((5,5))
    for i in range(weights.shape[0]):
        for j in range(weights.shape[1]):
            weights[i][j] = abs(i - j)
    y1 = [resp1[testcase] for testcase in resp1 if testcase in resp2]
    y2 = [resp2[testcase] for testcase in resp1 if testcase in resp2]

    #print (y1, y2)
    
    #y1 = []
    #y2 = []
    
    #for testcase in resp1:
    #    if testcase in resp2:
    #        y1 += [resp1[testcase]]
    #        y2 += [resp2[testcase]]
    
    #print (y1, y2)
    #y1 = [yn_to_index[y] for y in y1]
    #y2 = [yn_to_index[y] for y in y2]

    if len(y1) > 0 and len(y2) > 0:
        resp_distr = np.zeros((5, 5))
        for i in range(len(y1)):
            resp_distr[y1[i]][y2[i]] += 1
        total_resp = np.sum(resp_distr)
        observed_agreement = sum([resp_distr[i][i] for i in range(resp_distr.shape[0])]) * 1.0
        observed_agreement /= total_resp
        total_coincidence = 1.0 * sum([np.sum(resp_distr[i,:]) * np.sum(resp_distr[:,i]) for i in range(resp_distr.shape[0])])
        total_coincidence /= total_resp * total_resp
        kappa = (observed_agreement - total_coincidence) / (1 - total_coincidence)
        num = 0
        denom = 0
        for i in range(5):
            for j in range(5):
                num += weights[i][j] * resp_distr[i][j]
                denom += weights[i][j] * np.sum(resp_distr[i,:]) * np.sum(resp_distr[:,j])
        weighted_kappa = 1 - total_resp * 1.0 * num / denom
        print (resp_distr, total_resp, total_coincidence, observed_agreement, "Kappa:", kappa, "weighted kappa:", weighted_kappa)
        return weighted_kappa

#Computes the standard Cohen's Kappa interannotator agreement metric
#Inputs: resp1, resp2 - response sequences for two users
#Return value: the Kappa coefficient (from [0, 1])
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
relatums = {}
system_yn = {}
test_counter = 0
tj_count = 0
descr_count = 0
descr_success = 0
suggested_rels = {}

#Main annotation evaluation pipeline
for subm in open('annotations').readlines():

    #Read-off the annotation components
    subm = subm.strip().split(":")
    ID = subm[0].split("=")[1]
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
    if task_type == "1":# and "behind" in resp:
        print ("ID:", ID, resp, user, testcase, task_type)

        #Call Blender with the extracted annotation data
        result = subprocess.check_output(["blender", scene_path, "--background", "--python", "main.py", "--", relation, relatum, referent1, referent2, task_type, resp])
        result = result.decode("utf-8").split("\n")

        #Print the evaluation results
        res = ""
        for item in result:
            if "RESULT" in item:
                res = (item.split(":")[1]).strip()
                break

        rel = ""
        for key in rel_accuracy:
            if key in resp and (key != "in " or "front" not in resp):
                rel = key
                break
        rel_accuracy[rel][0] += 1
        descr_count += 1
        if res == "1" or res == "0":
            res = int(res)
            descr_success += res
            rel_accuracy[rel][1] += res
        if res != 1:
            print ("{}\nRESULT: {}".format(result, res))
        print ("TOTAL PROCESSED: {}".format(descr_count))

        '''if testcase not in suggested_rels:
            ur_relations[testcase] = {}
            for rel in relations:
                if rel in resp and (rel != "in" or rel == "in" and "in " in resp and "front" not in resp):
                    ur_relations[testcase][user] = rel

            result = subprocess.check_output(["blender", scene_path, "--background", "--python", "main.py", "--", " ", relatum, " ", " ", "2", " "])
            result = result.decode("utf-8").split("\n")
            res = ""
            for item in result:
                if "RESULT" in item:
                    res = (item.split(":")[1]).strip()
                    break
            suggested_rels[testcase] = res.split("#")
            print (res.split("#"))'''
        
    elif task_type == "0" and ID == "100000000":
        result = subprocess.check_output(["blender", scene_path, "--background", "--python", "main.py", "--", relation, relatum, referent1, referent2, task_type, resp])
        result = result.decode("utf-8").split("\n")
        print (result)
        ur_yn[user][testcase] = yn_to_index[resp]
        tj_count = tj_count + 1
        res = ""
        for item in result:
            if "RESULT" in item:
                res = (item.split(":")[1]).strip()
                break        
        res = math.floor(5 * float(res))
        print ("RESULT:", res, "USER RESULT:", ur_yn[user][testcase])
        system_yn[testcase] = res

print ("DESCRIPTION TASK ACCURACY: {}".format(descr_success / descr_count))
print ("PER-RELATION ACCURACY: {}".format(rel_accuracy))

correct_suggestions = 0
for key in suggested_rels:
    for user in ur_relations[key]:
        if ur_relations[key][user] in suggested_rels[key]:
            correct_suggestions += 1
            break

print ("SUGGESTION ACCURACY: {}".format(correct_suggestions / descr_count))
    

#Compute and print the interannotator agreement
'''print(ur_yn.keys())
print("TJ_COUNT: ", tj_count)
avg = 0
tot = 0
keys = [key for key in iter(ur_yn)]
for us1 in range(len(keys)):
    for us2 in range(us1, len(keys)):
        if us1 != us2:
            print (keys[us1], keys[us2])
            result = weighted_cohen_kappa(ur_yn[keys[us1]], ur_yn[keys[us2]])
            if result is not None:
                avg += result
                tot += 1
print ("AVG KAPPA:", 1.0 * avg / tot)'''
'''
for user in ur_yn:
    print ("USER:", user)
    print (weighted_cohen_kappa(ur_yn[user], system_yn))
'''
