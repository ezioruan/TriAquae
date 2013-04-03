#!/usr/bin/python
import os,sys,global_env
DelimiterLine = '''\033[32;49;1m  	   						   Powered by TriAquae 
________________________________________________________________________________\033[0m''' 
WorkDir=global_env.WorkDir
GroupDir = '%s/conf/server_list' % WorkDir
GroupList = os.listdir(GroupDir)
CountGroups = len(GroupList)
#TotalMenuNumber = 0 
RecordLog = global_env.g_env()
class Group:
	def ListGroup(self,Show_List = 0,Total_M_Number = 0,Dictionary=0):
		GroupList = os.listdir(GroupDir)
		global ServerDic 
		ServerDic = {}	
		G_num = 0 
		global Dic
		Dic = {}
		for group in GroupList: 
			Dic[ G_num ] =  group  # Add Group list to Dic dictionary
			G_num = G_num + 1
		if Show_List == 1:
			print DelimiterLine,'\n'
			for key in Dic:
				ServerNum='%s/%s' %(GroupDir,Dic[key])
				count = len(open(ServerNum,'rb').readlines( )) 
				
				print '\033[32;40;1m%s. %s [ \033[0m\033[36;1m%s \033[0m\033[32;1m]\033[0m ' % (key,Dic[key],count)  # Print Dic list 
			#print '\033[32;40;1m%s. All the Servers (still under development...)\033[0m ' % G_num
			print ' '
			print '%s. Modify Group ' % (G_num + 1 )
			print '%s. Add/Delete Server' % (G_num + 2)
			print '%s. Upload server list' % (G_num + 3)
			print DelimiterLine
		global TotalMenuNumber 
		TotalMenuNumber = G_num + 3 
		if Total_M_Number == 1: 
			return TotalMenuNumber 
		if Dictionary == 1:return len(Dic)
		#print DelimiterLine
	def ChooseGroup(self,Str_Number,Show_G_name=0):
		print DelimiterLine
		Number = int(Str_Number)
		if Number < CountGroups:
			print 'Servers in \033[36;1m%s\033[0m\n' % Dic[Number]
			if Show_G_name == 0:
				Group().ListGroupContent(Number)  # Print server list
			else:
				pass
			print DelimiterLine
			return Dic[Number]  # return the group name
		elif Number == TotalMenuNumber: # Modify Group option 
			print 'The group list file is under directory %s,you can modify the group content through edit those files ' % GroupDir
		
		print DelimiterLine
		
	def ListGroupContent(self,GroupNum):
		GroupFileName = '%s/%s' % (GroupDir, Dic[GroupNum])
		f = file(GroupFileName)
		#print f.read()
		S_num = 0
		print '\033[36;1mID  IP Address		Username\033[0m'
		while True:
			line = f.readline()
			if len(line) == 0:
				break
			if line.startswith('#') is True:continue
			IP=line.split()[0]
			User = line.split()[1]
			ServerDic[ S_num ] =  IP  # Add server item to ServerDic dictionary
			print '%s. %s 	%s ' %(S_num,ServerDic[S_num],User)
			S_num = S_num + 1
		
		#for S_key in ServerDic:
		#	print '%s. %s ' % (S_key, ServerDic[ S_key ])  # Print server list line
		f.close() 
	def ChooseServerRange(self,StartIP,EndIP):
		try:
			if StartIP < EndIP:
				print DelimiterLine
				for i in range(StartIP,EndIP):
					print 	i,'.', ServerDic[i]
		except KeyError:
			print '\033[32;40;1m Error :Out of range.\033[0m'
	def ListVariable(self,Vname):
		#TotalMenuNumber = Group().ListGroup.TotalMenuNumber
		print Vname	
	def AddGroup(self,G_name):
		NewGroupName = '%s/Group_%s' % (GroupDir,G_name)
		F = file(NewGroupName,'w')
		print 'Created group %s successful.' % G_name
		RecordLog.op_log('Created new group : \033[36;1m %s \033[0m' % G_name)
		#GroupDicKey = Group().ListGroup(0,0,1) 
		#Dic[GroupDicKey ] = NewGroupName  
		AddServer = raw_input('Do you want to add new server to Group \033[32;40;1m%s\033[0m [ Y / N ]:' % G_name)	
		if AddServer == 'Y' or AddServer == 'y':
			while True:
				NewServerIP2 = raw_input('Input new server IP or Hostname:')
				if len(NewServerIP2) == 0:continue
				while True:
					IP2_user = raw_input("Input newser's username:")
					if len(IP2_user) == 0:continue
					IP2_pass = raw_input("Input newser's password:")
					if len(IP2_pass) == 0:
						print 'Error: password cannot be empty,please try again.'
						continue
					else:break
				NewServerIP = '%s %s %s \n' % (NewServerIP2,IP2_user,IP2_pass) #Separate the IP into different line
				F.write(NewServerIP)
				RecordLog.op_log('Add new server %s to group %s' %(NewServerIP2,G_name))
				print 'New server \033[32;40;1m%s\033[0m added successfully.' % NewServerIP2
				KeepAddServer = raw_input('Keep on adding new server?:[ Y / N ]')
				if KeepAddServer == 'Y' or KeepAddServer == 'y':continue
				else:break
		F.flush()
		F.close()
	def DelGroup(self,G_name):
		GroupList =os.listdir(GroupDir)
		IsFileExist = G_name in GroupList
		if IsFileExist is True:
			print G_name
			D_option = raw_input('Are you sure you want to delete group\033[32;40;1m%s\033[0m [ Y / N ]: ' % G_name)
			if D_option == 'Y':
				GroupFile='%s/%s' % (GroupDir,G_name)
				os.system('rm -rf %s' % GroupFile)
				#del Dic[2]
				#print Dic
				print 'Deleted group %s\n ' % G_name
				RecordLog.op_log('Deleted Group %s' % G_name)
				#print '\033[31;40;1mGroup will be deleted from list after re-login.\033[0m'
			else:
				print '\033[33;40;1mNo action,back to main menu.\033[0m'
		else:
			print '\n\033[31;49;1mError+++: Wrong group name,check again.\033[0m\n'
	def RenameGroup(self):
		#while True:
			print '---------------'
			LoadSuccess=False
			while not LoadSuccess:
				Group_name=raw_input('Which group name do you want to change?:')
	                        GroupFile='%s/%s' %(GroupDir,Group_name)

				try:
					file(GroupFile)
					LoadSuccess=True
				except IOError:
					print '\033[31;1mGroup name not exist\033[0m'
			while True:
				NewGroupName2=raw_input('New name:')
				NewGroupName = NewGroupName2.strip()
				if len(NewGroupName)==0:continue
				New_G_file='%s/%s' %(GroupDir,NewGroupName)
				GroupRename='mv %s %s' %(GroupFile,New_G_file) 
				os.system(GroupRename)	
				msg= '\033[36;1m group name of %s changed to %s\033[0m' %(Group_name,NewGroupName)
				print msg
				RecordLog.op_log(msg)
				break
	def UploadServerList(self,GroupName,UploadList,update_option):
		#try:	
		print 'Uploading server list-------------------------------------------'
		NewList = file(UploadList)
		OldList = file(GroupName,update_option)
		while True:
			line = NewList.readline()
			if len(line) == 0:break
			if line.startswith('#') is True:continue
			OldList.write(line)
			print line,
		print 'New server list has successfully uploaded.'
		NewList.close()
		OldList.close()			
	def ServerManage(self,option='Add'):
		LoadSucess=False;
		while not LoadSucess:
			try:
				GroupName=raw_input('\nInput Group name which the server is in:')
				GroupFile='%s/conf/server_list/%s' %(WorkDir,GroupName)
				file(GroupFile)
				print '\033[32;40;1m------------------------Server List----------------------------\033[0m' 
				os.system("cat %s|awk '{print $1}'" %GroupFile)	
				LoadSucess=True
			except IOError:
				print '\n\033[31;40;1mNo such group name found,please try again.\033[0m'	
		if option == 'Add':
			f=file(GroupFile,'a')
                        while True:
                                NewServerIP2 = raw_input('Input new server IP or Hostname:')
                                if len(NewServerIP2) == 0:continue
                                while True:
                                        IP2_user = raw_input("Input newser's username:")
                                        if len(IP2_user) == 0:continue
                                        IP2_pass = raw_input("Input newser's password:")
                                        if len(IP2_pass) == 0:
                                                print 'Error: password cannot be empty,please try again.'
                                                continue
                                        else:break
                                NewServerIP = '%s %s %s \n' % (NewServerIP2,IP2_user,IP2_pass) #Separate the IP into different line
                                f.write(NewServerIP)
				RecordLog.op_log('Add new server %s to group %s' %(NewServerIP2,GroupName))
                                print 'New server \033[32;40;1m%s\033[0m added successfully.' % NewServerIP2
                                KeepAddServer = raw_input('Keep on adding new server?:[ Y / N ]')
                                if KeepAddServer == 'Y' or KeepAddServer == 'y':continue
                                else:
					f.close()
					break
				
		elif option == 'Del':
			#f=file(GroupFile)
			while True:
				f=file(GroupFile)
				print '\n\033[33;40;1mNotice: All matched IP adresses will be deleted,becare\033[0m'
				IP=raw_input('Input the server IP which you want to delete:')
				
				if len(IP) ==0:continue
				NotMatchedRow = 0
				while True:
					line = f.readline()
					if len(line) ==0:break
					OldIP=line.split()[0]
					if IP == OldIP:
						os.system("grep ^%s %s|awk '{print $1}'" %(IP,GroupFile))
						MatchNumbers=os.system("grep ^%s %s|wc -l|xargs echo -e '\033[33;40;1mmatched rows:\033[0m'" %(IP,GroupFile))
						DelAllMatches = raw_input('Do you want to delete all the matched rows?(y/n)')
						#NotMatchedRow = -1 # set NoteMatchedRow < 0
						if DelAllMatches == 'y':
							NotMatchedRow = -1 # set NoteMatchedRow < 0
							DelIP = "sed -i '/%s/d' %s" %(IP,GroupFile)
							os.system(DelIP)
						else:break
						msg = 'User deleted server from group %s' %GroupName
						RecordLog.op_log(msg)
						print 'IP has been deleted from group %s ' %GroupName
						
					else:
						NotMatchedRow += 1
				if NotMatchedRow > 0: print '\033[33;1m 0 matched rows!\033[0m'
#A=Group()
#A.ServerManage('Del')

		#except:
		#	print 'err'
#A = Group()
#A.UploadServerList('Group_2','/tmp/sh.list','a')
#A.ListGroup()
#A.ChooseGroup(1)
