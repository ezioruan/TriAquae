#!/usr/bin/python
import sys,os,time
option=sys.argv
build_file='build.cfg'

def setup_build():
	try:
		option[1]
	except IndexError:
		print '\nError:no argument detected,use --help for helps\n '
		sys.exit()
	if option[1] == 'build':
		try:
                	option[2]
        	except IndexError:
                	print '\nError:You must specify where to install this program\n'
			sys.exit()

		if  option[2].startswith('--prefix='):
			print 'Start to check pre-installation environment...................................\n'
			while True:
				try:
					Dir=option[2].split()[0][9:] #pick up direcotry name
					if option[2].split()[0][-1] == '/':
						RealDir=option[2].split()[0][9:-1]
					else:
						RealDir=Dir	
					os.lstat(Dir)
					f = file(build_file,'w')
					record_dir='WorkingDir: %s\n' % RealDir
					f.write(record_dir)
				
					# Check modules
					'''try:
						import hashlib
						record_module_hashlib='hashlib: Yes\n'
						f.write(record_module_hashlib)	
					except ImportError:
						record_module_hashlib='hashlib: No\n'
						f.write(record_module_hashlib)
						print 'Error: no module named hashlib,you need install it manually'
					'''

                                        # Check module Crypto
                                        try:
                                                import Crypto
                                                record_module_Crypto='Crypto: Yes\n'
                                                f.write(record_module_Crypto)
                                        except ImportError:
                                                record_module_Crypto='Crypto: No\n'
                                                f.write(record_module_Crypto)

					# Check module paramiko
					try:
                                                import paramiko
                                                record_module_paramiko='paramiko: Yes\n'
                                                f.write(record_module_paramiko)
                                        except ImportError:
                                                record_module_paramiko='paramiko: No\n'
                                                f.write(record_module_paramiko)

				except OSError:
					CreateDir=os.system('mkdir -p %s' % Dir)
					if CreateDir == 0:
						print '\033[31;40;1mdirecotry not exsit,creating successful........\033[0m'
						continue 
					else:
						print 'Error: directory not exist and has no permission to create.'
						sys.exit()
				f.close()
				time.sleep(3)
				print "If no error printed out , you can run '\033[32;40;1mpython setup.py install\033[0m' to install the program \n"
				break
		else:
			print '\nError:You must specify install directory for this program\n'
	
	elif option[1].startswith('--help'):
		print '''
	--help		Show helps
	build --prefix=dir	Check and prepare the pre-installation environment
	install		install software'''
	elif option[1] == 'install':
		#print 'Starting to install software on the system.......'
		#try:
			f = file(build_file)
			while True:
				line = f.readline()
				if len(line) ==0:break
				name=line.split()[0]
				name_info=line.split()[1]
				'''if name.startswith('hashlib'):
					if name_info == 'No':
						print '\nError: no module named hashlib found in the system,please manually install it.'''
						#sys.exit()
				
				if name.startswith('paramiko'):
					if name_info == 'No':
						print '\nStart to install paramiko automatically.......'
						os.system('tar xvzf modules/paramiko-1.7.7.1.tar.gz')
						os.system('cd paramiko-1.7.7.1;python setup.py build && python setup.py install')
						try:
							import paramiko
						except ImportError:
							print 'Error:module paramiko install failed ,please install it manually.'
							sys.exit()
				elif name.startswith('Crypto'):
					if name_info == 'No':
						print '\nStart to install Crypto automatically.......'
						os.system('tar xvzf modules/pycrypto-2.6.tar.gz')
                                                os.system('cd pycrypto-2.6;python setup.py build && python setup.py install')
						try:
                                                        import Crypto 
                                                except ImportError:
                                                        print 'Error:module Crypto install failed ,please install it manually.'
                                                        sys.exit()
				elif name.startswith('WorkingDir:'):
					WorkingDir=name_info


				# Copy sourcecode to workding directory
			FileCopy='cp -rp bin conf INSTALL.txt include logs modules scripts %s' % WorkingDir
			print 'Extract files to working directory...\n'
			SetDirVariable= 'WorkDir = "%s" ' % WorkingDir
			print SetDirVariable
			SetDirCmd = "sed -i '2i%s'  %s/conf/global_env.py " %(SetDirVariable,WorkingDir)
			SetDirCmd_2 = "sed -i '2i%s'  %s/bin/TriAquae_console " %(SetDirVariable,WorkingDir)
			SetDirCmd_3 = 'cp -rp %s/conf/global_env.py %s/include/' %(WorkingDir,WorkingDir)
			os.system(FileCopy)
			os.system(SetDirCmd)
			os.system(SetDirCmd_2)
			os.system(SetDirCmd_3)
			
			time.sleep(3)
			print '\n\033[32;1mComplete ok\nNow you can run %s/bin/TriAquae_console to start manage your network.\nDefault login password : admin \n\nEenjoy!\033[0m' %WorkingDir		

	else:print '\nWrong option, try --help for helps\n'
setup_build()
