from subprocess import call

print ("Running Blender...")
call(["blender", "blocks_world.blend", "--background", "--python", "main.py"])
