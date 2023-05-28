import hou

def GetURL(node):
    if node.parm("customURL").eval()==True:
        url = node.parm("url").eval()
    else:
        url = None
    return url

def CreateParm(name, displayName, parmType, default, range = None, help = None, values = None, multiline = None):
    if range:
        min = range[0]
        max = range[1]
    if parmType == "int":
        if not range:
            min = 1
            max = 10
        newParm = hou.IntParmTemplate(name, displayName, 1, default_value=(int(default),), min = min, max = max, help = help)   
                
    elif parmType == "float":
        if not range:
            min = 0.0
            max = 1.0
        newParm = hou.FloatParmTemplate(name, displayName, 1, default_value=(default,), min = min, max = max, help = help)
                
    elif parmType == "string":
        if multiline:
            newParm = hou.StringParmTemplate(name, displayName, 1, default_value=(default,), help = help, tags = {'editor' : '1', 'editorlines' : '3-10'})
        else:
            newParm = hou.StringParmTemplate(name, displayName, 1, default_value=(default,), help = help)
                
    elif parmType == "intMenu":
        newParm = hou.IntParmTemplate(name, displayName, 1, default_value=(default,), help = help)
        newParm.setMenuLabels(values)
        newParm.setMenuItems(values)
                
    elif parmType == "stringMenu":
        newParm = hou.StringParmTemplate(name, displayName, 5, default_value=(default,), help = help)
        newParm.setMenuLabels(values)
        newParm.setMenuItems(values)
                
    elif parmType == "bool":
        newParm = hou.ToggleParmTemplate(name, displayName, default_value=(default,), help = help)
        
    else:
        newParm = None
        
    return newParm

def RemoveAllParmsFromFolder(folderName, group):
    folder = group.findFolder(folderName)
    for i in folder.parmTemplates():
        group.remove(i)
        
def RemoveParm(node, parmName):
    group = node.parmTemplateGroup()
    existing = group.find(parmName)
    if existing:
        group.remove(existing)
        node.setParmTemplateGroup(group)