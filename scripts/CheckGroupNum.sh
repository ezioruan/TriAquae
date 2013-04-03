#!/bin/bash


CurGroupNum=$(ls server_list|wc -l)
OriGroupNum=$(cat .md5.txt|wc -l)

if [ $CurGroupNum = $OriGroupNum ];then
	exit 0
else
	exit 1
fi
