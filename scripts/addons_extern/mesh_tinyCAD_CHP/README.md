# mesh_tinyCAD_CHP

> Chamfer plus (first extend non intersecting edges, then trigger fillet / chamfer Operator). 

### Installation

This addon lives separately from the mesh_tinyCAD add-on.  

1. Download zip to some location on your HD
2. UserPrefs -> Addons -> Install from File -> Locate the Zip
3. Enable using Tick box.
4. Ctrl+U and Save User Preferences to Fully store the add-on's enabled state in your startup.blend

### Usage

**how to Trigger:**  

1. It will attach itself to the tinyCAD `W` menu if it's found. 
2. or.. hit Spacebar, type `CHP` and trigger it that way

- Menu item should only appear if two edges are selected.
- Operator should only process geometry if the condition known as `V` is met. (both edges can be projected to a common intersection)

### Limitations

This only intended to solve the `V` condition. Not `X` and `T` (are a little more involved..and not worth my time)

`V` is the last row in this graphic.  
![image 1](https://cloud.githubusercontent.com/assets/619340/12535934/071df51a-c295-11e5-8ae0-4efd475e4273.png)





