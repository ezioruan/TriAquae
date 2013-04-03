#!/usr/bin/python
import time,sys
#time.sleep(20)

def Analyzer(sysinfo):
        try:
                Index=line.split()
                IndexAvg_30s = float(line.split()[4])
                IndexSug = float(line.split()[3])
                IndexAlert = float(line.split()[6])
                Operator = line.split()[2]
                NewLine = Index[0]+ '\t' +Index[1] + '\t\t' + Index[2]+' '+Index[3]+'\t\t'+Index[4]+'\t\t'+Index[5]+'\t'+Index[6]
                Dangerous = NewLine + '\t\tDangerous'
                High = NewLine + '\t\tHigh'
                Good = NewLine + '\t\tGood'
                if Operator == '<':
                        if IndexAvg_30s >= IndexAlert:
                                print '\033[31;40;1m%s\033[0m' % Dangerous
                        elif IndexAvg_30s > IndexSug:
                                print '\033[33;40;1m%s\033[0m' % High
                        else:
                                print '\033[32;40;1m%s\033[0m' % Good

                elif Operator == '>':
                        #print '-----------------------------------------------------------------'
                        if IndexAvg_30s <= IndexAlert:
                                print  '\033[31;40;1m%s\033[0m' % Dangerous
                        elif IndexAvg_30s <= IndexSug:
                                print  '\033[33;40;1m%s\033[0m' % High
                        else:
                                print  '\033[32;40;1m%s\033[0m' % Good
	except:print 'Error: some values did not find in the source log file,please check .'
#Analyzer('a')
LogName = sys.argv[1]

f=file(LogName)
RunNext = 0
print '----------------------------------\033[32;40;1mSystem Capacity Analyzer\033[0m ----------------------------------------'
while True:
        line=f.readline()
        if len(line)==0:break
	if line.startswith('\n'):continue
        if line.startswith('-----'):
                RunNext=1
		print '-------------------------------System Running Status (30seconds)-----------------------------------'
                print  "Index_Name\tRunning_index\tSuggest_num\tAverage_30_sec\tMax\tThreshold\tStatus\n"

		continue
        if RunNext == 1:
                Analyzer(line)
                continue
        print line,


