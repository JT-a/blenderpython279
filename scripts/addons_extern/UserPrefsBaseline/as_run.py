import bpy
import os
import sys
import json
import uuid

sys.path.append(os.path.dirname(__file__))

import baseline_lib_funcs

with open(baseline_lib_funcs.baseline_file, "w") as f:
    f.write(baseline_lib_funcs.propjson(bpy.context.user_preferences))

print("SENTINEL_TOKEN")

sys.exit()
