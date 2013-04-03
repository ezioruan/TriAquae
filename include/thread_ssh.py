#!/usr/bin/python
'This program connect remote server through ssh'
import paramiko,threading,time,os,sys,socket
#import FileTransfer
import global_env
WorkDir = global_env.WorkDir
DelimiterLine = '\033[32;49;1m_______________________________________________________________________________________________\033[0m'
GroupDir = '%s/conf/server_list' % WorkDir
GroupList = os.listdir(GroupDir)
ServerList = ''
RecordLog=global_env.g_env()

def CountLine(groupName):
	fileName = '%s/%s' %(GroupDir,groupName)
	lineNumber = 0
	f = file(fileName)
	while True:
		line = f.readline()
		if len(line) == 0:break
		if line.startswith('#'):continue
		lineNumber += 1
	return lineNumber 
#print CountLine('BJ')
class CmdBind:
	cmd_count_result = {}
	cmd_count_result['Error'] = []
	cmd_count_result['Success'] = []
	def ssh2(self,ip,username,password,cmd):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,22,username,password,timeout=5)
			stdin,stdout, stderr= ssh.exec_command(cmd)
			#stdin.write('\n')
			Output = stdout.readlines()
			for i in Output:
				msg = i
				print msg,
				RecordLog.op_log(msg)
				
			msg= '------------------------------------[%s]\t\033[33;49;1mOK\033[0m\n' % (ip)
                        RecordLog.op_log(msg)
                        print msg
			CmdBind.cmd_count_result['Success'].append(ip)

			ssh.close()
		except:
			msg= '------------------------------------[%s]\t\033[31;49;1mConnection Error\033[0m \n' % (ip)
			RecordLog.op_log(msg)
			print msg
			CmdBind.cmd_count_result['Error'].append(ip)
	def CmdExcution(self,single_thread=0,multi_thread=0,server_list_file=0):
		#Initate the command excution result count 
        	CmdBind.cmd_count_result['Error'] = []
        	CmdBind.cmd_count_result['Success'] = []
	
		try:
			if multi_thread == 1:
				LimitedCmd=['shutdown','reboot','rm','halt','dd','fsck']
				
				while True:
					cmd2 = raw_input('\033[32;49;1m[Please input your command,Ctrl + C to go back:]\033[0m')
					cmd = cmd2.strip()	
					if cmd.startswith('more'):
						print 'command not supported,try "cat" instead!' 
						continue
					if cmd == 'q':continue
					elif len(cmd) == 0:continue
					RunCmd=True;
					RecordLog.op_log("\033[36;1mUser Input: %s \033[0m" % cmd)
					for i in LimitedCmd:
						if  i in cmd:
							choice=raw_input('\n\033[33;40;1mThe command you input might be dangerous,do you really want to run it on all the servers?(y/n)\033[0m')
							if choice == 'y':
								break
							else:
								RunCmd=False
								break
					if RunCmd is False:
						print 'Exit,back to main menu.'
						break		
						
					if len(cmd)==0:continue
					threads = []
					server_L_file = '%s/%s' % (GroupDir,server_list_file) #locate server list file
	
					ServerList = file(server_L_file) #Locate & open server list file 
					print '------------------------------------\033[36;1mFeedback\033[0m-----------------------------------'
					while True:
						try:
							line = ServerList.readline()
							if len(line) == 0:break
							if line.startswith('#') is True:continue
							#if line.startswith('getsysteminfo'):
								
							ip_addr = line.split()[0]
							try:
								line.split()[2]
							
							except IndexError:
								msg= '\033[31;40;1mError :no username or passwd found for ip: %s,please check\033[0m' % ip_addr  
								RecordLog.op_log(msg)
                        					print msg
								pass
	
							#IsPassExist == 1
							username =  line.split()[1]
							password =  line.split()[2]
							if len(ip_addr) == 0:break
							a= threading.Thread(target=CmdBind().ssh2,args=(ip_addr,username,password,cmd))
							a.start()

						except IndexError:
							print 'Error: index error'
					Job_total =  CountLine(server_list_file)
					if Job_total < 100:time.sleep(5)
					else:time.sleep(10)
					Job_success = len(CmdBind.cmd_count_result['Success'])
					Job_failed = len(CmdBind.cmd_count_result['Error'])
					Job_unknown = Job_total - Job_success - Job_failed
					print '\033[41;40;1mCommand excution task completed\033[0m'
					msg= '\033[36;1mResult# Total: %s  Success: %s Failed: %s Unkown: %s\033[0m\nSee operation.log for details!' %(Job_total,Job_success,Job_failed,Job_unknown)
					print msg
					RecordLog.op_log(msg)
                			CmdBind.cmd_count_result['Error'] = []
                			CmdBind.cmd_count_result['Success'] = []
		except KeyboardInterrupt:
			print 'Go Back'

	def FileTransfer(self,ip,user,password,file1,file2,FileSend = 0):
        	'''if FileSend == 0 , send file to client, else get file from clients'''
		try:
			CmdBind.cmd_count_result['Error'] = []
                	CmdBind.cmd_count_result['Success'] = []	

        		tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        		tcpsock.settimeout(5)
        		tcpsock.connect((ip,22),)
        		ssh = paramiko.Transport(tcpsock)
        		ssh.connect(username=user,password=password)
	
       			sftpConnect=paramiko.SFTPClient.from_transport(ssh)
			'''except:
				msg= 'Error: timout when try to connect remote server: %s' % ip
	                        RecordLog.op_log(msg)
        	                print msg'''

        		if FileSend == 1:
                		print '--------------------------------------'
				file3 =  '%s_%s' %(file1,ip)
				msg= 'Getting file %s  from %s....' %(file2,ip)
				RecordLog.op_log(msg)
                                print msg
	
                		sftpConnect.get(file2,file3)
				msg = '\033[32;40;1mDownload file successful,save to local: %s \033[0m' % file3
                                RecordLog.op_log(msg)
                                print msg
				CmdBind.cmd_count_result['Success'].append(ip)

        		else:
                		msg= '\033[32;40;1mSending File to %s......\033[0m' %ip
				RecordLog.op_log(msg)
                        	print msg
                		sftpConnect.put(file1,file2)
				print '\033[32;40;1mFile has been sending to %s successfully.\033[0m' % ip
				CmdBind.cmd_count_result['Success'].append(ip)
		except IOError:
			msg= '\033[31;40;1mError: exception triggered when connectting remote host: %s\n\tplease check to make sure client is reachable or has the specified file on it\033[0m' %(ip)
		 	RecordLog.op_log(msg)
                        print msg
			CmdBind.cmd_count_result['Error'].append(ip)
		except :
			msg= 'Error: timout when try to connect remote server: %s' % ip
			RecordLog.op_log(msg)
                        print msg
			CmdBind.cmd_count_result['Error'].append(ip)
	def Run_FileTransfer(self,file1,file2,Server_list,FileSend = 0):
		server_list_file = '%s/%s' % (GroupDir,Server_list) #locate server list file
                OpenServerList = file(server_list_file) #open server list file
        	while True:
                	line= OpenServerList.readline()
                	if len(line) == 0:break
                	if line.startswith('#') is True:continue
			ip = line.split()[0]

                        try:
                                line.split()[2]
                		user = line.split()[1]
                		password = line.split()[2]	
                		threads = [] # sending or getting files by threading
                		a=threading.Thread(target=CmdBind().FileTransfer,args=(ip,user,password,file1,file2,FileSend))
                		a.start()

                        except IndexError:
                                msg= '\033[31;40;1mError :no username or passwd found for ip: %s,please check\033[0m' % ip
                                RecordLog.op_log(msg)
                        	print msg
				continue
			except:print 'Warning: transmission warning'
		print '\033[41;40;1mFile transmission task excution completed!\033[0m' 
		Job_total =  CountLine(Server_list)
		if Job_total < 100:time.sleep(5)
		else:time.sleep(10)
                Job_success = len(CmdBind.cmd_count_result['Success'])
                Job_failed = len(CmdBind.cmd_count_result['Error'])
                Job_unknown = Job_total - Job_success - Job_failed
                msg= '\033[36;1mResult# Total: %s  Success: %s Failed: %s Unkown: %s\033[0m\nSee operation.log for details!' %(Job_total,Job_success,Job_failed,Job_unknown)
		print msg
		RecordLog.op_log(msg)
	def Run_Scripts(self,Server_list,Run_Command):
		server_list_file = '%s/%s' % (GroupDir,Server_list) #locate server list file
                OpenServerList = file(server_list_file) #open server list file
		print 'Start run commmand on remote servers......................'
                while True:
                        line= OpenServerList.readline()
                        if len(line) == 0:break
                        if line.startswith('#') is True:continue
                        ip = line.split()[0]
                	try:
                        	line.split()[2]
			        user = line.split()[1]
        	                password = line.split()[2]
				
                        	threads = [] # sending or getting files by threading
                        	a= threading.Thread(target=CmdBind().ssh2,args=(ip,user,password,Run_Command))
				a.start()

                        except IndexError:
                                msg= '\033[31;40;1mError :no username or passwd found for ip: %s,please check\033[0m' % ip
                               	RecordLog.op_log(msg)
                        	print msg
				continue 
			except:
				print 'error occured'
		print '\033[41;40;1mTask excution completed\033[0m'
		Job_total =  CountLine(Server_list)
                if Job_total < 100:time.sleep(5)
                else:time.sleep(10)
                Job_success = len(CmdBind.cmd_count_result['Success'])
                Job_failed = len(CmdBind.cmd_count_result['Error'])
                Job_unknown = Job_total - Job_success - Job_failed
                msg= '\033[36;1mResult# Total: %s  Success: %s Failed: %s Unkown: %s\033[0m\nSee operation.log for details!' %(Job_total,Job_success,Job_failed,Job_unknown)
                print msg
                RecordLog.op_log(msg)

		#print '\033[41;40;1mTask excution completed\033[0m'
#T=CmdBind()
#T.CmdExcution(0,1,'Group_Beijing')		
