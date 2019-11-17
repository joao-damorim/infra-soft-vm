import subprocess

def exec(command):
    return  subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

# comando = "VBoxManage"

# print(exec(comando+' modifyvm Ubuntu --memory 4096 --vram 32 --boot1 dvd').communicate())