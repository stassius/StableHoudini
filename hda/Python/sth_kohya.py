import os
import signal
import subprocess
import platform
import sth_settings
import hou

kohya_dir = sth_settings.GetConfigValue('Training', 'kohya_folder')
process = None
stop = False

if not kohya_dir:
    print('Adding default Kohya folder to hda/Config/config.ini')
    print('Please, change it to the real kohya_ss location and restart the project.')
    sth_settings.SetConfigValue('Training', 'kohya_folder', 'C:/kohya_ss/')


def CallKohya(script_name, source_folder, network_module, num_cpus, parms):
    global process
    global kohya_dir
    global stop
    
    if process:
        print("Kohya is already running! Can't run another instance!")
        return
    
    venv = os.path.join(kohya_dir, "venv")
    command = f'accelerate launch --num_cpu_threads_per_process {str(num_cpus)} ' + os.path.join(kohya_dir, script_name) 
    
    # Parse arguments
    for key in parms:
        value = parms[key]
        if type(value) is bool:
            if value:
                command += " --" + key
        elif type(value) is str and not value.strip():
            continue
        elif type(value) is int and value == 0:
            continue
        elif type(value) is float and value == 0.0:
            continue
        else:
            command += " --" + key + "=" + str(value)
        
    command += f" --train_data_dir={source_folder}"
    command += f' --network_module={network_module}'
    # Activate venv
    if platform.system() == 'Windows':
        activate_script = f'{venv}/Scripts/activate.bat'
    else:
        activate_script = f'source {venv}/bin/activate'
    os.environ['PYTHONIOENCODING'] =  'utf-8'
    print("Starting Kohya_ss with next arguments:")
    print('--------------------------------------')
    print(command)
    print('--------------------------------------')
    # Starting Kohya
    process = subprocess.Popen(f'{activate_script}  && {command}', shell=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, errors='ignore')
    hou.ui.setStatusMessage('Training started')
    while True:
        realtime_output = process.stdout.readline()
        if stop:
            stop = False
            break
        if realtime_output == '' and process.poll() is not None:
            break
        if realtime_output.strip():
            if realtime_output.strip().startswith("steps:") or realtime_output.strip()[1].isdigit():
                hou.ui.setStatusMessage(realtime_output.strip())
            else:
                print(realtime_output.strip(), flush=False)
    hou.ui.setStatusMessage('Finished')

def Interrupt():
    global process
    process.kill()
    stop = True
    print("Process interrupted")
    process = None