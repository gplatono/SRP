from subprocess import call
import os

print ("Running Blender...")

for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    if file.endswith(".blend"):
        call(["blender", file, "--background", "--python", "main.py"])
