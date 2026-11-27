import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cast5 import *
clear_scene(); arm = build('milo')
print('PROBE', sorted({(o.name.split('_')[1] if '_' in o.name else o.name, (o.data.materials[0].name if getattr(o,'data',None) and hasattr(o.data,'materials') and o.data.materials else '-')) for o in bpy.data.objects if o.name.startswith('milo_eye')}))
