import configparser
import hou    
import os  
from pathlib import Path
from os.path import exists  

listConfig = {
    'models': { 
                'url': '/sdapi/v1/sd-models', 
                'jsonitem' : '',
                'jsonname' : 'title'},
    'samplers': { 
                'url': '/sdapi/v1/samplers', 
                'jsonitem' : '',
                'jsonname' : 'name'},
    'upscalers': { 
                'url': '/sdapi/v1/upscalers', 
                'jsonitem' : '',
                'jsonname' : 'name'},
    'embeddings': { 
                'url': '/sdapi/v1/embeddings', 
                'jsonitem' : 'loaded',
                'jsonname' : ''},
    'hypernetworks': { 
                'url': '/sdapi/v1/hypernetworks', 
                'jsonitem' : '',
                'jsonname' : 'name'},
    'loras': { 
                'url': '/sdapi/v1/loras', 
                'jsonitem' : '',
                'jsonname' : 'name'},
    'cn_models': { 
                'url': '/controlnet/model_list', 
                'jsonitem' : 'model_list',
                'jsonname' : ''},
    'cn_preprocessors': { 
                'url': '/controlnet/module_list', 
                'jsonitem' : 'module_list',
                'jsonname' : ''},
}

availableItems = {
    'models' : [],
    'samplers' : [],
    'upscalers' : [],
    'embeddings' : [],
    'hypernetworks' : [],
    'loras' : [],
    'cn_models' : [],
    'cn_preprocessors' : [],
}

config = configparser.ConfigParser()

def WriteDefaulConfig(filename):
    config = configparser.ConfigParser()
    config['Main'] = {
        'url' : 'http://127.0.0.1:7860',
        'timeout' : 1.2,
        }
    config['Authorization'] = {
        'useauth' : False,
        'username' : '',
        'password' : ''
    }
    Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
    print("Writing default config to "+filename)
    with open(filename, 'w') as file:
        config.write(file)

def GetConfigValue(section, key):
    if not config.has_option(section, key):
        print(f"Error! No config value for {section}/{key}. Delete config file and restart the project.")
        return None
    return config[section][key]


configfile = os.path.dirname(hou.nodeType('Top/Stable_Diffusion_Dream').definition().libraryFilePath())+"/Config/config.ini"
if not exists(configfile):
    WriteDefaulConfig(configfile)
config.read(configfile)
