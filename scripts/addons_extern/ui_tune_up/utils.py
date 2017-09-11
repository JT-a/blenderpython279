from bpy.ops import op_as_string
import os, re, json

dev = False

path = os.path.dirname(__file__)
print(path)
# if dev:
# 	path = "D:\\Blender Foundation\\Blender\\2.75\\scripts\\addons\\ui_tune_up"

#debug dump variables
def dd(*value, dodir=0, vert=0, start=""):

	if dev:
		if start:
			print(start)
			
		if dodir: 
			print(30*"-")
			print(dir(value))
		elif vert:
			for arg in value:
				print(10*"-")
				for v in arg:
					if isinstance(arg, dict):
						print(v, arg[v])
					else:
						print(v)
		else:
			n = len(value)
			pattern = n * "%s "
			value = pattern % value
			print(value)

def operator_exists(idname):
   try:
	   op_as_string(idname)
	   return True
   except:
	   return False

def is_operator(cls):
	return hasattr(cls, "__mro__") and bpy.types.Operator in cls.__mro__

#compose a filename with the addon path
def p(file, open_folder = False):
	file = os.path.join(path, file)
	if open_folder:
		os.startfile(os.path.dirname(file))
	return file

def load_json(file):
	data = []
	#strip comments 
	with open(p(file), "r") as f:
		data = f.read()
		#strip // comments
		regex = re.compile("//.+", re.MULTILINE)
		data = re.sub(regex, "", data)
	try:
		data = json.loads(data)
	except Exception as e:
		return "Config Error: " + e.args[0]
	return data


