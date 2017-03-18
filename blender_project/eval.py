import re
import subprocess

relations = {'near': [0,0], 'in': [0,0], 'on':[0,0] , 'touching': [0,0], 'front': [0,0], 'behind': [0,0], 'right': [0,0], 'left': [0,0], 'at': [0,0], 'over': [0,0], 'under': [0,0], 'above': [0,0], 'below': [0,0], 'between': [0,0]}
inp = ""
for line in open("dump", "r").readlines():
    inp = inp + line
tests = []
for test in inp.split("###\n"):
    if test != "":
        test = test.split(':')
        tests.append([test[0], test[1], test[2], [x for x in re.split("[;\n]", test[3]) if x != ""]])

total = 0
total_test = 0
success = 0
for test in tests:
	scene_path = test[0] + "/scene.blend"
	total_test = total_test + 1
	for response in test[3]:
		total = total + 1
		res = subprocess.check_output(["blender", scene_path, "--background", "--python", "main.py", "--", test[1], response])
		res = res.decode("utf-8").split("*")
		for item in res:
			if item != "":
				print (item)
				item = item.split()
				if len(item) > 0 and item[0] == 'RELATION:':
					print (item)
					relations[item[1]][0] = relations[item[1]][0] + 1
					relations[item[1]][1] = relations[item[1]][1] + float(item[2])					
		if 'RESULT: OK' in res:
			success = success + 1		
		#input("Press key to continue...")
	print (relations)
	print ("SR: ", float(success) / total, ", TOTAL: ", total_test, "/", len(tests))
	print ("SUCCESS TOTAL: ", success, "TEST TOTAL: ", total)

for item in relations.keys():
	if relations[item][0] != 0:
		relations[item][1] = relations[item][1] / relations[item][0]
print (relations)

