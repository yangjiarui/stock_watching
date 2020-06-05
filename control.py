# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 17:14
# @Author  : Handsomejerry
# @Site    : 
# @File    : rrrrrrrr.py
# @Software: PyCharm
import os
import subprocess
import time
#
# subprocess.Popen('taskkill /f /t /im mitmdump.exe')
# subprocess.Popen('taskkill /f /t /im mitmdump.exe')
# time.sleep(3)
# # subprocess.Popen('taskkill /f /t /im python.exe')
# # subprocess.Popen('taskkill /f /t /im python.exe')
# # time.sleep(4)
# print('正在整合中间表')
# subprocess.Popen('python D:\colourdata\colourdata\jerry微信模拟_百威\大众微信模拟发送链接群控数据临时处理.py')
# time.sleep(4*60)
# print('中间表整合完成')
#
# subprocess.Popen('python D:\colourdata\colourdata\jerry微信模拟_百威\dazhongweixin_day_sql_es(1).py')
# time.sleep(8*60)
# print('导入ES完成')
#




subprocess.Popen('python 2redis.py')
time.sleep(60)
subprocess.Popen('python calc_angalsfromseq2redis.py')
time.sleep(20)
subprocess.Popen('python decisions.py')





# q3=subprocess.Popen('ipconfig')
# q2=subprocess.Popen('mitmweb')
# q1.wait()

# q1.send_signal('python 大众微信模拟发送链接群控20190423_2.py')
#
# #关闭模拟程序
# q1.args('taskkill /f /t /im python.exe')
#
# ##关闭mitmdump
# taskkill /f /t /im mitmdump.exe
#
#
# python dazhongweixin_day_sql_es.py
#
#
#
# mitmdump -s script_dazhong_weixin20190423.py
#
#
# python 大众微信模拟发送链接群控20190423_2.py
#
#
#
# subprocess.Popen('taskkill /f /t /im mitmdump.exe')