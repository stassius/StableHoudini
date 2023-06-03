import json
from pathlib import Path
import hou
import os

hda = hou.nodeType('Top/Stable_Diffusion_Dream').definition().libraryFilePath()
hda = os.path.dirname(hda)

def GetURL(node):
    if node.parm("customURL").eval()==True:
        url = node.parm("url").eval()
    else:
        url = None
    return url

def GetListOfFiles(path, forMenu, addNone):
    results = []
    if addNone:
        if forMenu:
            results.extend(["None", "None"])
        else:
            results.append("None")
    targetPath = os.path.join(hda, path)
    presets_dir = os.path.dirname(targetPath)
    Path(targetPath).mkdir(parents=True, exist_ok=True)
    for file in os.listdir(targetPath):
        if file.endswith(".json"):
            with open(os.path.join(targetPath, file)) as f:
                try:
                    data = json.load(f)
                    results.append(file)
                    if forMenu:
                        results.append(data['name'])
                except:
                    print(f"Error parsing JSON {file}")
    return results

def GetJSON(path):
    with open(os.path.join(hda, path)) as f:
        try:
            result = json.load(f)
        except:
            print(f"Error parsing JSON {path}")
            result = None    
        return result
    
def FillUI(node, targetFolderName, parms, groups, additionalFolders = None):
    """
    Given a node, this function fills in a specified UI folder with new parameters. 
    The function takes in the node, the target folder name, a list of parameter dictionaries, 
    and an optional list of additional folders to add. The function returns a list of all 
    parameter names added to the UI. 

    :param node: The node to add parameters to.
    :param targetFolderName: The name of the folder to add parameters to.
    :param parms: A list of parameter dictionaries, each containing information about the parameter to add.
    :param additionalFolders: An optional list of additional folders to add.
    :return: A list of all parameter names added to the UI.
    """
    group = node.parmTemplateGroup()
    RemoveAllParmsFromFolder(targetFolderName, group)
    node.setParmTemplateGroup(group)
    folder = group.findFolder(targetFolderName)
    # Find all Parm Groups and create folders for them
    folders = set([ x['group'] for x in parms if 'group' in x ])
    parmFolders = {}
    for fld in folders:
        parmFolders[fld] = hou.FolderParmTemplate(fld, fld)
    allParms = []
    for i, parm in enumerate(parms):
        help = parm.get('help', None)
        range = parm.get('range', None)
        values = parm.get('values', None)
        multiline = parm.get('multiline', None)
        displayName = parm.get('displayName', None)
        if not 'default' in parm:
            default = None
        else:
            default = parm['default']
        parmType = parm['type']
        newParm = CreateParm(name=parm['name'], displayName=displayName, parmType=parmType, default=default, range=range, help=help, values=values, multiline=multiline)
            
        if not newParm:
            print(f"Unknown Parm Type: {parm['type']} for {parm['name']}")
            continue
        if 'hidden' in parm:
            newParm.hide(parm['hidden'])
        if 'group' in parm:
            parmFolders[parm['group']].addParmTemplate(newParm)
        else:
            folder.addParmTemplate(newParm)
        allParms.append(parm['name'])
        
    if groups:
        sorted = groups
    else:
        sorted = folders
    for fld in list(sorted):
        print(f"Adding {fld} folder")
        folder.addParmTemplate(parmFolders[fld])
    for fld in list(set(folders) - set(sorted)):
        folder.addParmTemplate(parmFolders[fld])
        
    # Add additional folders
    if additionalFolders:
        for fld in additionalFolders:
            folder.addParmTemplate(fld)
    group.replace(group.findFolder(targetFolderName), folder)
    node.setParmTemplateGroup(group)
    return allParms
    
def CreateParm(name, displayName, parmType, default, range = None, help = None, values = None, multiline = None):
    if not displayName:
        displayName = name.replace("_", " ").capitalize()
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
        newParm = hou.StringParmTemplate(name, displayName, 1, default_value=(default,), help = help)
        newParm.setMenuLabels(values)
        newParm.setMenuItems(values)
                
    elif parmType == "bool":
        if default is None:
            value = False
        else:
            value = default
        newParm = hou.ToggleParmTemplate(name, displayName, default_value=value, help = help)
        
    elif parmType == "directory":
        newParm = hou.StringParmTemplate(name, displayName, 1, default_value=(default,), string_type = hou.stringParmType.FileReference, file_type = hou.fileType.Directory, help = help)
        
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