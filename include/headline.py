import textwrap,Termina_size

HeadLine='''\033[32;1m
|=============================================================================================================================|
|															      |
|						       TriAquae 2.0							      |
|                                                    As good as water							      |
|														              |
|															      |				
|\tWelcome to log in TriAquae 2.0 management console,you will be able to manage many servers through this small and      |
|\tlight software.													      |
|\033[0m															      |	
|\t\033[31;1mPlease be careful with your opreations because right now the key of managing the whole network is in your hand.	      |	
|\tYou must be very clear about any instructions you input before you send them to this cosole.\033[0m\033[32;1m	      		      |	
|															      |
|															      |
|											Report bug: Triaquae@gmail.com        |
|_____________________________________________________________________________________________________________________________|
\033[0m'''

HeadLine100 = '''\033[32;1m
|==============================================================================================|
|											       |
|					TriAquae 2.0					       |
|				      As good as water					       |
|											       |
|  Welcome to log in TriAquae 2.0 management console,you will be able to manage many servers   |
|  through this small and light software.                                                      |     
|\t\033[0m                                                                                       |
|  \033[31;1mPlease be careful with your opreations because right now the key of managing the whole      | 
|  network is in your hand.You must be very clear about any instructions you input before      | 
|  you send them to this cosole.\033[0m\033[32;1m        		                         	       |
|                                                                                              |
|                                                                                              |
|                                                        Report bug: Triaquae@gmail.com        |
|______________________________________________________________________________________________|
\033[0m'''

HeadLine80 =  '''\033[32;1m
|==============================================================================|
|                                                                              |
|                                   TriAquae 2.0                               |
|                                 As good as water                             |
|                                                                              |
|  Welcome to log in TriAquae 2.0 management console,you will be able to       |
|  manage many servers through this small and light software.                  |
|\033[31;1m                                                                              |
|  Please be careful with your opreations because right now the key of         |
|  managing tnetwork is in your hand.You must be very clear about any          | 
|  instructions you input before you send them to this cosole.                 |
|\033[0m\033[32;1m                                                                              |
|                                         Report bug: Triaquae@gmail.com       |
|______________________________________________________________________________|
\033[0m'''

def head_line():
	T_size = Termina_size.terminal_size()
	if T_size[0] >= 127:
		print HeadLine
	elif T_size[0] >= 100:
		print HeadLine100 
	else: 
		print HeadLine80
		#print T_size

head_line()


