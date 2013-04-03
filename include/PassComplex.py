#!/usr/bin/python

def Complex():
	UpperLetter='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	LowerLetter='abcdefghijklmnopqrstuvwxyz'
	Digital='0123456789'
	while True:
		InputPass=raw_input('New password:')
		if len(InputPass) < 6:
			print 'Bad password,too short ,at least 6 letters!'
			continue
		RepeatPass=raw_input('Retype New password:')
		TestPass=True
		TestPassNum=0
		TestPassUpper=0
		TestPassLower=0
		if InputPass == RepeatPass:
			for letter in RepeatPass:
				if letter in Digital:
					TestPassNum =1	
				else:
					pass

			for letter in RepeatPass:
                                if letter in UpperLetter:
                                        TestPassUpper=1;
                                else:
                                        pass 
			for letter in RepeatPass:
                                if letter in LowerLetter:
                                        TestPassLower=1
                                else:
                                        pass

			if TestPassNum==0:
				print 'Bad password,new password takes at least 1 integer!'
				continue
		        if TestPassUpper==0:
                                print 'Bad password,new password takes at least 1 uppercase!'
                                continue
		        if TestPassLower==0:
                                print 'Bad password,new password takes at least 1 lowercase!'
                                continue
			print '\033[33;40;1mNew password will be set on remote servers\033[0m'
			return RepeatPass		

		else:
			print 'Password not match,try again!'
			continue
		
#Complex()
