#!/usr/bin/python
import sys,os,time
import global_env
WorkDir = global_env.WorkDir

#Configuration part!
################################################################################
JobRunner = '%s/bin/JobRunner' % WorkDir
TestMsg = '''        ------------This Is Test Menu------------\n
you can configure your own menu and run your own jobs,it will run "uptime"
command on remote servers,edit myMenu.conf in conf/ dir to customize your 
own menu.
--------------------------------------------------------------------------\n'''

menu1 = {
	'name'		: 'My first menu ', #name of the menu,Example: 'system booting log'
	'description'	: TestMsg,     #Example:'This feature will collect system booting log  
	'run_engine'	: JobRunner,   #engine to run job
	'run_interval'	: 0,           #Suggest: 5 , set if to 10 if more than 100 clients,  
	'excute_sequence'	: [
					"-r  'uptime'",
					#"-s  /tmp/s.list  /tmp/remote_file.txt",
					#"-g /tmp/remote_file.txt  /tmp/local_file.txt "
		 		  ] 
	
}

menu2 = {
	'name'	:'My second menu',
	'description'	:'restart apache service',
	'run_interval'	: 5,
	'run_engine'	: JobRunner,
	'excute_sequence'	: []
	
}

menu3 = {

	'name':'collect user last login info',
	'description'	: 'This is another test menu!!!',
	'run_interval'	:6,
	'run_engine'	:JobRunner,
	'excute_sequence'	: [
			"-r 'last'"
		]
}
## add your menu to below list if you want to enable it 
applyMenu = [menu1,menu2,menu3] 

#------------------------------------------------------------------------------






################################################################################
##Program part,don't modify it if you are not really know what you are doing.
def menuCheck():
	'''Check correctness of all custmized menus before run it'''
	menuIndex = 0
	for menu in applyMenu:
		
		try:
			menu['excute_sequence']
			key_name = ['name','description','run_engine','run_interval']
			for name in key_name:
				if menu.has_key(name):
					pass
					
				else:
					print name,'not exist in menu sequense %s ,please check!' % menuIndex
					sys.exit()
			if len(menu['name'].strip()) == 0:
				print 'menu name must be set in menu sequence %s' % menuIndex
		except KeyError:
			print 'parameter error in the menu sequence %s,please check whether the [ excute_sequence ] parameter has been set' % menuIndex
			return 'err'	
		except NameError:
			print 'can not find menu name: %s' % applyMenu[applyMenu.index(menu)]
			return 'err'
		menuIndex +=1
def RunJobSequence(menu,groupName):
	'''check task excution sequence before run'''
	for index,parameter in menu.items():
		#print index,'---->',parameter
		job_interval = menu['run_interval']
		if index == 'excute_sequence':
			if len(menu[index]) == 0: #check if there's value in excute_sequence list
				print 'No job has been set for %s,please check ' % index 
			else:
				for job in menu[index]:
					command = job.strip()
					addGroupNameInCommand = "%s %s %s %s " %(JobRunner,command[:2],groupName,command[2:])
					#print addGroupNameInCommand
					os.system(addGroupNameInCommand)
					time.sleep(job_interval)	

def menuShow(groupName):
	passCheck = 'yes'
	if menuCheck() == 'err':
       		print '\033[31;1mError:Parameter mistake,please repaire the error before run it,exit!\033[0m'
		passCheck = 'no'	
		return passCheck
	menuDic = {}
	menuNum = 1
	
	while True:
		if passCheck != 'yes':break
		for menu in applyMenu:
			print "\t\033[36;1m%s. %s\033[0m" % (menuNum,menu['name'])
			menuDic[menuNum] = menu['name']
			menuNum +=1
		menuNum = 1

		try:
			menu_option = int(raw_input('[Please choose an option to proceed-->#]'))
			if menu_option == 0:raise ValueError
			menuNumInMenuList = menu_option - 1
			print '''\033[36;1m\n%s\033[0m\nTask will start running after 5 seconds,type Ctrl + c to cancel''' % applyMenu[menuNumInMenuList]['description']
			time.sleep(5)
			RunJobSequence(applyMenu[menuNumInMenuList],groupName)
			menuDic.clear()
			
		except ValueError:
			print '\033[31;1mWrong option\033[0m'
		except IndexError:
                        print '\033[31;1mWrong option\033[0m'
		except KeyboardInterrupt:
			print '\nForce exit!'
			break

def runCheck():
	if __name__ == '__main__':
		try:
			if sys.argv[1] == '--check':
				print '\nYou need to login TriAquae_console before you run check option'
			elif sys.argv[1] == '--help':
				print '''\n
	usage:	 python myMenu.conf --check GroupName
	example: python myMenu.conf --check Group_beijing'''		
			else:
				print 'Wrong option, try --help for detail'
				sys.exit()
		except IndexError:
			print 'no argument detected.'
		try:
			groupName = sys.argv[2]
			menuShow(groupName)
		except IndexError:
			print '\n\033[31;1mError:you need to specify groupname after --check option\033[0m'
runCheck()
