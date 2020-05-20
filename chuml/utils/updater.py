#!/usr/bin/python3
import os
import signal
import subprocess
import time
import datetime
import json

gunicorn = None
def start():
	global gunicorn
	gunicorn = subprocess.Popen(
		"gunicorn3 index:app",
		stdout=subprocess.PIPE, 
		shell=True,
		preexec_fn=os.setsid
		)

def stop():
	os.killpg(os.getpgid(gunicorn.pid), signal.SIGTERM) 

def up_to_date():
	return b'Already up to date.\n' == subprocess.check_output(
		["git", "pull"], stderr=subprocess.STDOUT)

if __name__ == "__main__":
	start()
	while True:
		if not up_to_date():
			print(datetime.datetime.now(), "updating...")
			stop()
			start()

		time.sleep(5*60)