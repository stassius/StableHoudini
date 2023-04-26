import hou
import requests
import SDA1111
import importlib


def GetURL(node):

    importlib.reload(SDA1111)
    if node.parm("customURL").eval() == True:
        url = node.parm("url").eval()
    else:
        url = "http://127.0.0.1:7860"
    return url


def Reload(node):

    importlib.reload(SDA1111)
    SDA1111.StableDiffusion().SwitchModel(GetURL(node), node.parm("model").eval())


def RefreshModels(node):

    importlib.reload(SDA1111)
    model = SDA1111.StableDiffusion().GetCurrentModel(GetURL(node))
    if model:
        node.parm("model").set(model)


def Interrupt(node):

    importlib.reload(SDA1111)
    node.cancelCook()
    SDA1111.StableDiffusion().Interrupt(GetURL(node))