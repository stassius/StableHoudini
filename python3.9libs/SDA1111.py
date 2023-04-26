import re
# from msilib.schema import Error
import os
from pathlib import Path
import requests
import io
import base64
from PIL import Image, PngImagePlugin


class StableDiffusion(object):
    def __init__(self):
        os.environ['HTTP_PROXY'] = ''

    def ParseArgs(self, args):
        payload = {}
        for key in args:
            payload[key] = args[key]
        return payload

    def Error(self, code):
        if code==404:
            print("Error connecting server!")
            return
        print("Server Error!")

    def Interrupt(self, url):
        print("Interrupting...")
        response = self.Request(f'{url}/sdapi/v1/interrupt',  "POST")

    def SetOption(self, url, option, value):
        print("Changing option: "+option+" to value: "+ str(value))
        option_payload = {
        option: value
        }
        response = self.Request(f'{url}/sdapi/v1/options',  "POST", option_payload )

    def GetCurrentModel(self, url):
        response = self.Request(f'{url}/sdapi/v1/options',  "GET")
        if response == None:
            return ("Error", "Error")
        r = response.json()
        return r[r'sd_model_checkpoint']

    def SwitchModel(self, url, model):
        option_payload = {
        "sd_model_checkpoint": model
        }
        response = self.Request(f'{url}/sdapi/v1/options',  "POST", option_payload)

    def GetAvailableModels(self, url):
        response = self.Request(f'{url}/sdapi/v1/sd-models',  "GET")
        if response == None:
            return("Error", "Error")
        list=[]
        for r in response.json():
            list+=[r['title']]
            list+=[r['title']]
        list.sort()
        return list

    def CN_GetAvailableModels(self, url):
        response = self.Request(f'{url}/controlnet/model_list',  "GET")
        if response == None:
            return("Error", "Error")
        list=[]
        for r in response.json()['model_list']:
            list+=[r]
            list+=[r]
        return list

    def CN_GetAvailableProcessors(self, url):
        response = self.Request(f'{url}/controlnet/module_list',  "GET")
        if response == None:
            return("Error", "Error")
        list=[]
        for r in response.json()['module_list']:
            list+=[r]
            list+=[r]
        return list

    def GetAvailableSamplers(self, url):
        response = self.Request(f'{url}/sdapi/v1/samplers',  "GET")
        if response == None:
            return ("Error", "Error")
        list=[]
        for r in response.json():
            list+=[r['name']]
            list+=[r['name']]
        return list

    def GetAvailableUpscalers(self, url):
        response = requests.get(f'{url}/sdapi/v1/upscalers')
        if response == None:
            print('GetAvailableUpscalers', response.status_code)
            return ("Error", "Error")
        list=[]
        for r in response.json():
            list+=[r['name']]
            list+=[r['name']]
        return list

    def GetTrailingNumber(s):
        m = re.search(r'\d+$', s)
        return int(m.group()) if m else None

    def SplitToStringAndNumber(self, s):
        head = s.rstrip('0123456789')
        tail = s[len(head):]
        return head, tail

    def GetNumberedName(self, s, index):
        filename, extension = os.path.splitext(s)
        name, number = self.SplitToStringAndNumber(filename)
        if number:
            number = str(int(number) + index)
            name+=number
        filename=name+extension
        return filename

    def SaveFileDirect(self, url, file, output, index = None):
        image = Image.open(io.BytesIO(base64.b64decode(file.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + file
        }

        response2 = self.Request(f'{url}/sdapi/v1/png-info',  "POST", png_payload)
        if response2 == None:
            return

        if index is not None:
            filename = self.GetNumberedName(output, index)
        else:
            filename = output

        print("Saving file: "+filename)
        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save(filename, pnginfo=pnginfo)

    def Request(self, url : str, type : str, payload = None) -> requests.Response:
        if type == "POST":
            try:
                if payload:
                    response = requests.post(url=url, json=payload)
                else:
                    response = requests.post(url=url, timeout=0.1)
                if response.status_code!=200:
                    print('Request POST', response.status_code)
                    print(f'URL: {url}')
                    return None
                return response
            except requests.exceptions.RequestException as e:
                print("Connection error: "+url)
                return None
        elif type == "GET":
            try:
                response = requests.get(url=url, timeout=0.1)
                if response.status_code!=200:
                    print('Request GET', response.status_code)
                    print(f'URL: {url}')
                    return None
                return response
            except requests.exceptions.RequestException as e:
                print("Connection error: "+url)
                return None
        else:
            print("Unknown type of request!")

    def TextToImage(self, url, output, model, args):
        payload = self.ParseArgs(args)
        if model:
            override_settings = {}
            override_settings["sd_model_checkpoint"] = model
            override_payload = {
                    "override_settings": override_settings
            }
            print("Generating with model: " + model)
            payload.update(override_payload)
        response = self.Request(f'{url}/sdapi/v1/txt2img',  "POST", payload)
        if response == None:
            return
        r = response.json()
        if len(r['images'])>1:      
            for idx, i in enumerate(r['images']):
                self.SaveFileDirect(url, i, output, idx)
        else:
            self.SaveFileDirect(url, r['images'][0], output)

    def ImageToImage(self, url, output, model, args, image, mask):
        payload = self.ParseArgs(args)
        fc = open(image, 'rb').read()
        imgEncoded = "data:image/png;base64," + base64.b64encode(fc).decode('utf-8')
        payload.update({"init_images" : [imgEncoded]})
        if mask:
            fc = open(mask, 'rb').read()
            maskEncoded = "data:image/png;base64," + base64.b64encode(fc).decode('utf-8')
            payload.update({"mask" : maskEncoded})
            # payload.update({"inpaint_full_res": False})

        if model:
            override_settings = {}
            override_settings["sd_model_checkpoint"] = model
            override_payload = {
                    "override_settings": override_settings
            }
            print("Generating with model: " + model)
            payload.update(override_payload)
        response = self.Request(f'{url}/sdapi/v1/img2img',  "POST", payload)
        if response == None:
            return

        r = response.json()

        if len(r['images'])>1:      
            for idx, i in enumerate(r['images']):
                self.SaveFileDirect(url, i, output, idx)
        else:
            self.SaveFileDirect(url, r['images'][0], output)
        print("Generation completed")

    def upscaleAndSave(self, url, upscaler, resizeValue, folder, image):
        print("Upscaling...")
        payload = {
            "upscaler_1": upscaler,
            "upscaling_resize": resizeValue,
        }

        fc = open(image, 'rb').read()
        imgEncoded = "data:image/png;base64," + base64.b64encode(fc).decode('utf-8')
        payload.update({"image" : imgEncoded})
        response = self.Request(f'{url}/sdapi/v1/extra-single-image',  "POST", payload)
        if response == None:
            return None
        r = response.json()
        head = os.path.splitext(image)[0]
        path,filename = os.path.split(image)
        outputpath = path+"/"
        if folder:
            outputpath += folder+"/"
        print("Upscaling complete")
        self.SaveFileDirect(url, r['image'], outputpath+"upscaled_"+filename)
        return outputpath+"upscaled_"+filename