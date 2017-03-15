import re
import subprocess

inp = ""
for line in open("dump", "r").readlines():
    inp = inp + line
tests = []
for test in inp.split("###\n"):
    if test != "":
        test = test.split(':')
        tests.append([test[0], test[1], test[2], [x for x in re.split("[;\n]", test[3]) if x != ""]])

for test in tests:
	scene_path = test[0] + "/scene.blend"
	for response in test[3]:
		res = subprocess.check_output(["blender", scene_path, "--background", "--python", "main.py", "--", test[1], response])
		res = res.decode("utf-8").split("*")
		for item in res:
			if item != "":
				print (item)
		input("Press key to continue...")
