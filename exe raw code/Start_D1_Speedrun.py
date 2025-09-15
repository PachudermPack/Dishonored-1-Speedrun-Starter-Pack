import os
import shutil
import subprocess
import sys

# Define the paths
source_loc = r"C:\Program Files\LiveSplit\Dishonored_1\settings.cfg"
dest_loc = os.path.expanduser("C:\\Program Files\\LiveSplit\\settings.cfg")

# Copy the file
shutil.copy(source_loc, dest_loc)

# Define the paths to executables and their respective directories
LiveSplit_path = r"C:\Program Files\LiveSplit\LiveSplit.exe"
InputOverlay_path = r"C:\Program Files\InputOverlay\NohBoard.exe"
D1_Jump_Macro_path = r"C:\Program Files\Jump_Macro_d1\Dish2Macro.exe"

# Directory for LiveSplit
LiveSplit_dir = os.path.dirname(LiveSplit_path)

# Directory for InputOverlay
InputOverlay_dir = os.path.dirname(InputOverlay_path)

# Directory for D1 Jump Macro
D1_Jump_Macro_dir = os.path.dirname(D1_Jump_Macro_path)

# Function to run subprocesses and ensure they are terminated properly
def run_subprocess(xmouse_command, cwd=None):
    process = subprocess.Popen(xmouse_command, shell=True, cwd=cwd, creationflags=subprocess.CREATE_NO_WINDOW)
    return process

# Run D1 Jump Macro in a separate Command Prompt window with a specific title
jump_macro_process = run_subprocess(
    f'start cmd /k "title DH1START && cd {D1_Jump_Macro_dir} && {os.path.basename(D1_Jump_Macro_path)}"'
)

# Run InputOverlay in its directory
inputoverlay_process = run_subprocess([InputOverlay_path], cwd=InputOverlay_dir)

# Run LiveSplit in its directory
livesplit_process = run_subprocess([LiveSplit_path], cwd=LiveSplit_dir)

# Run XMouse in its directory
xmouse_command = [
    "start", "", 
    "%userprofile%\\AppData\\Roaming\\Highresolution Enterprises\\XMouseButtonControl\\Configs\\DH1_Speedrun.xmbcp"
]
xmouse_process = run_subprocess(xmouse_command, shell=True)

# List of all subprocesses
subprocesses = [jump_macro_process, inputoverlay_process, livesplit_process, xmouse_process]

# Function to terminate all subprocesses and ensure they are cleaned up
def cleanup_processes(processes):
    for process in processes:
        if process.poll() is None:  # Check if the process is still running
            process.terminate()
        try:
            process.wait(timeout=5)  # Wait for the process to terminate
        except subprocess.TimeoutExpired:
            process.kill()

# Cleanup all subprocesses after they finish
cleanup_processes(subprocesses)

# Flush stdout to ensure everything is written
sys.stdout.flush()

print("All subprocesses have been terminated and cleaned up.")