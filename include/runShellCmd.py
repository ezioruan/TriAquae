#!/usr/bin/python
import os


def runShell(cmd):
	
	os.system(cmd)
def userInput():
	while True:
		input = raw_input('\033[36;1mShell command[q to quit]:\033[0m')
		try:
			if len(input.strip()) == 0:continue
			if input == 'q':break
			runShell(input)
		except KeyboardInterrupt:break
