#!/usr/bin/python
import global_env,os,sys,time
WorkDir=global_env.WorkDir
RecordLog = global_env.g_env()

ServerList='%s/conf/server_list' %WorkDir
CompressedFile='%s/conf/server_list.tgz' % WorkDir
TailLine='''\033[33;40;1m\nBefore you exit the program,you need to input a password to encrypt the password file.\n\033[0m'''
HeadLine='''\033[33;40;1m\nPlease input the password to decrypt the password file\n\033[0m'''

def Encrypt():
	print TailLine
	Compress='tar cvzf %s -C %s/conf server_list >/tmp/TriAquae.temp' %(CompressedFile,WorkDir)
	#tar cvzf serverlist.tar.bz -C /usr/local/TriAquae1011/conf/ server_list
	
	SystemUser = os.getlogin()
        Modify_ServerList_Permission = 'chmod -R 600 %s && chown -R %s %s  ' % (ServerList,SystemUser,ServerList)
        os.system(Modify_ServerList_Permission)
	os.system(Compress) # tar the server list
	while True:
		try:
			EncryptCmd='gpg -c %s' % CompressedFile
			BackupOldGpg = 'mv %s.gpg %s.gpg.bak' %(CompressedFile,CompressedFile)
			os.system(BackupOldGpg)
			CMD=os.system(EncryptCmd)
			if CMD != 0:
				print '\n\033[31;40;1mError: something wrong with setting password,try again.\033[0m'
				sys.exit()
			else:
				print '\nNew password has been set, exit'
				break

		except:
			print '\nPassword must be set before exit the program.' 
			continue
	print '---------------------------------'
	
def MD5Check():
	Md5File='%s/conf/.md5.txt' % WorkDir
	LoadSucess=False
	while not LoadSucess:
		try:
			file(Md5File)
			LoadSucess=True
		except IOError:
			print '\033[31;40;1mError++:password file lost,rebuild...\033[0m'
			Gen_Md5FileCmd='md5sum %s/* > %s/conf/.md5.txt' % (ServerList,WorkDir)
                        os.system(Gen_Md5FileCmd)
	Size_Md5 = os.stat(Md5File).st_size
	if Size_Md5 ==0:print 'Md5 file crashed.'
		
	os.system('rm -rf %s/conf/.md5.log' % WorkDir)
	Md5CheckCmd='md5sum -c %s > %s/conf/.md5.log' % (Md5File,WorkDir)
	os.system(Md5CheckCmd)
	#os.system('touch %s/lfflla' %ServerList)
	
	CurGroupList = os.listdir(ServerList)
	if len(OriGroupList) == len(CurGroupList):
		print 'Exiting the program.....\nDetecting configuration file changes.............'
	else:
		msg= '\033[34;1mGroup list changed.....you need to set the new encrypt password.\033[0m'
		print msg
		RecordLog.op_log(msg)
		ModifyMd5File = "sed  -i 's/OK/NO/g' %s/conf/.md5.log" % WorkDir
		os.system(ModifyMd5File)
	#Check group numbers,encrypt if numbers of group changed
	f=file('%s/conf/.md5.log' %WorkDir)
	while True:
		line=f.readline()
		if len(line)==0:break
		if line.split()[1] != 'OK':
			print 'File Has been changed'
		        # Gernerate MD5 checking file
        		Gen_Md5FileCmd='md5sum %s/* > %s/conf/.md5.txt' % (ServerList,WorkDir)
			os.system(Gen_Md5FileCmd)
			
			#Call Encrypt function
			msg = '\033[33;40;1mGroup List has been dectected changed,you need to set up new password to encrypt!\033[0m\n'
			RecordLog.op_log(msg)
			print msg
			time.sleep(1)
			Encrypt()
			RecordLog.op_log('TriAquae logout')
			break
	BackupMd5File = 'cp -rp %s/conf/.md5.txt %s/conf/.md5.txt.bak'	%(WorkDir,WorkDir)			
	os.system(BackupMd5File)
	f.close()
	#IF no file is been changed ,just delete user data and not need encrypt again.
	RemoveListDir='rm -rf %s/*' % ServerList
        os.system(RemoveListDir)
	RemoveCompressedFile='rm -rf  %s/conf/server_list.tgz' % WorkDir
        os.system(RemoveCompressedFile)


	
def Decrypt():
	EncryptedFile='%s/conf/server_list.tgz.gpg' % WorkDir
	DecryptCmd='gpg -o %s/conf/list.tgz -d %s'  % (WorkDir,EncryptedFile)
	print HeadLine  	
	CMD=os.system(DecryptCmd)
	if CMD != 0:
		msg = '\n\033[31;40;1mError:wrong password!\033[0m'
		print msg
		RecordLog.op_log(msg)
		sys.exit()
	else:
		print 'Right'
		RecordLog.op_log('\033[36;1mUser login TriAquae\033[0m')
		Uncompress='tar xvzf %s/conf/list.tgz -C %s/conf  >/tmp/TriAquae.temp' %(WorkDir,WorkDir)
		os.system(Uncompress)
		RemoveCompressedFile='rm -rf  %s/conf/list.tgz' % WorkDir
		os.system(RemoveCompressedFile)
		global OriGroupList
		OriGroupList=os.listdir(ServerList)
		Gen_Md5FileCmd='md5sum %s/* > %s/conf/.md5.txt' % (ServerList,WorkDir)
                os.system(Gen_Md5FileCmd)

#Decrypt()		
#Encrypt()	
#time.sleep(15)	
#MD5Check()
#Decrypt()
