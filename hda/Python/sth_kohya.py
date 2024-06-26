import os
import signal
import subprocess
import platform
import sth_settings
import hou
import psutil
import sys


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    if including_parent:
        parent.kill()


kohya_dir = sth_settings.GetConfigValue('Training', 'kohya_folder')
stop = False

if not kohya_dir:
    print('Adding default Kohya folder to hda/Config/config.ini')
    print('Please, change it to the real kohya_ss location and restart the project.')
    sth_settings.SetConfigValue('Training', 'kohya_folder', 'C:/kohya_ss/')


def CallKohya(script_name, source_folder, num_cpus, parms):
    global kohya_dir
    global stop

    venv = os.path.join(kohya_dir, "venv")
    # Activate venv
    if platform.system() == 'Windows':
        activate_script = f'{venv}/Scripts/activate.bat'
        accelerate_path = os.path.join(venv, "Scripts/accelerate")
    else:
        activate_script = f'source {venv}/bin/activate'
        accelerate_path = os.path.join(venv, "bin/accelerate")
    command = f'{accelerate_path} launch --num_cpu_threads_per_process {str(num_cpus)} ' + os.path.join(
        kohya_dir, script_name)

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

    os.environ['PYTHONIOENCODING'] = 'utf-8'
    print("Starting Kohya_ss with next arguments:")
    print('--------------------------------------')
    print(command)
    print('--------------------------------------')
    # Starting Kohya
    # check_path = 'python -c "import sys; print(sys.path)"'
    process = subprocess.Popen(f'{activate_script}  && {command}', shell=True, encoding="utf-8",
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, errors='ignore')
    hou.ui.setStatusMessage('Training started')
    while True:
        realtime_output = process.stdout.readline()
        return_code = process.returncode
        if stop:
            stop = False
            kill_proc_tree(process.pid)
            return_code = 100
            break
        if realtime_output == '' and process.poll() is not None:
            break
        if realtime_output.strip():
            if '%|' in realtime_output.strip():
                hou.ui.setStatusMessage(realtime_output.strip())
            else:
                print(realtime_output.strip(), flush=False)
    hou.ui.setStatusMessage('Finished')
    return return_code


def Interrupt():
    global stop
    stop = True
