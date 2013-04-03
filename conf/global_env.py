#!/usr/bin/python
#WorkDir = "/usr/local/TriAquae2.1.0" 
import time,sys
include = '%s/include' % WorkDir
conf = '%s/conf' % WorkDir
sys.path.append(include)
sys.path.append(conf)

op_log_file='%s/logs/operation.log' %WorkDir
excution_log_file='logs/excution_result.log'
date =time.strftime('%Y_%m_%d %H:%M:%S')
f=file(op_log_file,'a')
class g_env:
	
	def op_log(self,log):
		date=time.strftime('%Y_%m_%d %H:%M:%S')
		record = '%s   %s\n' %(date,log)
		f.write(record)
		#f.close()

