#!/usr/bin/python


import os,sys,time
import global_env 
WorkDir=global_env.WorkDir
SysAnalyzer = 'python %s/include/SysAnalyzer.py ' % WorkDir 
HeadLine='''\n\033[33;40;1m
________________________________________________________________________________________________
		
				System Capacity Analyzer 1.0
			
									Powered by TriAquae


Notice:  Index will display in 3 colours
 1. Green: means everything runs in a good status
 2. Yellow: means system running ok ,but crossed the susggest index value,no need panic
 3. Red:  means system is in a busy status ,if any of the index is always in a red colour status,
	 maybe you need to think about improving the system capacity.

________________________________________________________________________________________________
\033[0m'''
def collect(dir,filename_head=0,dump_2_file=0):
	#try:
	log_files= os.listdir(dir)
	f= file(dump_2_file,'w')
	f.write(HeadLine)
	f.flush()
	for filename in log_files:
		if filename.startswith(filename_head):
			OriFileName= '%s/logs/%s' %(WorkDir,filename)
			NewFileName = '%s/logs/Analyzer_%s' % (WorkDir,filename)
			FormatSysInfo = '%s %s > %s ' % (SysAnalyzer,OriFileName,NewFileName)
			os.system(FormatSysInfo)
			#Archive logs
			date=time.strftime('%Y_%m_%d_%H_%M')
			Archive_dir='%s/logs/archive' % WorkDir
			Archived_log_name='%s/%s_%s' %(Archive_dir,filename,date)
			Dump_to_Archive='mv %s %s' % (OriFileName,Archived_log_name)
			os.system(Dump_to_Archive)

			#Dump all fomatted log files to one file
			DumpCmd='cat %s >> %s' %(NewFileName,dump_2_file)
			os.system(DumpCmd)
			
	f.close()		
	#except:

#collect('../logs/','system_runing','../logs/All_runing_status')

def show_file(filename):
	try:
		LineNum=1
		f= file(filename)
		while True:
			line=f.readline()
			if len(line) == 0:break
			if LineNum == 50:
				option=raw_input('\033[32;40;5m------More------\033[0m')
				if option == '':
					print line,
					LineNum = 1
			else:
				print line,
				LineNum = LineNum + 1
		print '\n\n\033[33;40;1m--------Done----------\nYou can all see the log in %s \033[0m' % filename
						
	except IOError:
		print '\033[31;40;1mno log to be showed,exit.\n\033[0m'
		sys.exit()

#show_file('../logs/All_runing_status')
