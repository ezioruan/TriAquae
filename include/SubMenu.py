#!/usr/bin/python
import global_env
WorkDir = global_env.WorkDir

Menu = '''\033[32;40;1m
	1. Command excution on mutiple servers
	2. Run crontab for mutiple servers 
	3. Send/get file 
	4. System management
	5. Check client connection status
	6. App deployment (still under development...)\033[0m
	\033[36;1m7. My menu\033[0m\n'''
SubFileMenu = '''\033[32;40;1m	1. Send file to clients
	2. Get file from clients
	3. File synchronization (still under development...)\033[0m\n'''
SysManagementMenu = '''\033[32;40;1m	1. Collect system running status
	2. Collect system hardware information
	3. Collect system log (still under development...)
	4. System capacity analyzer (still under development...)
	5. Change system password\033[0m\n '''
ClientConnection = '''\033[32;40;1m	1. Start run client connection test
			\033[0m'''

AppInstall='''\033[33;40;1mThis feature is still under developing status,it will achive folow functions after released:\n
	1. Allow users to customize thier own submenu
	2. Customize your own software which needs to be automatically installed on all the clients
	3. Define your own job crontab,like collect information,excute scripts and etc.
	4. .....\033[0m
	
\033[31;40;1m	Got a new idea of this feature? send email to Triaquae@gmial.com,if we take your suggestion,\nyou will see it in the next relased version!\033[0m'''
class SubMenu:
	def ShowMenu(self):
		print Menu
        def ListMenu(self,MenuNumber):
		if MenuNumber == 2:
			print '''\033[33;40;1mTwo steps to configure a scheduled job:\n
\t1. type python %s/bin/JobRunner --help at bin dir to learn more information.
\t2. put JobRunner into local crontab
\nNotice: you need to create or copy a server list and put it into below location if the TriAquae_console is not running:\n%s/conf/server_list \033[0m''' %(WorkDir,WorkDir)
		
		if MenuNumber == 3:
			print SubFileMenu
		elif MenuNumber == 4:
			print SysManagementMenu
		elif MenuNumber == 5:
			print ClientConnection
		elif MenuNumber == 6:
			print AppInstall			
		#elif MenuNumber == 7:
		
	#def ChooseOption(self,Number):
		
		
#a= SubMenu()
#a.ListMenu(Menu)
#a.ListMenu(SysManagementMenu)
#a.ListMenu(ClientManagementMenu)

