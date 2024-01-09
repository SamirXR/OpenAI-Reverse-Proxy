import os
import subprocess
import threading

files = [
    "nyx_api/api.py",
    "discord_bot/bot.py",
]  

def run_script(file):
    command = f"python {os.getcwd()}/{file}"  
    subprocess.Popen(command, shell=True)

threads = []

for file in files:
    thread = threading.Thread(target=run_script, args=(file,))
    threads.append(thread)
    thread.start()

while True:
    pass
