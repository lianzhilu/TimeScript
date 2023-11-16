import os
import argparse
import time
from bcc import BPF
from bcc.utils import printb
import time
import subprocess
import getpass
import multiprocessing
import platform


def open_terminal_and_run_command(command):
    if platform.system() == "Windows":
        terminal_command = "start cmd /K"
    elif platform.system() == "Linux":
        terminal_command = "x-terminal-emulator -e"
    elif platform.system() == "Darwin":  # macOS
        terminal_command = "open -a Terminal"
    else:
        print("Unsupported operating system.")
        return
    subprocess.run(f"{terminal_command} {command}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # output_queue.put(result.stdout)

def work_func():
    # os.system('sudo python3 timesnoop.py')
    open_terminal_and_run_command('sudo python3 timesnoop.py')

def find_latest_file(dir):
    current_directory = dir
    all_files = os.listdir(current_directory)

    files = [f for f in all_files if os.path.isfile(os.path.join(current_directory, f))]
    
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(current_directory, f)))
    
    return latest_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--runtime', type=str, default='', help='The wasm runtime you want to run.')
    parser.add_argument('--source', type=str, default='', required=True, help='The source wasm file you want to run.')
    parser.add_argument('--times', type=int, default=1, help='The number of times you want to run.')
    parser.add_argument('--outdir', type=str, default='./record/', help='The output directory of execution time. If you want to use other directory, please replace dir in timesnoop.py')
    args = parser.parse_args()

    worker_process = multiprocessing.Process(target=work_func)
    worker_process.start()

    runtime = args.runtime
    source = args.source
    times = args.times
    outdir = args.outdir

    if runtime == 'wasmer':
        runway = 'wasmer run'
    elif runtime == 'wamr':
        runway = './iwasm'
    elif runtime == 'wasmedge-aot':
        runway = 'wasmedge --dir .:.'
    else:
        runway = runtime
    
    time.sleep(15)
    while times >= 0:
        os.system(runway+ ' ' +source)
        print(str(times))
        time.sleep(10)
        times -= 1
    
    worker_process.join()

    lastfile = find_latest_file(outdir)
    count = 0
    total = 0.0
    with open(outdir + lastfile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            num = float(line)
            count += 1
            total += num
    print('avg: ', total/count)