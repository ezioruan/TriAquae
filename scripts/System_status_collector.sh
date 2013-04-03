#!/bin/bash
#for LoadAvg
System_date=$(date)
Vmstat_log=/tmp/system_vmstat.txt
sys_status_log=/tmp/system_status.log
echo '' > $sys_status_log
vmstat 3 10 > $Vmstat_log
DiskSpeed=$(hdparm -t /dev/sda)
IP_addr=$( /sbin/ifconfig | grep 'inet addr:'| grep -v '127.0.0.1' |cut -d: -f2 | awk '{ print $1}')
CPU=$( grep 'model name' /proc/cpuinfo |head -n1|cut -d: -f2)
CpuCores=$(grep '^processor' /proc/cpuinfo |wc -l)
/usr/bin/top -n1 >/tmp/system_top.txt
SysTasks=$(/usr/bin/top -n1 |grep '^Tasks:')
Uptime=$(uptime)
#sleep 2
TotalMem=$(free -m|grep -i '^Mem'|awk '{print $2}')

echo -e "\033[32;40;1m
System Date: $System_date
IP: $IP_addr
CPU: $CPU       Cores: $CpuCores
TotalMem MB: $TotalMem
Up time: $Uptime 
DiskSpeed: $DiskSpeed
System $SysTasks\033[0m" > $sys_status_log
echo -e "-----------------------------------------------------------------------------------------------" >> $sys_status_log

Avg_5=$(sar -q 1 2|tail -n1|awk '{print $5}')
Avg_1=$(sar -q 1 2|tail -n1|awk '{print $4}')
AlertAvg=`echo $CpuCores*2|bc`


#for IO wait

IOavg=$(sed -n '3,13p' $Vmstat_log|awk '{sum+=$16} END {print sum/NR }')
IOalert=40
IOmax=$(sed -n '3,13p' $Vmstat_log|awk '{print $16 }' |sort -n|tail -n1)


#for Memory
Swap_so=$(sed -n '3,13p' $Vmstat_log |awk '{print $8}' |sort -n |tail -n1) #paged out swap
Swap_so_alert=10
TotalSwap=$( free -m|grep -i '^Swap:'|awk '{print $2}')
Swap_so_avg=$(sed -n '3,13p' $Vmstat_log|awk '{sum+=$8} END {print sum/NR }')
Swap_used=$(sed -n '3,13p' $Vmstat_log |awk '{print $3}' |sort -n |tail -n1)
Swap_used_MB=$(echo $Swap_used/1000 |bc)
Swap_alert=$(echo $TotalMem/20 |bc) # %5 of total memory

SuggestMem=$( echo $TotalMem/10*6 |bc)
MemUsed=$(free -m|grep -i '^-/+'|awk '{print $3}')
MemAlert_Threadhold=$(echo $TotalMem/10*8.5 |bc)

#for CPU
Cpu_idle_Avg=$(sed -n '3,13p' $Vmstat_log|awk '{sum+=$15} END {print sum/NR }') #cpu idle time
SuggestIdle=50
MinIdle=$( sed -n '3,13p' $Vmstat_log|awk '{print $15}' |sort -n|head -n1)
IdleAlert=20




######

echo -e "
Load_Avg(5m):             $Avg_1          <  $CpuCores            $Avg_5                $Avg_1          $AlertAvg
IO_wait%:                 $IOavg        <  20                   $IOavg                  $IOmax          $IOalert
Memory_MB:                $MemUsed        <  $SuggestMem        $MemUsed                $MemUsed        $MemAlert_Threadhold
Swap_MB:                  $Swap_used_MB      <  0                  $Swap_used_MB              $Swap_used_MB      $Swap_alert
SwapPageOut/s:            $Swap_so        <  0                  $Swap_so_avg            $Swap_so        $Swap_so_alert
Cpu_Idle%:                $Cpu_idle_Avg   >  $SuggestIdle         $Cpu_idle_Avg           $MinIdle        $IdleAlert "  >>$sys_status_log
