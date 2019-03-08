#!/bin/bash

path=/home/ctivan/weeklyreport/temp/
content=weekly_report
email1=kuraoka@yo-ren.com
email2=hugo.xiong@yo-ren.com
email3=chris.zhang@yo-ren.com
email4=weijen.lim@yo-ren.com
email5=nick.su@yo-ren.com
email6=amy.zhang@yo-ren.com
email7=bella.ma@yo-ren.com
email8=zoe.zhang@yo-ren.com
email9=cora.chen@yo-ren.com
email10=christopher@yo-ren.com

variable1=bj-lawson.xlsx

echo $content|mailx -v -s "Weekly report Beijing" -a $path$variable1 $email1, $email2, $email3, $email4, $email5, $email6, $email7, $email8, $email9, $email10
