import re

input = ""
for line in open("dump", "r").readlines():
    input = input + line
#print (input)
input = input.split("###\n")
tests = []
for test in input:
    test = test.split(':')
    tests.append([test[0], test[1], test[2], [x for x in re.split("[;\n]", test[3]) if x != ""]])
print (tests)
