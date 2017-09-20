from subprocess import call
import os

print ("Running Blender...")

for file in os.listdir("/u/gplatono/SRP/blender_project/screenshots"):
    if file.endswith(".blend"):
        call(["blender", file, "--background", "--python", "main.py"])
