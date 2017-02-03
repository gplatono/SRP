from subprocess import call

print ("Running Blender...")
call(["blender", "sandbox.blend", "--background", "--python", "main.py"])
