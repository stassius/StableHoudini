defaultURL = "http://127.0.0.1:7860"
username = ""
password = ""
timeout = 1
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
    'cn_models' : [],
    'cn_preprocessors' : [],
}
