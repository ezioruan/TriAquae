import getpass,hashlib,sys,os
'''
pwd = getpass.getpass('password:')
print pwd
p=hashlib.md5(pwd)
if p.hexdigest() 
'''
PassFile = '.password'
StoredPass = open(PassFile).read()
ReTry = 0
if len(StoredPass)> 0:
	while True:
	        InputPass = getpass.getpass('password:')
        	SecretPass =hashlib.md5(InputPass)
		EncrptPass = SecretPass.hexdigest() 	
		if EncrptPass == StoredPass:
			print 'Password is correct!'
			break
		else:
			print 'Wrong password.'
			ReTry = ReTry + 1
			if ReTry == 3:
				print 'Too many wrong times,send alert to administrator.'
				sys.exit()	
			continue
else:
	while True:
		CreatePass = getpass.getpass('Input new password:')
		RepeatPass = getpass.getpass('Input the password again:')
		if CreatePass == RepeatPass:
			if len(CreatePass) < 8:
				print 'Password must more that 8 letters.'
				continue
			else:
				SecretPass1 = hashlib.md5(RepeatPass)
				DumpToFile = SecretPass1.hexdigest()
				SavePass = file(PassFile,'w')
				SavePass.write(DumpToFile)
				SavePass.close()
				print 'Password created successfully.'
				break		
		else:
			print "Password doesn't match, please try again."	

os.system('clear')
