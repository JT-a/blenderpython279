import bpy
from ui_tune_up.utils import operator_exists, dd, load_json, path
kc = bpy.context.window_manager.keyconfigs['Blender User']

valid_map_types = [m.identifier for m in bpy.types.KeyMapItem.bl_rna.properties['map_type'].enum_items]

#removes key shortcuts assigned to invalid operators
def clear_keyboard():
	print("cleaning keyboard")
	for map in kc.keymaps:
		for k in map.keymap_items:
			idname = k.idname
			if idname and not operator_exists(idname):
				print("removing", idname)
				map.keymap_items.remove(k)
				
def validate_key(kdata):
	
  	#validate args number
	if not len(kdata) == 5:
		print(kdata)
		print("key has 5 arguments but %i were given." % len(kdata))
		print("cmd, mapname, idname, props, kprops")
		return False
	
	cmd, mapname, idname, props, kprops = kdata
	
	#validate cmd
	if not cmd in ['key', 'del']:
		print(kdata)
		print("Invalid command %s," % cmd, "not in 'key' or 'del'")
		return False

	#validate map
	try:
		map = kc.keymaps[mapname]
	except:
		print(kdata)
		print(mapname, "is not a valid map name.")
		return False
		
	#validate idname
	if not idname or not operator_exists(idname):
		print(kdata)
		print(idname, "is not a valid operator.")
		return False
	
	#validate map_type
	if not "map_type" in kprops or (not kprops['map_type'] in valid_map_types):
		kprops['map_type'] = "KEYBOARD"
		 
	if "type" in kprops and kprops['type'].find("MOUSE")>-1:
		kprops['map_type'] = "MOUSE"
	
	#normalize key modifiers
	if cmd == "key":
		any = "any" in kprops and kprops['any'] == True
		if any:
			if "shift" in kprops: del kprops["shift"]
			if "ctrl" in kprops: del kprops["ctrl"]
			if "alt" in kprops: del kprops["alt"]
			if "oskey" in kprops: del kprops["oskey"]
		else:
			if "any" in kprops: del kprops['any']
			kprops['shift'] = "shift" in kprops and kprops['shift'] == True
			kprops['ctrl'] = "ctrl" in kprops and kprops['ctrl'] == True
			kprops['alt'] = "alt" in kprops and kprops['alt'] == True
			kprops['oskey'] = "oskey" in kprops and kprops['oskey'] == True
			
	return True

def check_properties(data, props):

	for prop in props:
		try:
			if getattr(data, prop) != props[prop]:
				return False
		except Exception as e:
			print(e)
			return False
	
	return True

def findkey(kdata, by = "type"):
	cmd, mapname, idname, props, kprops = kdata
	
	map = kc.keymaps[mapname]
	
	#map_type = kprops['map_type']
	
	keys = []
	
	for k in map.keymap_items:
		found = False
		if by == "type" and kprops:
			found = check_properties(k, kprops)
		elif by == "idname" and idname and k.idname == idname:
			found = check_properties(k.properties, props)
			
		if found:
			keys.append(k)
	
	#print(keys)
	n = len(keys)
	
	if n == 0:
		#print("not found by", by)
		if by == "type":
			return findkey(kdata, "idname")
	elif n == 1:
		#print("found by", by)
		return keys[0]
	else:
		print("multiple found by",by)
		if by == "type":
			return findkey(kdata, "idname")

def setkey(kdata):
	cmd, mapname, idname, props, kprops = kdata
	
	if cmd == "del":
		return delkey(kdata)

	map = kc.keymaps[mapname]
	
	k = findkey(kdata)

	if not k:
		#wasnt found. create one
		if "type" in kprops:
			k = map.keymap_items.new(idname, kprops['type'], "PRESS")
		else:
			print(kdata)
			print("type not provided")
			return False
		

	#set maptype and idname
	if k.idname != idname:
		k.idname = idname
	
	map_type = kprops.pop('map_type')
	if k.map_type != map_type:
		k.map_type = map_type
	
	#check properties
	for prop in props:
		if not hasattr(k.properties, prop):
			print(kdata)
			print(prop, "is not a valid operator property for " + idname)
			return False
	
	for kprop in kprops:
		if not hasattr(k, kprop):
			print(kdata)
			print(kprop, "is not a valid type property")
			return False

	#all good modify the key
		
	for prop in props:
		setattr(k.properties, prop, props[prop])	

	for kprop in kprops:
		setattr(k, kprop, kprops[kprop])

	return True

def delkey(kdata):
	
	cmd, mapname, idname, props, kprops  = kdata
	
	map = kc.keymaps[mapname]
	
	keys = 0
	
	for k in map.keymap_items:
		found = False
		if idname and idname == k.idname:
			
			found = check_properties(k.properties, props)
			found = found * check_properties(k, kprops)
		
		if found:
			map.keymap_items.remove(k)
			keys+=1
			#del k
			#print(k)	

	print(kdata)
	print(keys, "removed")
	return True	

		
def load_keyboard():
	
	print(30*"-" + "loading keyboard")

	config = load_json("data.json")
	
	if isinstance(config, str):
		return {"ERROR"}, config

	data = config['keyboard']
	
	errors = 0
	for kdata in data:
		if validate_key(kdata):
			if setkey(kdata) == False: errors +=1
		else:
			errors +=1
	
	erstr = str(errors) + " errors. See console." if errors else ""
	return {"INFO"}, "Keyboard loaded. " + erstr

if __name__ == "__main__":
	print(load_keyboard())
	
