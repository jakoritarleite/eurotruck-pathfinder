import sys
import subprocess

def exec_command(command):
	sub = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	output = sub.stderr.read()+sub.stdout.read()

	return output

while True:
	_ = exec_command("python pathfinder.py")
	_ = exec_command(f"./sxc/sxc64.exe {sys.argv[1]} -bl list.txt")
	o = exec_command(f"./sxc/sxc64.exe {sys.argv[1]} -o output")
	_ = exec_command("python clean.py")

	if '0 items still missing' in o:
		break