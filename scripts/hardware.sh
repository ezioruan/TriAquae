#!/bin/bash

echo -e '\033[32;40;1mSystem_serial_number & Vendor Info:\033[0m '
dmidecode -t 1

getconf LONG_BIT |xargs  echo -e '\033[32;40;1mSystem version::\033[0m'
uname -a
echo -e '\033[32;40;1mRaid Info:\033[0m '
lspci|grep 'RAID' 

echo -e '\033[32;40;1mEthernet Interface Info:\033[0m '
lspci|grep 'Ethernet'

echo -e '\033[32;40;1mNumber of Memmory slots on server:\033[0m '
dmidecode |grep -A16 "Memory Device$"|grep 'Size'|wc -l

echo -e '\033[32;40;1mPhysical Memory Info:\033[0m '
dmidecode -t 16  #mem

echo -e '\033[32;40;1mNumber of Physical Memory in slots Info:\033[0m '
dmidecode -t 17|grep 'Size' 

echo -e '\033[32;40;1mNumber of CPU cores Info:\033[0m '
cat /proc/cpuinfo |grep 'model name' |wc -l|xargs echo -e '\033[32;40;1mLogical CPU cores:\033[0m' #num of cores
cat /proc/cpuinfo |grep 'physical id'|uniq -c|wc -l |xargs echo -e '\033[32;40;1mPhysical CPU cores:\033[0m'



cat /proc/cpuinfo |grep 'model name' |head -n 1

cat /proc/cpuinfo |grep 'cpu cores'|head -n1

cat /proc/cpuinfo |grep 'cpu MHz' | awk -F":" '{print $2}' |xargs echo 'Cpu MHz:'

echo -e '\033[32;40;1mHard Disk Info:\033[0m '
cat /proc/scsi/scsi 
echo -e '-----------------Partition info-----------------'
fdisk -l
