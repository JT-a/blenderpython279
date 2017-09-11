import bpy
import os
import json
import uuid

baseline_file = bpy.utils.user_resource("DATAFILES", "Baseline.json")
baseline_data_storage = bpy.utils.user_resource("DATAFILES", "UserPrefsBaseline", create=True)
baseline_keys_storage = bpy.utils.user_resource("DATAFILES", "UserPrefsBaselineHotKeys", create=True)


def ignore(x):
    if x.startswith("__") or x in {"bl_rna"}:
        return False
    return True


def iterprops(prop):
    for prefsect_name in filter(ignore, dir(prop)):
        prefsect = getattr(prop, prefsect_name)
        for prefvar_name in filter(ignore, dir(prefsect)):
            prefvar_val = getattr(prefsect, prefvar_name)
            if type(prefvar_val) in {bool, int, str, float}:
                yield ((prefsect_name, prefvar_name), repr(prefvar_val))


def propdict(prop):
    d = dict()
    for k, v in iterprops(prop):
        d[".".join(k)] = str(v)
    d['addons'] = [addon.module for addon in prop.addons]
    return d


def propjson(prop):
    return json.dumps(propdict(prop))
